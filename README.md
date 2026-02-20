<!-- ollama pull nomic-embed-text -->

Install Python Dependencies

Use Python 3.10+ and install dependencies before running the API.

Install from requirements file:
pip install -r requirements.txt


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






