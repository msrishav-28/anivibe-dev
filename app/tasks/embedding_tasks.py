"""
Background tasks for embedding generation
"""
from celery import Task
from app.tasks.celery_app import celery_app
import logging

logger = logging.getLogger(__name__)


class CallbackTask(Task):
    """Base task with callbacks"""
    
    def on_success(self, retval, task_id, args, kwargs):
        """Success callback"""
        logger.info(f"Task {task_id} succeeded")
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Failure callback"""
        logger.error(f"Task {task_id} failed: {exc}")


@celery_app.task(base=CallbackTask, bind=True)
def generate_clip_embeddings_task(self, anime_ids: list):
    """
    Generate CLIP embeddings for anime posters (background task)
    
    Args:
        anime_ids: List of anime IDs to process
    
    Returns:
        Number of embeddings generated
    """
    from app.core.ml_models import get_clip_model, encode_image_clip
    from PIL import Image
    from pathlib import Path
    
    logger.info(f"Generating CLIP embeddings for {len(anime_ids)} anime...")
    
    posters_dir = Path("data/posters")
    clip_model, clip_preprocess, _, device = get_clip_model()
    
    embeddings = {}
    processed = 0
    
    for idx, anime_id in enumerate(anime_ids):
        poster_path = posters_dir / f"{anime_id}.jpg"
        
        if not poster_path.exists():
            continue
        
        try:
            image = Image.open(poster_path)
            embedding = encode_image_clip(image, clip_model, clip_preprocess, device)
            embeddings[anime_id] = embedding
            processed += 1
            
            # Update progress
            if processed % 10 == 0:
                self.update_state(
                    state="PROGRESS",
                    meta={"current": processed, "total": len(anime_ids)}
                )
        
        except Exception as e:
            logger.error(f"Error processing anime {anime_id}: {e}")
    
    logger.info(f"✅ Generated {processed} CLIP embeddings")
    return processed


@celery_app.task(base=CallbackTask, bind=True)
def generate_sbert_embeddings_task(self, anime_data: list):
    """
    Generate SBERT embeddings for anime synopses (background task)
    
    Args:
        anime_data: List of dicts with anime_id and synopsis
    
    Returns:
        Number of embeddings generated
    """
    from app.core.ml_models import get_sbert_model, encode_text_sbert
    
    logger.info(f"Generating SBERT embeddings for {len(anime_data)} anime...")
    
    sbert_model = get_sbert_model()
    
    texts = [item["synopsis"] for item in anime_data if item.get("synopsis")]
    anime_ids = [item["anime_id"] for item in anime_data if item.get("synopsis")]
    
    if not texts:
        return 0
    
    # Batch encode
    batch_size = 32
    embeddings = {}
    
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i+batch_size]
        batch_ids = anime_ids[i:i+batch_size]
        
        batch_embeddings = encode_text_sbert(batch_texts, sbert_model)
        
        for anime_id, embedding in zip(batch_ids, batch_embeddings):
            embeddings[anime_id] = embedding
        
        # Update progress
        self.update_state(
            state="PROGRESS",
            meta={"current": len(embeddings), "total": len(texts)}
        )
    
    logger.info(f"✅ Generated {len(embeddings)} SBERT embeddings")
    return len(embeddings)


@celery_app.task(base=CallbackTask)
def update_faiss_index_task(index_type: str = "both"):
    """
    Rebuild FAISS indexes (background task)
    
    Args:
        index_type: Type of index to rebuild (clip, sbert, or both)
    
    Returns:
        Status message
    """
    import sys
    from pathlib import Path
    
    sys.path.insert(0, str(Path(__file__).parents[2]))
    
    from scripts.create_faiss_indexes import create_all_indexes
    
    logger.info(f"Rebuilding FAISS indexes: {index_type}")
    
    try:
        create_all_indexes(use_gpu=False)
        return f"Successfully rebuilt {index_type} indexes"
    except Exception as e:
        logger.error(f"Failed to rebuild indexes: {e}")
        raise
