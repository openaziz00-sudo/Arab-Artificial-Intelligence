"""Optional local semantic search powered by sentence-transformers."""
from __future__ import annotations

import os
from typing import Any

DEFAULT_MODEL = os.getenv("ARAB_PROMPTS_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

class SemanticIndex:
    def __init__(self, records: list[dict[str, Any]], model_name: str = DEFAULT_MODEL):
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise RuntimeError("ثبت sentence-transformers لتفعيل البحث الدلالي") from exc
        self.records = records
        self.model = SentenceTransformer(model_name)
        self.documents = [self._text(row) for row in records]
        self.embeddings = self.model.encode(self.documents, normalize_embeddings=True, show_progress_bar=False)

    @staticmethod
    def _text(row: dict[str, Any]) -> str:
        return f"{row['title']} {row['summary']} {row['prompt']}"

    def search(self, query: str, category: str | None = None, limit: int = 20) -> list[dict[str, Any]]:
        import numpy as np
        query_vector = self.model.encode([query], normalize_embeddings=True, show_progress_bar=False)[0]
        scores = np.asarray(self.embeddings) @ query_vector
        ranked = np.argsort(-scores)
        result = []
        for index in ranked:
            row = self.records[int(index)]
            if category and row["category"] != category:
                continue
            result.append({**row, "score": round(float(scores[index]), 4)})
            if len(result) >= limit:
                break
        return result
