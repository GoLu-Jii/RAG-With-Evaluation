from typing import List, Dict, Optional

from qdrant_client import QdrantClient
from app.retrieval.qdrant import raw_search

def retrive(
    client: QdrantClient,
    collection_name: str,
    query_vector: List[float],
    top_k: int = 5,
    score_threshold: Optional[float] = None,   # minimum cosine similarity score
    doc_id: Optional[float] = None
):
    results = raw_search(
        client=client,
        collection_name=collection_name,
        query_vector=query_vector,
        limit=top_k,
    )

    filtered = []

    for r in results:
        score = r.score
        payload = r.payload

        # Apply score threshold if provided
        if score_threshold is not None and score < score_threshold:
            continue

        # Apply metadata filter if provided
        if doc_id is not None and payload.get("doc_id") != doc_id:
            continue

        filtered.append(
            {
                "score": score,
                "text": payload.get("text"),
                "doc_id": payload.get("doc_id"),
                "page": payload.get("page"),
                "source": payload.get("source"),
            }
        )

    return filtered