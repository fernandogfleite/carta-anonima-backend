import re
import unicodedata

_WHITESPACE_RE = re.compile(r"\s+")


def normalize_name(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    normalized = "".join(char for char in normalized if not unicodedata.combining(char))
    normalized = normalized.strip().lower()
    normalized = _WHITESPACE_RE.sub(" ", normalized)
    return normalized
