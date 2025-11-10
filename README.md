# 🇫🇷 France Development Grants API  

# 🇫🇷 France Development Grants API  

[![Build Status](https://img.shields.io/github/actions/workflow/status/Grewal-Pam/france-health-grants/ci.yml?style=flat-square&label=CI%20Build)](https://github.com/Grewal-Pam/france-health-grants/actions)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue?style=flat-square)
[![Deploy](https://img.shields.io/badge/Render-Live%20API-success?style=flat-square&logo=render)](https://france-grants.onrender.com/docs)
![License](https://img.shields.io/badge/license-MIT-lightgrey?style=flat-square)

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




