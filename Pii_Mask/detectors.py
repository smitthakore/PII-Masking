import re
from config import REGEX_PATTERNS

def regex_detect(text: str):
    """Run regex-based detection for structured PII."""
    results = []
    for label, pattern in REGEX_PATTERNS.items():
        for match in re.finditer(pattern, text):
            results.append({
                "start": match.start(),
                "end": match.end(),
                "text": match.group(),
                "type": label,
                "score": 1.0  # regex = high confidence
            })
    return results
