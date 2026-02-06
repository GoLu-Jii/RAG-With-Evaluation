STEP 1 — core/config.py (START HERE)

Why first?
Everything else depends on config. Changing this later causes refactors.

File: app/core/config.py

What to define:

model names

chunk size

overlap

Qdrant URL

collection name

Example (minimal):

import os

EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4.1-mini"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "documents"


Stop here and commit.

STEP 2 — Ingestion (MOST IMPORTANT)

If ingestion is wrong, everything else is garbage.

2A. ingestion/loader.py

Goal: Load raw text, preserve pages.

Implement:

PDF loader

TXT loader

No chunking. No embeddings.

2B. ingestion/chunker.py

Goal: Deterministic chunking + metadata.

Implement:

chunk size

overlap

attach doc_id, page, source

This file should be pure logic.

2C. ingestion/embedder.py

Goal: Convert text → vectors.

Implement:

embed_texts()

embed_query()

No database. No FastAPI.

🔎 Verification checkpoint (do NOT skip)

Before moving on:

Same PDF → same number of chunks every run

Every chunk has metadata

No OpenAI call outside embedder.py

If this fails → stop.

STEP 3 — Vector Store Layer
3A. retrieval/qdrant.py

Goal: Encapsulate Qdrant.

Implement:

create/init collection

upsert points

raw search

No thresholds yet. No filtering logic.

3B. retrieval/retriever.py

Goal: Retrieval logic.

Implement:

top-k

score threshold

metadata filters

This is where “retrieval techniques” live.

🔎 Verification checkpoint

Query returns chunks

Filters work (doc_id)

Low-score chunks are excluded

Only after this is retrieval “done”.

STEP 4 — Generation (ONLY NOW)
4A. generation/prompts.py

Goal: Write prompts as plain text.

Include:

citation rules

refusal rules (“if context insufficient…”)

No logic. Just strings.

4B. generation/generator.py

Goal: LLM call + answer assembly.

Input:

query

retrieved chunks

Output:

answer

cited chunk IDs

Do NOT do retrieval here.

STEP 5 — API Layer (FastAPI)

Only now do you touch FastAPI.

5A. api/ingest.py

Calls:

loader → chunker → embedder → qdrant.upsert

5B. api/query.py

Calls:

embed_query → retriever → generator


Routes should be thin (10–20 lines max).

STEP 6 — Evaluation (After system works)
evaluation/ragas_eval.py

Implement:

load eval dataset

call /query

compute RAGAS metrics

store results

If you do this earlier, you’ll waste time.

STEP 7 — Observability (Last, but valuable)

Add:

latency logging

token counting

rough cost estimation

This turns “works” into “production-aware”.

Correct Mental Model (tattoo this)
Layer	Determinism
Config	100%
Ingestion	95%
Retrieval	85%
Generation	40%
Evaluation	Meta

Always code from top determinism → bottom determinism.

Common wrong starting points (avoid these)

❌ Starting with FastAPI routes
❌ Writing prompts before retrieval
❌ Adding RAGAS before ingestion works
❌ Writing everything in one file “temporarily”

There is no “temporary” in production code.