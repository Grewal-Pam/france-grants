# 🧠 Agent Module – Agentic AI RAG System

This module implements a **state-machine style agentic pipeline** for intelligently exploring France's global health and aid funding using vector search, knowledge graphs, and LLM reasoning.

---

## 🎯 Overview

The agent module orchestrates a multi-stage reasoning system:

```
User Query 
    ↓
Perception (classify query type)
    ↓
Planner (decide execution strategy)
    ↓
Agent Core (execute KG lookup, stats, or RAG)
    ↓
Arbiter (compute confidence & validate)
    ↓
JSON Trace (log results to /outputs/traces/)
```

---

## 📂 Module Structure

| Component | File | Purpose |
|-----------|------|---------|
| **Perception** | `perception.py` | Classifies query into 3 categories: KG lookup, summary stats, or RAG |
| **Planner** | `planner.py` | Decides which execution steps to run based on query type |
| **Agent Core** | `agent.py` | Orchestrates KG lookup, vector search (RAG), and LLM summarization |
| **Arbiter** | `arbiter.py` | Computes confidence scores and validates outputs |
| **Trace** | (JSON logs) | Every run saved to `/outputs/traces/` for debugging & audits |

---

## 🔍 Query Perception (3 Categories)

The `perception.py` module classifies incoming queries:

### Category 1: **KG Lookup**
- **Pattern:** Direct entity or relationship queries
- **Examples:**
  - "Which African countries received health funding?"
  - "Show me donors in the KG"
  - "List all agencies"
- **Execution:** Direct knowledge graph edge/node lookup

### Category 2: **Summary Stats**
- **Pattern:** Aggregate or statistical questions
- **Examples:**
  - "How much did France spend on health in Africa?"
  - "Total funding by year"
  - "Top 5 recipients"
- **Execution:** Pre-computed summary tables + live aggregation

### Category 3: **RAG (Retrieval-Augmented Generation)**
- **Pattern:** Open-ended, descriptive, or context-heavy queries
- **Examples:**
  - "Explain France's health aid strategy in Africa"
  - "What are the trends in funding?"
  - "Provide a detailed overview"
- **Execution:** Vector search → LLM reasoning → Final answer

---

## ⚙️ Planner Logic

The `planner.py` module decides the execution path:

```python
if perception_category == "KG_LOOKUP":
    execute_kg_query()
elif perception_category == "SUMMARY_STATS":
    execute_stats_query()
else:  # RAG
    vector_search() → llm_summarize()
```

The planner also:
- Chains multiple steps if needed (e.g., KG → RAG for context)
- Sets confidence thresholds
- Decides whether to invoke the LLM

---

## 🤖 Agent Core Execution

The `agent.py` orchestrates the actual work:

### KG Lookup
```python
from src.agent.agent import Agent
agent = Agent()
result = agent.kg_lookup(query="countries in health_africa")
```

### Summary Stats
```python
result = agent.summary_stats(metric="total_funding", group_by="year")
```

### RAG (Vector Search + LLM)
```python
result = agent.rag_query(query="Explain France health strategy in Africa")
# Returns: {answer, sources, confidence, trace}
```

---

## 📊 Arbiter & Confidence Scoring

The `arbiter.py` module validates and scores outputs:

- **Confidence score:** 0.0 (low) to 1.0 (high)
- **Validation checks:**
  - Is the query understood?
  - Are results plausible?
  - Is there sufficient source data?
  - Does the LLM answer match the retrieved docs?

Example:
```python
confidence = arbiter.score(query, result, sources)
print(f"Confidence: {confidence:.2%}")  # e.g., 87%
```

---

## 📝 Trace Logging

Every agent run is logged as JSON in `/outputs/traces/`:

```json
{
  "timestamp": "2025-11-26T10:30:45Z",
  "query": "Which African countries received health funding?",
  "perception": "KG_LOOKUP",
  "execution_steps": ["kg_lookup"],
  "results": {
    "countries": ["Benin", "Cameroon", "Ghana", ...],
    "count": 15
  },
  "confidence": 0.95,
  "trace_id": "trace-20251126-103045-abc123"
}
```

This enables:
- Debugging failed queries
- Auditing decisions
- Analyzing user patterns
- Improving perception & planner logic

---

## 🔗 Knowledge Graph Integration

The agent queries custom KG CSVs:

- **`kg/nodes.csv`** — Entities (countries, donors, agencies, flow types)
- **`kg/edges.csv`** — Generic relationships
- **`kg/edges_health_africa.csv`** — Custom Africa health funding relationships

