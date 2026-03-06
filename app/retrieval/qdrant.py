import os 
from typing import List, Dict
import uuid
from dotenv import load_dotenv

from qdrant_client import QdrantClient
from qdrant_client.models import (VectorParams, Distance, PointStruct)


load_dotenv()

url = os.getenv("QDRANT_URL")
api_key = os.getenv("QDRANT_API_KEY")

# def qdrant_client(
#         url: str = "http://localhost:6333",
# )-> QdrantClient:
#     return QdrantClient(url = url)

def qdrant_client(
    url: str = url,
    api_key: str = api_key
)-> QdrantClient:

    if not url or not api_key:
        raise ValueError("missing qdrant url or qdrant api key in the envirenment variable!!!")
    
    return QdrantClient(
        url = url,
        api_key=api_key
    )

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
