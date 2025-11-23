from fastapi import FastAPI, Query
from google.cloud import bigquery

# ==============================
#  CONFIG
# ==============================
PROJECT = "france-grants-analytics-478219"
DATASET = "france_grants_gold"
TABLE = "fact_enriched"

app = FastAPI(title="France Grants API (BigQuery)")
client = bigquery.Client()


# ==============================
#  HELPER FUNCTION
# ==============================
def run_query(sql: str, params: dict = None):
    job_config = None

    if params:
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter(
                    name, "INT64" if isinstance(value, int) else "STRING", value
                )
                for name, value in params.items()
            ]
        )

    query_job = client.query(sql, job_config=job_config)
    return list(query_job.result())


# ==============================
#  HEALTH CHECK
# ==============================
@app.get("/")
def health():
    return {"status": "ok", "api": "France Grants API"}


# ==============================
#  ENDPOINT 1 — TOP RECIPIENTS
# ==============================
@app.get("/v1/top_recipients")
def top_recipients(year: int = Query(2023)):
    sql = f"""
        SELECT recipient_country, SUM(usd_disbursement) AS total
        FROM `{PROJECT}.{DATASET}.{TABLE}`
        WHERE year = @year
        GROUP BY recipient_country
        ORDER BY total DESC
        LIMIT 10
    """

    rows = run_query(sql, {"year": year})

    return [
        {"recipient": r.recipient_country, "total_usd": float(r.total)}
        for r in rows
    ]


# ==============================
#  ENDPOINT 2 — FUNDING BY AGENCY
# ==============================
@app.get("/v1/by_agency")
def by_agency(year: int = Query(2023), limit: int = 10):
    sql = f"""
        SELECT agency_name, SUM(usd_disbursement) AS total
        FROM `{PROJECT}.{DATASET}.{TABLE}`
        WHERE year = @year
        GROUP BY agency_name
        ORDER BY total DESC
        LIMIT @limit
    """

    rows = run_query(sql, {"year": year, "limit": limit})

    return [
        {"agency": r.agency_name, "total_usd": float(r.total)}
        for r in rows
    ]


# ==============================
#  ENDPOINT 3 — FLOW BREAKDOWN
# ==============================
@app.get("/v1/flow_breakdown")
def flow_breakdown(year: int = Query(2023)):
    sql = f"""
        SELECT flow_name, SUM(usd_disbursement) AS total
        FROM `{PROJECT}.{DATASET}.{TABLE}`
        WHERE year = @year
        GROUP BY flow_name
        ORDER BY total DESC
    """

    rows = run_query(sql, {"year": year})

    return [
        {"flow_type": r.flow_name, "total_usd": float(r.total)}
        for r in rows
    ]


# ==============================
#  ENDPOINT 4 — YEARLY TREND
# ==============================
@app.get("/v1/trends")
def trends(recipient: str = Query("Senegal")):
    sql = f"""
        SELECT year, SUM(usd_disbursement) AS total
        FROM `{PROJECT}.{DATASET}.{TABLE}`
        WHERE recipient_country = @recipient
        GROUP BY year
        ORDER BY year
    """

    rows = run_query(sql, {"recipient": recipient})

    return [
        {"year": int(r.year), "total_usd": float(r.total)}
        for r in rows
    ]
