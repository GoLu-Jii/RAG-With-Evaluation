from app.ingestion.loader import load_pdf
from app.ingestion.chunker import chunk_pages
from app.ingestion.embedder import embed_text, embed_query


# CHANGE THIS to a real local PDF path
SAMPLE_PDF_PATH = "data/uploads/sample.pdf"


def test_chunk_determinism():
    pages = load_pdf(SAMPLE_PDF_PATH)

    chunks_1 = chunk_pages(pages, doc_id="test-doc")
    chunks_2 = chunk_pages(pages, doc_id="test-doc")

    assert len(chunks_1) == len(chunks_2), "Chunk count must be deterministic"


def test_chunk_metadata():
    pages = load_pdf(SAMPLE_PDF_PATH)
    chunks = chunk_pages(pages, doc_id="test-doc")

    sample = chunks[0]

    assert "text" in sample
    assert "doc_id" in sample
    assert "page" in sample
    assert "source" in sample


def test_embedding_shape_consistency():
    pages = load_pdf(SAMPLE_PDF_PATH)
    chunks = chunk_pages(pages, doc_id="test-doc")

    texts = [c["text"] for c in chunks[:3]]
    embeddings = embed_text(texts)

    assert len(embeddings) == len(texts), "Each text must produce one embedding"

    dim = len(embeddings[0])
    assert dim > 0, "Embedding dimension must be > 0"

    for emb in embeddings:
        assert len(emb) == dim, "Embedding dimensions must be consistent"


def test_query_document_embedding_alignment():
    pages = load_pdf(SAMPLE_PDF_PATH)
    chunks = chunk_pages(pages, doc_id="test-doc")

    doc_embedding = embed_text([chunks[0]["text"]])[0]
    query_embedding = embed_query("test question")

    assert len(doc_embedding) == len(query_embedding), (
        "Query and document embeddings must have same dimension"
    )
