# src/agent/planner.py

from typing import Dict, Any
from .perception import QueryType


def build_plan(query: str, query_type: QueryType) -> Dict[str, Any]:
    """
    Return a simple plan structure that the Agent can execute.

    This is not a full LLM planner—just a structured description
    of what steps we will run.
    """
    if query_type == QueryType.HEALTH_AFRICA_COUNTRIES:
        return {
            "query_type": query_type.value,
            "steps": [
                "Load kg/edges_health_africa.csv",
                "Extract unique recipient_country values",
                "Sort country names alphabetically",
                "Return list of countries and basic explanation",
            ],
        }

    if query_type == QueryType.SUMMARY_STATS:
        return {
            "query_type": query_type.value,
            "steps": [
                "Read analysis/summary_stats.csv",
                "Extract metrics: rows, unique_donors, unique_recipients, unique_agencies, total_funding_usd",
                "Format a human-readable summary",
            ],
        }

    # Default: generic semantic RAG
    return {
        "query_type": query_type.value,
        "steps": [
            "Embed the user query using the Embedder",
            "Query Chroma collection 'france_grants' with top-k similarity search",
            "Use the top documents as evidence to compose an answer",
        ],
    }
