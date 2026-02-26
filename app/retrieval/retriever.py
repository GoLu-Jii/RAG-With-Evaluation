from typing import List, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

def raw_search(
    client: QdrantClient,
    collection_name: str,
    query_vector: List[float],
    limit: int = 5,
    query_filter: Optional[Filter] = None
):
    try:
        results = client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=limit,
            query_filter=query_filter,
            with_payload=True,
            with_vectors=False
        )
        return results
    except Exception as e:
        raise RuntimeError(f"Qdrant search failed: {e}")


def retrive(
    client: QdrantClient,
    collection_name: str,
    query_vector: List[float],
    top_k: int = 3,
    score_threshold: Optional[float] = None,
    doc_id: Optional[str] = None
):

    qdrant_filter = None
    if doc_id:
        qdrant_filter = Filter(
            must=[
                FieldCondition(
                    key="doc_id", 
                    match=MatchValue(value=doc_id)
                )
            ]
        )

    
    results = raw_search(
        client=client,
        collection_name=collection_name,
        query_vector=query_vector,
        query_filter=qdrant_filter, 
        limit=top_k,
    )

    filtered = []
    
    
    for r in results.points:
        score = r.score
        payload = r.payload

        
        if score_threshold is not None and score < score_threshold:
            continue
            
       

        filtered.append({
            "score": score,
            "chunk_id": payload.get("chunk_id"),
            "text": payload.get("text"),
            "doc_id": payload.get("doc_id"),
            "page": payload.get("page"),
            "source": payload.get("source"),
        })

    return filtered