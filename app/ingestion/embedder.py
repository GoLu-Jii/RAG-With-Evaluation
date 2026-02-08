# embedding

import requests
from typing import List
from app.core.config import OLLAMA_BASE_URL, EMBEDDING_MODEL


# embede text
def embed_text(texts: List[str])-> List[List[float]]:
    embedding: List[List[float]] = []

    for text in texts:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/embeddings",
            json={
                "model": EMBEDDING_MODEL,
                "prompt": text
            },
            timeout=60,
        )

        response.raise_for_status()
        embedding.append(response.json()["embedding"])

    return embedding


# embede query
def embed_query(text: str) -> List[float]:

    return embed_text([text])[0]
