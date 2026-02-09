# embedding

import requests
from typing import List
from app.core.config import OLLAMA_BASE_URL, EMBEDDING_MODEL


# embede text
def embed_text(texts: List[str])-> List[List[float]]:
    embedding: List[List[float]] = []

    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/embed",
        json={
            "model": EMBEDDING_MODEL,
            "input": texts,
        },
        timeout=60,
    )

    response.raise_for_status()
    embedding.extend(response.json()["embeddings"])

    return embedding


# embede query
def embed_query(text: str) -> List[float]:

    return embed_text([text])[0]
