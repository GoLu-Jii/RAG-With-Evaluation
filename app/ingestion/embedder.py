from typing import List
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_text(texts: List[str]) -> List[List[float]]:
    if not texts:
        raise ValueError("No texts provided for embedding")

    embeddings = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=False,
        normalize_embeddings=True
    )

    return embeddings.tolist()


def embed_query(text: str) -> List[float]:
    if not text or not text.strip():
        raise ValueError("Query text is empty")

    return embed_text([text])[0]