import requests
from typing import List, Dict

from app.generation.prompts import SYSTEM_PROMPT, build_user_prompt
import os

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("LLM_MODEL", "llama3.1:8b")

OLLAMA_URL = f"{OLLAMA_BASE_URL}/api/generate"
TIMEOUT = 60


# format retrieved chunks into context block with chunk id

def format_chunks(chunks: List[Dict])-> str:
    context_block = []
    
    for chunk in chunks:
        block = (
            f"[{chunk['chunk_id']}]\n"
            f"{chunk['text']}\n"
        )
        context_block.append(block)

    return "\n---\n".join(context_block)


# extract cited chunk id from answer and map back to metadata

def extracted_sources(answer: str, chunks: List[Dict])-> List[Dict]:
    sources = []

    for chunk in chunks:
        c_id = chunk["chunk_id"]
        if f"[{c_id}]" in answer:
            sources.append(
                {
                    "doc_id": chunk["doc_id"],
                    "chunk_id": c_id,
                    "page": chunk['page'],
                }
            )

    return sources


# generate answer using ollama

def generate_answer(
        query: str,
        retrieved_chunk: List[Dict],
)-> Dict:
    
    if not retrieved_chunk:
        return {
            "answer": "I don't know.",
            "sources": [],
        }

    
    context = format_chunks(retrieved_chunk)
    user_prompt = build_user_prompt(query, context)

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": user_prompt,
        "system": SYSTEM_PROMPT,
        "stream": False,
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=TIMEOUT
        )
    except requests.RequestException as e:
        raise RuntimeError(f"Ollama request failed {e}")

    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        detail = ""
        try:
            detail = response.json().get("error", "")
        except ValueError:
            detail = response.text.strip()
        raise RuntimeError(f"Ollama returned HTTP {response.status_code}: {detail}") from e

    try:
        data = response.json()
    except ValueError as e:
        raise RuntimeError("Ollama returned invalid JSON") from e

    if data.get("error"):
        raise RuntimeError(f"Ollama generation error: {data['error']}")

    answer_text = data.get("response", "").strip()
    if not answer_text:
        return {
            "answer": "I don't know.",
            "sources": [],
        }

    sources = extracted_sources(answer_text, retrieved_chunk)

    return{
        "answer": answer_text,
        "sources": sources,
    }
