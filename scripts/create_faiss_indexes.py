"""
Create FAISS indexes for fast similarity search
"""
import logging
from pathlib import Path
import sys
import numpy as np
import faiss
import pickle

sys.path.insert(0, str(Path(__file__).parents[1]))

from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

EMBEDDINGS_DIR = Path("data/embeddings")
FAISS_DIR = Path(settings.faiss_index_path)
FAISS_DIR.mkdir(parents=True, exist_ok=True)


def create_faiss_index(
    embeddings: np.ndarray,
    anime_ids: np.ndarray,
    index_name: str,
    use_gpu: bool = False
) -> faiss.Index:
    """
    Create FAISS index from embeddings
    
    Args:
        embeddings: Embedding vectors (N x D)
        anime_ids: Anime IDs corresponding to embeddings
        index_name: Name for the index
        use_gpu: Use GPU for index if available
    
    Returns:
        FAISS index
    """
    n_vectors, dimension = embeddings.shape
    logger.info(f"Creating {index_name} index: {n_vectors} vectors, {dimension} dimensions")
    
    # Normalize embeddings for cosine similarity
    faiss.normalize_L2(embeddings)
    
    # Choose index type based on dataset size
    if n_vectors < 10000:
        # Flat index for small datasets (exact search)
        index = faiss.IndexFlatIP(dimension)
        logger.info(f"Using Flat index (exact search)")
    else:
        # IVF index for larger datasets (approximate search)
        nlist = min(int(np.sqrt(n_vectors)), 1000)  # Number of clusters
        quantizer = faiss.IndexFlatIP(dimension)
        index = faiss.IndexIVFFlat(quantizer, dimension, nlist, faiss.METRIC_INNER_PRODUCT)
        
        logger.info(f"Using IVF index with {nlist} clusters")
        
        # Train the index
        logger.info("Training index...")
        index.train(embeddings)
    
    # Add vectors
    logger.info("Adding vectors to index...")
    index.add(embeddings)
    
    # Use GPU if available and requested
    if use_gpu and faiss.get_num_gpus() > 0:
        logger.info("Moving index to GPU...")
        index = faiss.index_cpu_to_all_gpus(index)
    
    # Save index
    index_path = FAISS_DIR / f"{index_name}_index.faiss"
    faiss.write_index(faiss.index_gpu_to_cpu(index) if use_gpu else index, str(index_path))
    logger.info(f"✅ Saved index: {index_path}")
    
    # Save anime ID mapping
    id_mapping = {i: int(anime_id) for i, anime_id in enumerate(anime_ids)}
    mapping_path = FAISS_DIR / f"{index_name}_id_mapping.pkl"
    
    with open(mapping_path, 'wb') as f:
        pickle.dump(id_mapping, f)
    logger.info(f"✅ Saved ID mapping: {mapping_path}")
    
    return index


def verify_index(index: faiss.Index, embeddings: np.ndarray, index_name: str):
    """Verify index by performing test search"""
    logger.info(f"Verifying {index_name} index...")
    
    # Normalize test vector
    test_vector = embeddings[0:1].copy()
    faiss.normalize_L2(test_vector)
    
    # Search
    k = min(10, embeddings.shape[0])
    distances, indices = index.search(test_vector, k)
    
    logger.info(f"Test search results:")
    logger.info(f"  Top result index: {indices[0][0]}")
    logger.info(f"  Similarity score: {distances[0][0]:.4f}")
    logger.info(f"✅ Index verification successful")


def create_all_indexes(use_gpu: bool = False):
    """Create FAISS indexes for CLIP and SBERT embeddings"""
    
    # Load CLIP embeddings
    clip_embeddings_path = EMBEDDINGS_DIR / "clip_embeddings.npy"
    clip_ids_path = EMBEDDINGS_DIR / "clip_anime_ids.npy"
    
    if clip_embeddings_path.exists() and clip_ids_path.exists():
        logger.info("Creating CLIP index...")
        clip_embeddings = np.load(clip_embeddings_path)
        clip_ids = np.load(clip_ids_path)
        
        clip_index = create_faiss_index(
            clip_embeddings,
            clip_ids,
            "clip",
            use_gpu
        )
        
        verify_index(clip_index, clip_embeddings, "CLIP")
    else:
        logger.warning("CLIP embeddings not found. Run generate_embeddings.py first.")
    
    # Load SBERT embeddings
    sbert_embeddings_path = EMBEDDINGS_DIR / "sbert_embeddings.npy"
    sbert_ids_path = EMBEDDINGS_DIR / "sbert_anime_ids.npy"
    
    if sbert_embeddings_path.exists() and sbert_ids_path.exists():
        logger.info("Creating SBERT index...")
        sbert_embeddings = np.load(sbert_embeddings_path)
        sbert_ids = np.load(sbert_ids_path)
        
        sbert_index = create_faiss_index(
            sbert_embeddings,
            sbert_ids,
            "sbert",
            use_gpu
        )
        
        verify_index(sbert_index, sbert_embeddings, "SBERT")
    else:
        logger.warning("SBERT embeddings not found. Run generate_embeddings.py first.")


def get_index_stats():
    """Display statistics about created indexes"""
    logger.info("\n" + "="*50)
    logger.info("FAISS INDEX STATISTICS")
    logger.info("="*50)
    
    for index_type in ["clip", "sbert"]:
        index_path = FAISS_DIR / f"{index_type}_index.faiss"
        mapping_path = FAISS_DIR / f"{index_type}_id_mapping.pkl"
        
        if index_path.exists():
            index = faiss.read_index(str(index_path))
            
            with open(mapping_path, 'rb') as f:
                id_mapping = pickle.load(f)
            
            logger.info(f"\n{index_type.upper()} Index:")
            logger.info(f"  Vectors: {index.ntotal}")
            logger.info(f"  Dimension: {index.d}")
            logger.info(f"  Anime IDs: {len(id_mapping)}")
            logger.info(f"  Index type: {type(index).__name__}")
            logger.info(f"  Size: {index_path.stat().st_size / 1024 / 1024:.2f} MB")
        else:
            logger.info(f"\n{index_type.upper()} Index: Not found")
    
    logger.info("="*50)


def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Create FAISS indexes")
    parser.add_argument("--gpu", action="store_true", help="Use GPU for index")
    parser.add_argument("--stats", action="store_true", help="Show index statistics")
    args = parser.parse_args()
    
    if args.stats:
        get_index_stats()
    else:
        create_all_indexes(use_gpu=args.gpu)
        get_index_stats()
    
    logger.info("✅ FAISS index creation complete!")


if __name__ == "__main__":
    main()
