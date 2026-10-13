"""HTTP API for the Arabic prompt catalog.

Run locally with: uvicorn api.main:app --reload
"""
from __future__ import annotations

from functools import lru_cache
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from arab_prompts.catalog import categories, get_prompt, prompts, search as lexical_search

app = FastAPI(
    title="Arab Prompts API",
    description="واجهة برمجية مفتوحة لمكتبة البرومبتات العربية.",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@lru_cache(maxsize=1)
def semantic_index():
    from arab_prompts.semantic import SemanticIndex
    return SemanticIndex(prompts())

@app.get("/", tags=["meta"])
def root() -> dict[str, str]:
    return {"name": "Arab Prompts API", "docs": "/docs", "health": "/health"}

@app.get("/health", tags=["meta"])
def health() -> dict[str, Any]:
    return {"status": "ok", "prompts": len(prompts()), "categories": len(categories())}

@app.get("/categories", tags=["catalog"])
def list_categories() -> dict[str, Any]:
    counts = {key: sum(row["category"] == key for row in prompts()) for key in categories()}
    return {"categories": [{"id": key, "name": name, "count": counts[key]} for key, name in categories().items()]}

@app.get("/prompts", tags=["catalog"])
def list_prompts(
    category: str | None = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> dict[str, Any]:
    if category and category not in categories():
        raise HTTPException(404, f"Unknown category: {category}")
    rows = [row for row in prompts() if not category or row["category"] == category]
    return {"items": rows[offset:offset + limit], "total": len(rows), "offset": offset, "limit": limit}

@app.get("/prompts/{prompt_id}", tags=["catalog"])
def prompt_detail(prompt_id: int) -> dict[str, Any]:
    row = get_prompt(prompt_id)
    if row is None:
        raise HTTPException(404, "Prompt not found")
    return row

@app.get("/search", tags=["search"])
def search(
    q: str = Query(..., min_length=1, description="سؤال أو وصف المهمة باللغة العربية أو الإنجليزية"),
    category: str | None = None,
    limit: int = Query(20, ge=1, le=100),
    semantic: bool = Query(True, description="استخدم embeddings محلية عند تفعيلها"),
) -> dict[str, Any]:
    if category and category not in categories():
        raise HTTPException(404, f"Unknown category: {category}")
    if semantic:
        try:
            return {"query": q, "mode": "semantic", "items": semantic_index().search(q, category, limit)}
        except (ImportError, RuntimeError, OSError):
            pass
    return {"query": q, "mode": "lexical", "items": lexical_search(q, category, limit)}
