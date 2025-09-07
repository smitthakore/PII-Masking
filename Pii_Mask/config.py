import os

# Environment variables
HF_API_TOKEN = os.environ.get("HF_API_TOKEN", "your token")
HF_ENDPOINT = os.environ.get("HF_ENDPOINT", "")  # Your Inference Endpoint URL
HF_MODEL_REPO = os.environ.get("HF_MODEL_REPO", "dslim/bert-base-NER")

# Regex patterns for structured PII
REGEX_PATTERNS = {
    "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "PHONE": r"\b\+?\d[\d\-\s]{7,}\d\b",
    "IP_ADDRESS": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "CREDIT_CARD": r"\b(?:\d[ -]*?){13,16}\b",
    "PHONE_REGEX" : r"(\+?\d{1,3}[\s\-]?\(?\d{1,4}\)?[\s\-]?\d{2,4}[\s\-]?\d{2,4}[\s\-]?\d{0,9})",
    "GSTIN": r"\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}Z[A-Z\d]{1}"
}
    