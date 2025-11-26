# app/streamlit_app.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import json
import os
from datetime import datetime

import streamlit as st

from src.agent.agent import Agent


# -------------------------
# Page config
# -------------------------
st.set_page_config(
    page_title="France Health Grants Agent",
    page_icon="🩺",
    layout="wide",
)


# -------------------------
# Load Agent (cached)
# -------------------------
@st.cache_resource
def load_agent() -> Agent:
    return Agent()


agent = load_agent()


# -------------------------
# Sidebar
# -------------------------
st.sidebar.title("⚙️ Settings")

response_mode = st.sidebar.radio(
    "Response mode",
    options=["RAG + LLM (Groq)", "RAG only"],
    help="Choose whether to summarise evidence with the LLM or show retrieval-only output.",
)

use_llm = response_mode.startswith("RAG +")

st.sidebar.markdown("---")

st.sidebar.subheader("ℹ️ About this app")
st.sidebar.markdown(
    """
This app wraps your **France Health Grants Agent**:

- Uses a **knowledge graph + CSV** as a mini data warehouse  
- Runs **RAG over Chroma** (sentence-transformers MiniLM)  
- Optionally summarises with **Groq (llama-3.1-8b-instant)**  
- Logs every interaction as a **trace JSON** in `outputs/traces/`
"""
)


# -------------------------
# Main layout
# -------------------------
st.title("🩺 France Health Grants Agent")
st.caption("Ask questions about France's health and development funding, backed by your KG + RAG + Groq stack.")

default_question = "Which African countries received health funding from France?"

with st.form("qa_form"):
    question = st.text_input(
        "Ask a question about the France health grants dataset:",
        value=default_question,
        placeholder="e.g. Which African countries received health funding from France?",
    )
    submitted = st.form_submit_button("Ask the Agent")

if submitted and question.strip():
    with st.spinner("Thinking with France Grants Agent..."):
        try:
            result = agent.answer(question.strip(), use_llm=use_llm)
        except Exception as e:
            st.error(f"Agent error: {e}")
            st.stop()

    # -------------------------
    # Top-level answer card
    # -------------------------
    st.markdown("### ✅ Answer")

    st.markdown(
        f"""
**Mode:** `{result.get('mode', 'unknown')}`  
**Query type:** `{result.get('query_type')}`
"""
    )

    st.write(result.get("answer", ""))

    # -------------------------
    # Confidence & metadata
    # -------------------------
    col1, col2, col3 = st.columns(3)

    confidence = float(result.get("confidence", 0.0))
    conf_clamped = max(0.0, min(1.0, confidence))

    with col1:
        st.metric("Confidence (0–1)", f"{confidence:.3f}")
        st.progress(conf_clamped)

    with col2:
        st.text("Arbiter reason:")
        st.write(result.get("arbiter_reason", ""))

    with col3:
        ts_str = result.get("timestamp", "")
        st.text("Timestamp (UTC):")
        st.write(ts_str)

    st.markdown("---")

    # -------------------------
    # Tabs: Answer / Evidence / Plan / Trace
    # -------------------------
    tab_answer, tab_evidence, tab_plan, tab_trace = st.tabs(
        ["🧠 Answer details", "📚 Evidence", "🧩 Plan", "🧾 Trace JSON"]
    )

    # ---- Answer details tab ----
    with tab_answer:
        st.markdown("#### Raw answer text")
        st.write(result.get("answer", ""))

        st.markdown("#### Mode & query type")
        st.json(
            {
                "mode": result.get("mode"),
                "query_type": result.get("query_type"),
                "response_mode_selected": response_mode,
            }
        )

    # ---- Evidence tab ----
    with tab_evidence:
        st.markdown("#### Evidence used by the agent")

        qtype = result.get("query_type")
        evidence = result.get("evidence", {})

        if qtype == "health_africa_countries":
            countries = evidence.get("countries", [])
            st.write(
                f"France is funding health-related projects in **{len(countries)}** African countries:"
            )
            st.write(", ".join(countries))

            st.markdown("**Source file:**")
            st.code(evidence.get("edge_file", ""), language="bash")

        elif qtype == "summary_stats":
            st.write("Summary stats row used as evidence:")
            st.json(evidence)
        else:
            # generic_rag
            results = evidence.get("results", [])
            if not results:
                st.info("No evidence results found.")
            else:
                for i, r in enumerate(results, start=1):
                    with st.expander(f"Result {i} – id={r.get('id')}"):
                        st.markdown(
                            f"**Source:** `{r.get('metadata', {}).get('source')}`  \n"
                            f"**Distance:** `{r.get('distance')}`"
                        )
                        st.markdown("**Text snippet:**")
                        st.write(r.get("text", ""))

    # ---- Plan tab ----
    with tab_plan:
        st.markdown("#### Planner Output")
        st.json(result.get("plan", {}))

    # ---- Trace tab ----
    with tab_trace:
        st.markdown(
            """
The agent logs each interaction as a trace JSON file in `outputs/traces/`.  
Below you see the **in-memory trace object** that was just saved.
"""
        )
        st.json(result)

else:
    st.info("Enter a question and click **Ask the Agent** to get started.")
