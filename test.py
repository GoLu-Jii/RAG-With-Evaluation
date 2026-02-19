from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from app.retrieval.retriever import retrive

# --- FIX 1: Define the Client properly ---
# (No need for a wrapper function, just instantiate it directly)
client = QdrantClient(url="http://localhost:6333") 

# --- FIX 2: Load the CORRECT Embedding Model ---
# You MUST use this to search, because your collection is 384 dims.
# Do NOT use Ollama here.
model = SentenceTransformer('all-MiniLM-L6-v2')

# --- FIX 3: Generate the Vector ---
query_text = "What is the text about?"
query_vector = model.encode(query_text).tolist() 

# --- FIX 4: Run the Retrieval ---
retrieved_chunks = retrive(
    client=client,
    collection_name="documents",  # Check exact spelling!
    query_vector=query_vector,
    top_k=5,
    score_threshold=0.01          # Low threshold ensures you see ANY results
)

# Debug Print
print(f"Found {len(retrieved_chunks)} chunks.")
for chunk in retrieved_chunks:
    print(f"Score: {chunk['score']:.3f} | Text: {chunk['text'][:50]}...")