Example query:
```python
edges = agent.kg.get_edges(
    source_type="donor",
    target_type="recipient",
    relationship="funds",
    metadata={"region": "Africa", "sector": "health"}
)
```

---

## 🚀 Vector Search (RAG)

The agent uses **ChromaDB** + **Sentence Transformers (MiniLM-L6-v2)** for document retrieval:

### Build the vector index:
```bash
python -m src.rag.build_index
```

### Query the index:
```python
docs = agent.vector_search(
    query="France health funding trends",
    top_k=5
)
# Returns: [{"text": "...", "score": 0.92}, ...]
```

The LLM then summarizes these docs into a coherent answer.

---

## 🤝 LLM Integration (Groq FREE Tier)

The agent uses **Groq's FREE tier** for LLM inference:

- Model: `llama-3.1-8b-instant`
- Cost: **$0 (free tier)**
- Speed: Very fast (sub-second)

Set your API key:
```bash
export GROQ_API_KEY="your_key_here"
```

Example:
```python
summary = agent.llm_summarize(
    docs=retrieved_docs,
    query="What are trends in health funding?"
)
```

---

## 📖 Example Usage

### Interactive Query
```python
from src.agent.agent import Agent

agent = Agent()

# Query 1: KG Lookup
result = agent.run_query("Which African countries received health funding?")
print(result["answer"])  # List of countries
print(f"Confidence: {result['confidence']:.0%}")

# Query 2: Summary Stats
result = agent.run_query("How much did France spend on health in Africa?")
print(result["answer"])  # e.g., "$500M total"

# Query 3: RAG (open-ended)
result = agent.run_query("Explain France's health aid strategy in Africa")
print(result["answer"])  # Multi-sentence explanation
print(result["sources"])  # Retrieved documents
```

### View Traces
```bash
ls /outputs/traces/
cat /outputs/traces/trace-20251126-*.json
```

---

## 🧪 Testing Query Perception

Test the perception module directly:

```bash
python -c "
from src.agent.perception import classify_query

tests = [
    'Which African countries received health funding?',
    'How much did France spend on health in Africa?',
    'Explain the trends in health aid to Africa',
]

for q in tests:
    print(f'{q} => {classify_query(q)}')
"
```

Expected output:
```
Which African countries received health funding? => KG_LOOKUP
How much did France spend on health in Africa? => SUMMARY_STATS
Explain the trends in health aid to Africa => RAG
```

---

## 🔧 Configuration

### Agent Settings (src/agent/config.py)
```python
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = "llama-3.1-8b-instant"
VECTOR_SEARCH_TOP_K = 5
CONFIDENCE_THRESHOLD = 0.7
TRACE_DIR = "outputs/traces/"
```

### Modify as needed
- Increase `VECTOR_SEARCH_TOP_K` for more context (slower)
- Lower `CONFIDENCE_THRESHOLD` for more lenient scoring
- Change `LLM_MODEL` to a different Groq model (see docs)

---

## 📊 Performance & Metrics

Typical latencies (on single query):

| Stage | Latency |
|-------|---------|
| Perception | ~10ms |
| KG Lookup | ~50ms |
| Vector Search (RAG) | ~200ms |
| LLM Inference | ~1-2s |
| Arbiter Scoring | ~20ms |
| **Total** | **1-3s** |

This keeps the Streamlit app responsive for real-time user interactions.

---

## 🐛 Debugging

### Enable verbose logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)

agent = Agent(debug=True)
result = agent.run_query("Your query")
```

### Check trace files
```bash
# List all traces
find /outputs/traces/ -name "*.json" | sort | tail -5

# Pretty-print a trace
python -m json.tool /outputs/traces/trace-20251126-*.json
```

### Validate KG edges
```python
agent.kg.validate_edges()  # Checks for orphaned nodes, duplicates
```

---

## 🚀 Next Steps

- **Improve perception:** Add more query patterns to `perception.py`
- **Enhance RAG:** Use larger models (e.g., `llama-3.1-70b`) if possible
- **Multi-turn:** Implement conversation memory in `agent.py`
- **Custom metrics:** Add domain-specific confidence scoring in `arbiter.py`
- **Feedback loop:** Collect user feedback and retrain perception classifier

---

## 📚 Related Modules

- **`src/rag/`** — Vector search & document indexing
- **`web/app.py`** — Streamlit UI that calls the agent
- **`kg/`** — Knowledge graph CSVs (nodes & edges)
- **`analysis/`** — Summary stats & pre-computed aggregations

---
