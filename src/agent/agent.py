# src/agent/agent.py

import os
import json
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd

from .perception import classify_query, QueryType
from .planner import build_plan
from .arbiter import Arbiter
from src.rag.retriever import Retriever

from groq import Groq  # using Groq for free LLM summarisation (llama-3.1-8b-instant)


class Agent:
    """
    Simple agent over your France health grants project.

    It uses:
    - Perception: classify the query
    - Planner: decide steps
    - Execution:
        * For HEALTH_AFRICA_COUNTRIES -> KG edges_health_africa.csv
        * For SUMMARY_STATS           -> analysis/summary_stats.csv
        * For GENERIC_RAG             -> Chroma retriever (+ optional LLM)
    - Arbiter: compute a confidence score
    - Trace: save everything to outputs/traces/*.json
    """

    def __init__(self) -> None:
        self.arbiter = Arbiter()
        self.retriever = Retriever()

        self.trace_dir = os.path.join("outputs", "traces")
        os.makedirs(self.trace_dir, exist_ok=True)

        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            self.llm_client = Groq()
            self.llm_model = "llama-3.1-8b-instant"
            print("[Agent] Groq LLM configured (llama-3.1-8b-instant).")
        else:
            self.llm_client = None
            self.llm_model = None
            print("[Agent] No GROQ_API_KEY detected → Using retrieval-only mode.")

    # -------------------------
    # Public API
    # -------------------------
    def answer(self, query: str, use_llm: bool = True) -> Dict[str, Any]:
        """
        Main entrypoint for the agent.

        :param query: user question
        :param use_llm: if True and an LLM is configured, use it to summarise RAG.
                        if False, always return retrieval-only answer for generic_rag.
        """
        query_type = classify_query(query)
        plan = build_plan(query, query_type)

        if query_type == QueryType.HEALTH_AFRICA_COUNTRIES:
            result = self._handle_health_africa_countries(query, plan)
        elif query_type == QueryType.SUMMARY_STATS:
            result = self._handle_summary_stats(query, plan)
        else:
            result = self._handle_generic_rag(query, plan, use_llm=use_llm)

        # Save trace for inspection
        self._save_trace(result)

        return result

    # -------------------------
    # Handlers for each type
    # -------------------------
    def _handle_health_africa_countries(
        self, query: str, plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Use your precomputed KG export:
        - kg/edges_health_africa.csv
        where edges are:
        agency_name -> recipient_country with relation=funds_health_in_africa
        """
        path = os.path.join("kg", "edges_health_africa.csv")
        if not os.path.exists(path):
            raise FileNotFoundError(
                "kg/edges_health_africa.csv not found. "
                "Run the KG export script first."
            )

        df = pd.read_csv(path)
        countries = sorted(df["target"].unique().tolist())
        n_countries = len(countries)

        arb = self.arbiter.assess_tabular(n_countries)

        answer_text = (
            f"Based on the health-in-Africa edges in the knowledge graph, "
            f"France (via its agencies) is funding health-related projects in "
            f"{n_countries} African countries. These include:\n\n"
            + ", ".join(countries)
        )

        return {
            "query": query,
            "query_type": QueryType.HEALTH_AFRICA_COUNTRIES.value,
            "mode": "tabular_kg",
            "plan": plan,
            "answer": answer_text,
            "confidence": arb["confidence"],
            "arbiter_reason": arb["reason"],
            "evidence": {
                "countries": countries,
                "edge_file": path,
            },
            "timestamp": datetime.utcnow().isoformat(),
        }

    def _handle_summary_stats(
        self, query: str, plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        path = os.path.join("analysis", "summary_stats.csv")
        if not os.path.exists(path):
            raise FileNotFoundError(
                "analysis/summary_stats.csv not found. "
                "Run the summary stats script first."
            )

        df = pd.read_csv(path)
        row = df.iloc[0].to_dict()

        arb = self.arbiter.assess_tabular(int(row.get("rows", 0)))

        answer_text = (
            "Here is a quick summary of the France health grants dataset:\n"
            f"- Rows (grants): {row.get('rows')}\n"
            f"- Unique donors: {row.get('unique_donors')}\n"
            f"- Unique recipients: {row.get('unique_recipients')}\n"
            f"- Unique agencies: {row.get('unique_agencies')}\n"
            f"- Total funding (USD): {row.get('total_funding_usd')}"
        )

        return {
            "query": query,
            "query_type": QueryType.SUMMARY_STATS.value,
            "mode": "tabular_summary",
            "plan": plan,
            "answer": answer_text,
            "confidence": arb["confidence"],
            "arbiter_reason": arb["reason"],
            "evidence": row,
            "timestamp": datetime.utcnow().isoformat(),
        }

    # -------------------------
    # LLM summariser for RAG
    # -------------------------
    def _summarize_rag_with_llm(
        self,
        query: str,
        results: List[Dict[str, Any]],
        rag_confidence: float,
    ) -> str:
        """
        Use Groq LLM to turn raw RAG results into a human-readable answer.

        - query: user question
        - results: list of {id, text, metadata, distance}
        - rag_confidence: score from Arbiter (0..1), we pass it as a hint
        """

        if not self.llm_client or not self.llm_model:
            return "LLM client not configured; cannot summarize RAG results."

        # Build a compact "evidence" text block for the prompt
        evidence_lines = []
        for i, r in enumerate(results, start=1):
            src = r["metadata"].get("source")
            snippet = r["text"][:350].replace("\n", " ")
            evidence_lines.append(
                f"[{i}] source={src}, distance={r['distance']:.3f} :: {snippet}"
            )

        evidence_block = "\n".join(evidence_lines)

        prompt = f"""
        You are an analyst for a dataset of France's development and health grants.

        User question:
        \"\"\"{query}\"\"\"

        RAG retrieval confidence (0 to 1): {rag_confidence:.3f}

        Here are the top retrieved knowledge graph entries and summary rows:

        {evidence_block}

        TASK:
        1. Answer the user's question as accurately as you can.
        2. If the evidence clearly answers the question, give a direct and concise answer.
        3. If the evidence is indirect or incomplete, say so explicitly, but still provide your best interpretation.
        4. Mention specific countries, sectors or agencies only if the evidence supports them.

        Return ONLY the final answer in natural language, no bullet list of evidence.
        """

        resp = self.llm_client.chat.completions.create(
            model=self.llm_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You summarise France's health and development grants "
                        "based on retrieved evidence."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )

        # Groq SDK: message is an object, not a dict
        return resp.choices[0].message.content

    # -------------------------
    # Generic RAG handler
    # -------------------------
    def _handle_generic_rag(
        self,
        query: str,
        plan: Dict[str, Any],
        use_llm: bool = True,
    ) -> Dict[str, Any]:
        # Use your existing Retriever wrapper
        results = self.retriever.search(query, k=5)
        distances = [r["distance"] for r in results]

        arb = self.arbiter.assess_rag(distances)

        if use_llm and self.llm_client is not None:
            answer_text = self._summarize_rag_with_llm(
                query=query,
                results=results,
                rag_confidence=arb["confidence"],
            )
            mode = "rag+llm"
        else:
            # Retrieval-only fallback / explicit RAG-only mode
            snippet_lines: List[str] = []
            for i, r in enumerate(results, start=1):
                src = r["metadata"].get("source")
                snippet = r["text"][:180].replace("\n", " ")
                snippet_lines.append(
                    f"{i}. [source={src}, distance={r['distance']:.3f}] {snippet}..."
                )

            answer_text = (
                "I looked up semantically similar entries in the France grants "
                "knowledge base. Here are the most relevant pieces of evidence:\n\n"
                + "\n".join(snippet_lines)
            )
            mode = "rag_only"

        # small note for low-confidence answers
        if arb["confidence"] < 0.4:
            answer_text += (
                "\n\n⚠️ Note: Retrieval confidence is relatively low; "
                "this answer may be incomplete or approximate."
            )

        return {
            "query": query,
            "query_type": QueryType.GENERIC_RAG.value,
            "mode": mode,
            "plan": plan,
            "answer": answer_text,
            "confidence": arb["confidence"],
            "arbiter_reason": arb["reason"],
            "evidence": {
                "results": results,
            },
            "timestamp": datetime.utcnow().isoformat(),
        }

    # -------------------------
    # Trace logging
    # -------------------------
    def _save_trace(self, result: Dict[str, Any]) -> None:
        ts = result.get("timestamp", datetime.utcnow().isoformat())
        safe_ts = ts.replace(":", "").replace("-", "").replace(".", "")
        filename = f"trace_{safe_ts}.json"
        path = os.path.join(self.trace_dir, filename)

        to_save = {
            "query": result.get("query"),
            "query_type": result.get("query_type"),
            "mode": result.get("mode"),
            "plan": result.get("plan"),
            "answer": result.get("answer"),
            "confidence": result.get("confidence"),
            "arbiter_reason": result.get("arbiter_reason"),
            "evidence": result.get("evidence"),
            "timestamp": result.get("timestamp"),
        }

        with open(path, "w") as f:
            json.dump(to_save, f, indent=2)

        print(f"[Agent] Trace saved to {path}")
