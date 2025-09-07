from typing import List, Dict

def mask_text(text: str, entities: List[Dict]) -> str:
    """Replace PII entities with placeholders."""
    entities = sorted(entities, key=lambda x: x["start"], reverse=True)
    masked = text
    for i, ent in enumerate(entities):
        placeholder = f"[{ent['type']}_{i}]"
        masked = masked[:ent["start"]] + placeholder + masked[ent["end"]:]
    return masked
