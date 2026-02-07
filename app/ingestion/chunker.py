# implement chunking 

from typing import List, Dict, Union
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.config import CHUNK_SIZE, CHUNK_OVERLAP

def chunk_pages(
    pages: List[Dict],
    doc_id: str,
    source: str = "upload",
) -> List[Dict]:
    
    # use langchain for chunking 
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = CHUNK_SIZE,
        chunk_overlap = CHUNK_OVERLAP,
        splitter = ["\n\n", "\n", ". ", " "]
    )

    chunks: List[Dict] = []

    for page in pages:
        split_texts = splitter.split_text(page["text"])

        for text in split_texts:
            if not text.strip():
                continue

            chunks.append({
                "text": text.strip(),
                "doc_id": doc_id,
                "page": page[page],
                "source": source
            })
    
    return chunks
