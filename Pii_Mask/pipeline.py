from detectors import regex_detect
from hf_client import ner_detect

def detect_pii(text: str):
    """Hybrid PII detection (regex + NER)."""
    regex_entities = regex_detect(text)
    ner_entities = ner_detect(text)
    # Merge both lists (naive union; you can deduplicate later)
    all_entities = regex_entities + ner_entities
    return all_entities
