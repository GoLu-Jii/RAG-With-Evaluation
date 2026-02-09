# embedding

import requests
from typing import List
from app.core.config import OLLAMA_BASE_URL, EMBEDDING_MODEL


def embed_text(texts: List[str]) -> List[List[float]]:
    embeddings: List[List[float]] = []

    for text in texts:
        payload = {
            "model": EMBEDDING_MODEL,
            "input": text
        }

        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/embeddings",
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            raise RuntimeError(response.text)

        data = response.json()
        embeddings.append(data.get("embedding"))

    return embeddings


def embed_query(text: str) -> List[float]:
    return embed_text([text])[0]
