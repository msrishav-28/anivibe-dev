"""
Atlas (3D Visualization) Endpoints
"""
from fastapi import APIRouter
import random

router = APIRouter()

@router.get("/clusters")
async def get_atlas_clusters():
    """
    Get 3D cluster data for the 'Data Embers' visualization.
    Returns mocked coordinates for now.
    """
    clusters = []
    # Generate some mock 3D data points
    for i in range(50):
        clusters.append({
            "id": i,
            "x": random.uniform(-10, 10),
            "y": random.uniform(-10, 10),
            "z": random.uniform(-10, 10),
            "color": random.choice(["#8B5CF6", "#00F0FF", "#FF0055"]),
            "size": random.uniform(0.5, 2.0)
        })
    
    return {"clusters": clusters}
