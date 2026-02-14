import os 
import uuid 
from fastapi import APIRouter, HTTPException, File, UploadFile
from app.ingestion.loader import load_pdf
from app.ingestion.chunker import chunk_pages
from app.ingestion.embedder import embed_text
from app.retrieval.qdrant import qdrant_client, ensure_collection, upsert_points

from app.core.config import EMBEDDING_DIM, COLLECTION_NAME

router = APIRouter()

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/documents")
async def ingest_document(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="only '.pdf' files allowed!!!")
    
    doc_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        content = await file.read()
        with open (file_path, "wb") as f:
            f.write(content)

        # load
        pages = load_pdf(file_path)

        # chunks
        chunks = chunk_pages(pages, doc_id)

        if not chunks:
            raise HTTPException(status_code=400, detail="file not extracted!!!")
        
        # embede 
        texts = [c["text"] for c in chunks]
        embeddings = embed_text(texts)

        # payloads
        payloads = chunks

        # store in qdrant 
        client = qdrant_client()
        ensure_collection(client, COLLECTION_NAME, EMBEDDING_DIM)
        upsert_points(client, COLLECTION_NAME, embeddings, payloads)

        return {
            "doc_id": doc_id,
            "chunks_indexed": len(chunks),
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))