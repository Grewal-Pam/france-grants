# 🇫🇷 France Development Grants — Open Data & Knowledge Graph Pipeline

[![Build Status](https://img.shields.io/github/actions/workflow/status/Grewal-Pam/france-grants/.github/workflows/ci.yml?branch=dev)](https://github.com/Grewal-Pam/france-grants/actions)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
[![Render](https://img.shields.io/badge/Live%20API-Open-success?logo=render)](https://france-grants.onrender.com/docs)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

> **Live Docs:** https://france-grants.onrender.com/docs  
> **Goal:** Prototype an open data service that answers:  
> _How much development assistance did France provide to African countries for health?_

This project builds a **reproducible, open pipeline** for development-finance transparency — aligned with the data-governance and civic-tech practices used by **ONE Data** and **Data Commons**.

---

## Objectives

| Objective | Completed |
|---|---|
Extract raw grant data | ✅ OECD-style CSV ingestion  
Normalize and standardize entities | ✅ Ministry / agency canonical mapping  
Data quality enforcement | ✅ Null, type, non-negative checks  
Store clean dataset | ✅ SQLite  
Serve as public API | ✅ FastAPI + Swagger  
Export Knowledge Graph | ✅ CSV triples (nodes + edges)  
RDF alignment | ✅ Turtle generator (schema.org-ready)  

---

## 🏗️ Architecture

```mermaid
flowchart LR
    A["Raw CSV (OECD format)"] --> B["Clean & Normalize"]
    B --> C["Entity Resolution (donors, agencies, recipients)"]
    C --> D["Data Quality Rules"]
    D --> E[(SQLite Database)]
    E --> F["FastAPI /docs"]
    E --> G["KG Export: nodes.csv + edges.csv"]
    G --> H["RDF (schema.org) TTL"]
```
---

## 🛠️ Infrastructure & Deployment

For users who want a production-grade, cloud-native pipeline, this repository includes a complete Medallion Architecture (Bronze → Silver → Gold → KG) implemented with:

- Google Cloud Storage (Bronze layer)
- BigQuery (Silver/Gold/KG layers)
- GitHub Actions CI/CD
- Python extraction/load + SQL transformations

 See the full GCP Medallion + Knowledge Graph pipeline in [cloud/](cloud/) — diagrams, SQL models, automated deploy workflows, and reproducible ELT jobs are documented in `cloud/infra/README.md`.
