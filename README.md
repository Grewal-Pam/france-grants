# 🇫🇷 France Development Grants API  

> **Live Demo:** [https://france-grants.onrender.com/docs](https://france-grants.onrender.com/docs)

A FastAPI-based public API that aggregates France’s development assistance grants and provides queryable endpoints for policy analysis, transparency, and research.  
This project replicates the **ONE Campaign / Data Commons**-style data engineering case study end-to-end.

---

## 🚀 Features
- **ETL Pipeline:** Extracts and cleans raw CSV data of France’s health & development grants.  
- **SQLite-backed API:** Lightweight, file-based data persistence.  
- **Endpoints:**
  - `/v1/grants/total` → total USD grants by donor/sector/modality.  
  - `/v1/grants/by_year` → grant disbursements grouped by year.  
- **Fully container-ready** (Uvicorn + FastAPI).  
- **CI/CD via GitHub Actions + Render Deployment.**  
- **Swagger UI** auto-generated docs.

---

## 🧪 Local Setup

### 1️⃣ Clone & Create Environment
```bash
git clone https://github.com/<your-username>/france-health-grants.git
cd france-health-grants
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt



###2️⃣ Run ETL
python etl.py


This loads data/raw/grants.csv into a local SQLite DB grants.db.

3️⃣ Run the API
uvicorn src.api.main:app --reload


Then open 👉 http://127.0.0.1:8000/docs