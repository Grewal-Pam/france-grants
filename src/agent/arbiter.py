# src/agent/arbiter.py

from __future__ import annotations
from typing import List, Dict, Any
import math


class Arbiter:
    """
    Very simple arbiter that:
    - For RAG: looks at distances and assigns a confidence score.
    - For tabular/structured results: checks if we have any rows.
    """

    def assess_rag(self, distances: List[float]) -> Dict[str, Any]:
        if not distances:
            return {"confidence": 0.0, "reason": "No results returned from retriever"}

        avg_dist = sum(distances) / len(distances)

        # Chroma by default: smaller distance = closer. We'll just map it crudely.
        # You can tune this later.
        # Example: if avg_dist ~ 0.5 -> high confidence, if > 1.5 -> low.
        confidence = max(0.0, min(1.0, 1.5 - avg_dist))

        return {
            "confidence": confidence,
            "reason": f"Average distance={avg_dist:.3f} mapped to confidence.",
        }

    def assess_tabular(self, n_rows: int) -> Dict[str, Any]:
        if n_rows == 0:
            return {"confidence": 0.0, "reason": "No rows found for this query."}

        # More rows => more robust, but we clip at 1.0
        confidence = max(0.3, min(1.0, math.log10(n_rows + 1)))
        return {
            "confidence": confidence,
            "reason": f"{n_rows} rows found in dataset.",
        }
