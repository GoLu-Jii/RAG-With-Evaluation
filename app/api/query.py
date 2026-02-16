# query
# → embed_query
# → retrieve
# → generate_answer
# → measure latency
# → return structured JSON

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import time

from app.core.config import COLLECTION_NAME
from app.ingestion.embedder import embed_query
from app.retrieval.qdrant import qdrant_client
from app.retrieval.retriever import retrive
from app.generation.generation import generate_answer


router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/query")
async def query_document(request: QueryRequest):

    start_time = time.time()

    try:
        client = qdrant_client()

        # query_vector
        query_vector = embed_query(request.query)

        # retrieve chunks

        retrieved_chunks = retrive(
                client = client,
                collection_name = COLLECTION_NAME,
                query_vector = query_vector,
                top_k = 5,
                score_threshold = 0.5,   # minimum cosine similarity score
        )

        # handel empty retrieval 
        if not retrieved_chunks:
            latency_ms = int((time.time() - start_time) * 1000)
            return{
                "answer": "I don't know",
                "sources": [],
                "latency": latency_ms,
            }
        

        # generate answer
        result = generate_answer(
            query=request.query,
            retrieved_chunk=retrieved_chunks
        )

        latency_ms = int((time.time() - start_time) * 1000)

        return{
            "answer": result["answer"],
            "sources": result["sources"],
            "latency": latency_ms,
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))