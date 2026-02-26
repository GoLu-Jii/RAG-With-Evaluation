from qdrant_client import QdrantClient
from app.ingestion.embedder import embed_query  # adjust import
from app.retrieval.retriever import retrive     # adjust import

COLLECTION_NAME = "documents"

# def test_retrieval():
#     client = QdrantClient("http://localhost:6333")

#     query = "What are hallucinations in GPT models?"
#     vector = embed_query(query)

#     results = retrive(
#         client=client,
#         collection_name=COLLECTION_NAME,
#         query_vector=vector,
#         top_k=3,
#         score_threshold=0.6
#     )

#     print("\nResults:\n")
#     for r in results:
#         print("Score:", round(r["score"], 4))
#         print("Doc:", r["doc_id"])
#         print("Chunk:", r["chunk_id"])
#         print("Text preview:", r["text"][:120])
#         print("-" * 60)


# if __name__ == "__main__":
#     test_retrieval()

client = QdrantClient("http://localhost:6333")

client.delete_collection("documents")
# scroll = client.scroll(
#     collection_name="documents",
#     limit=15,
#     with_payload=True
# )

# for p in scroll[0]:
#     print(p.payload["chunk_id"], p.payload["text"][:200])