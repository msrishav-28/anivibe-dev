"""
Generate CLIP and BERT embeddings for all anime
Save to MongoDB for fast retrieval
"""
import asyncio
import logging
from pathlib import Path
import sys
import numpy as np
from PIL import Image
import torch
from typing import Dict, List
import json

sys.path.insert(0, str(Path(__file__).parents[1]))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import AsyncSessionLocal, get_mongodb
from app.core.ml_models import (
    get_clip_model,
    get_sbert_model,
    encode_image_clip,
    encode_text_sbert
)
from app.models.anime import Anime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

POSTERS_DIR = Path("data/posters")
EMBEDDINGS_DIR = Path("data/embeddings")
EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)


class EmbeddingGenerator:
    """Generate and save embeddings for anime"""
    
    def __init__(self):
        self.clip_model = None
        self.clip_preprocess = None
        self.clip_tokenizer = None
        self.device = None
        self.sbert_model = None
        self.mongodb = None
        
    def initialize_models(self):
        """Load ML models"""
        logger.info("Loading ML models...")
        
        # Load CLIP
        self.clip_model, self.clip_preprocess, self.clip_tokenizer, self.device = get_clip_model()
        logger.info("✅ CLIP loaded")
        
        # Load SBERT
        self.sbert_model = get_sbert_model()
        logger.info("✅ SBERT loaded")
        
        # Get MongoDB
        self.mongodb = get_mongodb()
        logger.info("✅ MongoDB connected")
    
    async def generate_clip_image_embeddings(self, anime_list: List[Anime]) -> Dict[int, np.ndarray]:
        """Generate CLIP embeddings from poster images"""
        logger.info("Generating CLIP image embeddings...")
        
        embeddings = {}
        processed = 0
        failed = 0
        
        for anime in anime_list:
            poster_path = POSTERS_DIR / f"{anime.id}.jpg"
            
            if not poster_path.exists():
                failed += 1
                continue
            
            try:
                # Load and process image
                image = Image.open(poster_path)
                
                # Generate embedding
                embedding = encode_image_clip(
                    image,
                    self.clip_model,
                    self.clip_preprocess,
                    self.device
                )
                
                embeddings[anime.id] = embedding
                processed += 1
                
                if processed % 100 == 0:
                    logger.info(f"CLIP: {processed}/{len(anime_list)} processed")
            
            except Exception as e:
                logger.error(f"Error processing anime {anime.id}: {e}")
                failed += 1
        
        logger.info(f"✅ CLIP embeddings: {processed} processed, {failed} failed")
        return embeddings
    
    async def generate_sbert_text_embeddings(self, anime_list: List[Anime]) -> Dict[int, np.ndarray]:
        """Generate SBERT embeddings from synopsis"""
        logger.info("Generating SBERT text embeddings...")
        
        embeddings = {}
        texts_to_encode = []
        anime_ids = []
        
        # Prepare texts
        for anime in anime_list:
            if not anime.synopsis:
                continue
            
            # Combine synopsis with genres and tags for richer embeddings
            text_parts = [anime.synopsis]
            
            if anime.genres:
                genres_str = ", ".join([g.name for g in anime.genres])
                text_parts.append(f"Genres: {genres_str}")
            
            if anime.tags:
                tags_str = ", ".join([t.name for t in anime.tags[:10]])  # Top 10 tags
                text_parts.append(f"Tags: {tags_str}")
            
            combined_text = ". ".join(text_parts)
            texts_to_encode.append(combined_text)
            anime_ids.append(anime.id)
        
        # Batch encode
        logger.info(f"Encoding {len(texts_to_encode)} synopses...")
        
        batch_size = 32
        for i in range(0, len(texts_to_encode), batch_size):
            batch_texts = texts_to_encode[i:i+batch_size]
            batch_ids = anime_ids[i:i+batch_size]
            
            batch_embeddings = encode_text_sbert(batch_texts, self.sbert_model)
            
            for anime_id, embedding in zip(batch_ids, batch_embeddings):
                embeddings[anime_id] = embedding
            
            if (i + batch_size) % 320 == 0:
                logger.info(f"SBERT: {i + batch_size}/{len(texts_to_encode)} processed")
        
        logger.info(f"✅ SBERT embeddings: {len(embeddings)} generated")
        return embeddings
    
    async def save_to_mongodb(self, clip_embeddings: Dict, sbert_embeddings: Dict):
        """Save embeddings to MongoDB"""
        logger.info("Saving embeddings to MongoDB...")
        
        collection = self.mongodb['anime_embeddings']
        
        # Prepare documents
        documents = []
        
        for anime_id in set(clip_embeddings.keys()) | set(sbert_embeddings.keys()):
            doc = {
                "anime_id": anime_id,
                "timestamp": asyncio.get_event_loop().time()
            }
            
            if anime_id in clip_embeddings:
                doc["clip_embedding"] = clip_embeddings[anime_id].tolist()
            
            if anime_id in sbert_embeddings:
                doc["sbert_embedding"] = sbert_embeddings[anime_id].tolist()
            
            documents.append(doc)
        
        # Insert in batches
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i+batch_size]
            await collection.insert_many(batch)
            
            if (i + batch_size) % 1000 == 0:
                logger.info(f"Saved {i + batch_size}/{len(documents)} to MongoDB")
        
        logger.info(f"✅ Saved {len(documents)} embeddings to MongoDB")
    
    def save_to_disk(self, clip_embeddings: Dict, sbert_embeddings: Dict):
        """Save embeddings to disk as numpy arrays"""
        logger.info("Saving embeddings to disk...")
        
        # Save CLIP embeddings
        if clip_embeddings:
            anime_ids = list(clip_embeddings.keys())
            embeddings_array = np.array([clip_embeddings[aid] for aid in anime_ids])
            
            np.save(EMBEDDINGS_DIR / "clip_embeddings.npy", embeddings_array)
            np.save(EMBEDDINGS_DIR / "clip_anime_ids.npy", np.array(anime_ids))
            
            logger.info(f"✅ Saved CLIP: {embeddings_array.shape}")
        
        # Save SBERT embeddings
        if sbert_embeddings:
            anime_ids = list(sbert_embeddings.keys())
            embeddings_array = np.array([sbert_embeddings[aid] for aid in anime_ids])
            
            np.save(EMBEDDINGS_DIR / "sbert_embeddings.npy", embeddings_array)
            np.save(EMBEDDINGS_DIR / "sbert_anime_ids.npy", np.array(anime_ids))
            
            logger.info(f"✅ Saved SBERT: {embeddings_array.shape}")
        
        # Save metadata
        metadata = {
            "clip_count": len(clip_embeddings),
            "sbert_count": len(sbert_embeddings),
            "clip_dim": len(next(iter(clip_embeddings.values()))) if clip_embeddings else 0,
            "sbert_dim": len(next(iter(sbert_embeddings.values()))) if sbert_embeddings else 0,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        with open(EMBEDDINGS_DIR / "metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)


async def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate anime embeddings")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of anime")
    parser.add_argument("--clip-only", action="store_true", help="Generate only CLIP embeddings")
    parser.add_argument("--sbert-only", action="store_true", help="Generate only SBERT embeddings")
    parser.add_argument("--skip-mongodb", action="store_true", help="Skip MongoDB save")
    args = parser.parse_args()
    
    # Initialize generator
    generator = EmbeddingGenerator()
    generator.initialize_models()
    
    # Get anime from database
    logger.info("Loading anime from database...")
    async with AsyncSessionLocal() as session:
        query = select(Anime)
        
        if args.limit:
            query = query.limit(args.limit)
        
        result = await session.execute(query)
        anime_list = result.scalars().all()
    
    logger.info(f"Processing {len(anime_list)} anime...")
    
    # Generate embeddings
    clip_embeddings = {}
    sbert_embeddings = {}
    
    if not args.sbert_only:
        clip_embeddings = await generator.generate_clip_image_embeddings(anime_list)
    
    if not args.clip_only:
        sbert_embeddings = await generator.generate_sbert_text_embeddings(anime_list)
    
    # Save embeddings
    generator.save_to_disk(clip_embeddings, sbert_embeddings)
    
    if not args.skip_mongodb:
        await generator.save_to_mongodb(clip_embeddings, sbert_embeddings)
    
    logger.info("✅ Embedding generation complete!")


if __name__ == "__main__":
    asyncio.run(main())
