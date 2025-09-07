import os
import time
import requests
from typing import List, Dict
from config import HF_API_TOKEN, HF_ENDPOINT, HF_MODEL_REPO

HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"} if HF_API_TOKEN else {}

def call_hf_inference(payload: dict, timeout: int = 30, max_retries: int = 2):
    """Call Hugging Face Inference Endpoint or public API with retries."""
    if HF_ENDPOINT:
        url = HF_ENDPOINT.rstrip("/")
    else:
        url = f"https://api-inference.huggingface.co/models/{HF_MODEL_REPO}"

    for attempt in range(max_retries + 1):
        try:
            resp = requests.post(url, headers=HEADERS, json=payload, timeout=timeout)
            if resp.status_code == 200:
                return resp.json()
            if resp.status_code in (429, 503) and attempt < max_retries:
                time.sleep(2 ** attempt)
                continue
            resp.raise_for_status()
        except Exception as e:
            if attempt == max_retries:
                raise e
            time.sleep(1)
    return {}

def ner_detect(text: str) -> List[Dict]:
    """Call NER model and normalize output."""
    if not text.strip():
        return []

    payload = {
        "inputs": text,
        "parameters": {"aggregation_strategy": "simple"},
        "options": {"wait_for_model": True}
    }

    raw = call_hf_inference(payload)
    results = []
    if isinstance(raw, list):
        for ent in raw:
            start = ent.get("start")
            end = ent.get("end")
            label = ent.get("entity_group") or ent.get("entity")
            score = ent.get("score", 0.0)
            if start is None or end is None:
                continue
            snippet = text[start:end]
            results.append({
                "start": int(start),
                "end": int(end),
                "text": snippet,
                "type": label,
                "score": float(score)
            })
    return results
