## stepwise roadmap for the project 


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

# Progress 09/02/2026

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

# progress 12-02-2026

STEP 4 — Generation (Ollama + Structured Output)

Only begin generation after retrieval is verified.

Goal: Turn retrieved chunks into answers with citations.

4A. generation/prompts.py

Write prompts as plain text.

Include:

citation rules

refusal rule if context insufficient

instruction to cite chunk IDs

No logic here.

Example instruction:

Use ONLY the provided context.
Cite chunk IDs in brackets.
If context insufficient, say "I don't know".
4B. generation/generator.py

Goal: Call Ollama and assemble structured output.

Input:

query

retrieved chunks

Output:

{
  "answer": "...",
  "sources": [
    {
      "doc_id": "...",
      "chunk_id": "...",
      "page": 2
    }
  ]
}

Rules:

Call Ollama locally (http://localhost:11434)

Inject context

Track chunk IDs manually

Add timeout handling

No retrieval logic inside generator

STEP 5 — API Layer (FastAPI Integration)

Routes must remain thin (10–20 lines).

5A. api/ingest.py

Pipeline:

loader → chunker → embedder → qdrant.upsert

Return:

{
  "doc_id": "...",
  "chunks_indexed": 42
}

Add:

file upload support

error handling

5B. api/query.py (MOST IMPORTANT ROUTE)

Pipeline:

embed_query → retriever → generator

Return:

{
  "answer": "...",
  "sources": [...],
  "latency_ms": 120
}

Add:

latency timing

empty retrieval handling

fallback message

clean JSON output

STEP 6 — Evaluation (Visible & Resume-Ready)

Only after system works end-to-end.

File: evaluation/ragas_eval.py

Implement:

20–30 test questions

call /query

compute metrics

store results

Create:

evaluation_report.md

Include:

metrics

failure cases

improvements made

sample outputs

This is required for internship signal.

STEP 7 — Dockerization (Required)

Goal: Run project in one command.

Add:

Dockerfile (FastAPI app)

docker-compose.yml

Services:

api

qdrant

ollama (optional or local)

Command to run:

docker compose up

Provide .env.example.

STEP 8 — README + Demo

Convert project → internship-ready.

README must include:

architecture diagram

how retrieval works

how generation works

evaluation results

run instructions

limitations

Record:
90-second demo video
Show:

upload

query

citations

evaluation metrics

STEP 9 — Observability (Light)

Add:

latency logging

token estimate

chunk count returned

rough cost estimate

Log to console.
Show sample in README.