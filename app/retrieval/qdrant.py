from typing import List, Dict
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import (VectorParams, Distance, PointStruct)

def qdrant_client(
        url: str = "http://localhost:6333",
)-> QdrantClient:
    return QdrantClient(url = url)


# check if collection exists if not create one 

def ensure_collection(client: QdrantClient, collection_name: str, vector_size: int)-> None:
    existing = {c.name for c in client.get_collections().collections}

    if collection_name in existing:
        return
    
    # create collection
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size = vector_size,
            distance=Distance.COSINE,
        ),
    )


# store chunk embedding + metadata into qdrant

def upsert_points(
        client: QdrantClient,
        collection_name: str,
        embeddings: List[List[float]],
        payloads: List[Dict],
)-> None:
    if len(payloads) != len(embeddings):
        raise ValueError("payload and embedding length mismatch !!! ")
    
    # points contains embeddings + metadata
    points = []

    for vector, payload in zip(embeddings, payloads):
        points.append(
            PointStruct(
                id= str(uuid.uuid4()),
                vector=vector,
                payload=payload,
            )
        )
    client.upsert(
        collection_name=collection_name,
        points=points
    )


# perform search in embeddings 

def raw_search(
    client: QdrantClient,
    collection_name: str,
    query_vector: List[float],
    limit: int = 5
):

    try:
        results = client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=limit
        )
        
        return results
        
    except Exception as e:
        raise Exception(f"Search failed: {str(e)}")
