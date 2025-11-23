# GCP infra notes
# 🇫🇷 France Grants Cloud ELT + Knowledge Graph Pipeline

This project implements a **cloud-native ELT pipeline** for processing France’s OECD CRS grants dataset and transforming it into a fully structured **analytics warehouse + knowledge graph** using:

- **Google Cloud Storage** (Bronze)
- **BigQuery** (Silver, Gold, KG layers)
- **GitHub Actions** (CI/CD)
- **Python** (Extraction & Load)
- **SQL** (Transformations)
- **Modern Data Lakehouse principles (ELT, Medallion Architecture)**

This is a fully automated, production-grade data pipeline designed using industry best practices.

---

# 🏗️ Architecture Overview (Medallion + KG)

```text
      ┌─────────────────────┐
      │   Raw CSV (local)   │
      └──────────┬──────────┘
                 │ Extract
                 ▼
    ┌──────────────────────────┐
    │    GCS Bronze Bucket     │
    │  gs://france-grants-bronze/raw/grants.csv │
    └──────────┬───────────────┘
                 │ Load
                 ▼
 ┌──────────────────────────────────┐
 │   BigQuery Bronze (Raw Table)    │
 │ france_grants_bronze.external_raw_grants  │
 └──────────┬───────────────────────┘
                 │ Transform (SQL)
                 ▼
    ┌────────────────────────────┐
    │ BigQuery Silver (Cleaned)  │
    │ clean_grants               │
    └──────────┬─────────────────┘
                 │ Transform (SQL)
                 ▼
     ┌────────────────────────────────────┐
     │      BigQuery Gold (Star Model)    │
     │  dim_country, dim_agency,          │
     │  dim_flow_type, dim_income_group,  │
     │  fact_financial_flows              │
     └──────────┬─────────────────────────┘
                 │ Transform (SQL)
                 ▼
┌────────────────────────────────────────────────┐
│ Knowledge Graph (Nodes + Edges Tables)         │
│ nodes_country, nodes_agency, ...               │
│ edges_donor_recipient, edges_donor_agency, edges_agency_recipient, edges_flow_recipient │
└────────────────────────────────────────────────┘
```

---

# 🔥 Features

- **End-to-End Cloud ELT Pipeline** — Raw → Bronze → Silver → Gold → KG. All transformations run in BigQuery.
- **Modern Data Lakehouse** — GCS for raw storage; BigQuery for compute + modeling; SQL-based transformations.
- **Knowledge Graph Construction** — Produces node and edge tables ready for graph export (Neo4j, TigerGraph, NetworkX).
- **CI/CD Orchestration** — GitHub Actions workflows for manual production deploy and tests; secure GCP auth via GitHub Secrets.
- **Idempotent** — Bronze load uses `WRITE_TRUNCATE`; pipeline is reproducible and avoids duplicates.

---

# 📁 Folder Structure (key files)

`cloud/`

`cloud/extract/upload_to_gcs.py` — Upload raw CSV → GCS Bronze

`cloud/load/load_to_bigquery.py` — Load Bronze CSV → BigQuery (WRITE_TRUNCATE)

`cloud/load/create_bq_tables.sql` — Dataset/table DDL

`cloud/warehouse/silver/clean_grants.sql` — Silver transformations

`cloud/warehouse/gold/` — Dimension & fact SQL

`cloud/warehouse/kg/` — Nodes & edges SQL

`.github/workflows/deploy_prod.yml` — Manual full pipeline deploy
`.github/workflows/deploy.yml` — Test / connectivity workflows

`data/raw/grants.csv` — Source CSV (example)

---

# 🪣 GCP Resources (example names)

| Layer  | Bucket / Dataset Name |
|--------|-----------------------|
| Bronze | `france-grants-bronze` / `france_grants_bronze` |
| Silver | `france-grants-silver` / `france_grants_silver` |
| Gold   | `france-grants-gold` / `france_grants_gold` |
| KG     | (KG tables in `france_grants_kg`) |

---

# 🧬 ELT Process Details

## Bronze (raw)
- Stored: `gs://france-grants-bronze/raw/grants.csv`
- Loaded into BigQuery as `france_grants_bronze.external_raw_grants` (WRITE_TRUNCATE)

## Silver (cleaned)
- `clean_grants.sql` normalizes columns, applies `SAFE_CAST`, trimming, lower-casing and null handling.
- Output: `france_grants_silver.clean_grants`

## Gold (star schema)
- Dimensions: `dim_country`, `dim_agency`, `dim_flow_type`, `dim_income_group`
- Fact: `fact_financial_flows`

## Knowledge Graph
- Nodes: country, agency, flow_type, income_group
- Edges: donor→recipient, donor→agency, agency→recipient, flow→recipient

---

# ⚙️ GitHub Actions

Workflows perform: GCP auth → upload CSV to GCS → load into BigQuery → run Silver / Gold / KG SQL in order. The production deploy workflow is manual (dispatch).

---

# 🧪 Quick Verification (BigQuery)

```sql
-- Bronze
SELECT COUNT(*) FROM `france_grants_bronze.external_raw_grants`;

-- Silver
SELECT COUNT(*) FROM `france_grants_silver.clean_grants`;

-- Gold
SELECT COUNT(*) FROM `france_grants_gold.fact_financial_flows`;

-- KG
SELECT COUNT(*) FROM `france_grants_kg.nodes_country`;
```

[Link to Looker studio Report Live Dashboard powered by the Gold-layer `fact_enriched` table.](https://lookerstudio.google.com/reporting/1dc553e1-2dd9-46e0-a0bf-399e43bda429)

### Highlights (from Gold-layer `fact_enriched` table)
- Top funding recipients (2023)
- Funding trend over time
- Funding by agency
- Funding by flow typeime
- Funding by agency
- Funding by flow type