# implement chunking 

from typing import List, Dict
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
        separators = ["\n\n", "\n", ". ", " "]
    )

    chunks: List[Dict] = []

    for page in pages:
        split_texts = splitter.split_text(page["text"])

        for chunk_index, text in enumerate(split_texts):
            if not text.strip():
                continue

            chunks.append({
                "chunk_id": f"{doc_id}_p{page['page']}_c{chunk_index}",
                "text": text.strip(),
                "doc_id": doc_id,
                "page": page["page"],
                "source": source
            })
    
    return chunks
