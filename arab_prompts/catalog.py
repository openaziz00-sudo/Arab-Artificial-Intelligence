"""Load and query the bundled Arabic prompt catalog."""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

DATA_PATH = Path(__file__).parent / "data" / "prompts.json"

@lru_cache(maxsize=1)
def _catalog() -> dict[str, Any]:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))

def prompts() -> list[dict[str, Any]]:
    return list(_catalog()["prompts"])

def categories() -> dict[str, str]:
    return dict(_catalog()["categories"])

def get_prompt(prompt_id: int) -> dict[str, Any] | None:
    return next((item for item in prompts() if item["id"] == prompt_id), None)

def search(query: str, category: str | None = None, limit: int = 20) -> list[dict[str, Any]]:
    """Fast dependency-free lexical search; use the API for semantic search."""
    terms = query.casefold().split()
    rows = [p for p in prompts() if not category or p["category"] == category]
    scored = []
    for item in rows:
        title = item["title"].casefold()
        haystack = " ".join((item["title"], item["summary"], item["prompt"])).casefold()
        score = sum(haystack.count(term) for term in terms) + 3 * sum(title.count(term) for term in terms)
        if query.casefold() in title:
            score += 10
        if score:
            scored.append((score, item))
    return [item for _, item in sorted(scored, key=lambda pair: (-pair[0], pair[1]["id"]))[:limit]]
