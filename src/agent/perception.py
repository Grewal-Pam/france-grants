# src/agent/perception.py

from enum import Enum


class QueryType(str, Enum):
    HEALTH_AFRICA_COUNTRIES = "health_africa_countries"
    SUMMARY_STATS = "summary_stats"
    GENERIC_RAG = "generic_rag"


def normalize(text: str) -> str:
    return text.lower().strip()


def classify_query(query: str) -> QueryType:
    """
    Very simple rule-based perception step.

    It looks for key phrases and decides which "mode" we should use.

    - HEALTH_AFRICA_COUNTRIES:
      Queries about health + Africa + France (= use KG edges_health_africa.csv)

    - SUMMARY_STATS:
      Queries about number of rows, total funding, unique donors, etc.

    - GENERIC_RAG:
      Everything else -> send to vector retriever.
    """
    q = normalize(query)

    # 1. Health Africa countries questions
   # 1. Health Africa questions (broad & robust)
    if (
        "africa" in q
        and ("health" in q or "fund" in q or "aid" in q)
        and ("france" in q or "french" in q)
    ):
        return QueryType.HEALTH_AFRICA_COUNTRIES




    # 2. Summary / stats questions
    if any(
        kw in q
        for kw in [
            "how many rows",
            "how many grants",
            "total funding",
            "total amount",
            "unique donors",
            "unique recipients",
            "summary stats",
        ]
    ):
        return QueryType.SUMMARY_STATS

    # 3. Default: semantic RAG
    return QueryType.GENERIC_RAG
