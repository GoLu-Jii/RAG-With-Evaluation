import os

# ollama settings 
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("LLM_MODEL", "llama3.1:8b")

# models
EMBEDDING_DIM = 384
LLM_MODEL = "llama3.1:8b"

# chunks
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# vector_db
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "documents"

# groq
GROQ_API_KEY="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"
