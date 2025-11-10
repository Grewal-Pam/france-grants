from fastapi import FastAPI, Query
from sqlalchemy import create_engine, text
from src.utils.africa import AFRICA

import os
from src.ingest.load_sheet import load_csv
from src.ingest.load_to_db import write_df

# -------------------------------------------------------------------
# 🔄 Data bootstrap on startup
# -------------------------------------------------------------------
if not os.path.exists("grants.db"):
    csv_path = "data/raw/grants.csv"
    if os.path.exists(csv_path):
        try:
            print("⚙️  Bootstrapping database from CSV...")
            df = load_csv(csv_path)
            write_df(df, "grants.db")
            print("✅ Database initialized successfully.")
        except Exception as e:
            print(f"❌ Database initialization failed: {e}")
    else:
        print("⚠️ CSV file not found, skipping DB creation.")


app = FastAPI(title="Grants API")
engine = create_engine("sqlite:///./grants.db", future=True)

def placeholders(n): 
    return ",".join([f":c{i}" for i in range(n)])

@app.get("/v1/grants/total")
def total(
    donor: str = Query("France"),
    sector: str = Query("Health"),
    modality: str = Query("Grant")
):
    ph = placeholders(len(AFRICA))

    # Map "Grant" to dataset codes
    GRANT_CODES = ["D01", "Grant"]

    sql = text(f"""
        SELECT SUM(amount_usd) AS total
        FROM grants
        WHERE donor_country = :donor
          AND sector LIKE '%' || :sector || '%'
          AND modality IN ({','.join([f':m{i}' for i in range(len(GRANT_CODES))])})
          AND recipient_country IN ({ph})
    """)

    # Build parameter dictionary
    params = {"donor": donor, "sector": sector}
    for i, m in enumerate(GRANT_CODES):
        params[f"m{i}"] = m
    for i, c in enumerate(sorted(AFRICA)):
        params[f"c{i}"] = c

    with engine.begin() as conn:
        row = conn.execute(sql, params).one()

    return {
        "donor": donor,
        "sector": sector,
        "region": "Africa",
        "total_grant_usd": float(row[0] or 0.0)
    }


@app.get("/v1/grants/by_year")
def by_year(
    donor: str = Query("France"),
    sector: str = Query("Health"),
    modality: str = Query("Grant")
):
    ph = placeholders(len(AFRICA))

    # Map "Grant" to dataset codes
    GRANT_CODES = ["D01", "Grant"]

    sql = text(f"""
        SELECT year, SUM(amount_usd) AS total
        FROM grants
        WHERE donor_country = :donor
          AND sector LIKE '%' || :sector || '%'
          AND modality IN ({','.join([f':m{i}' for i in range(len(GRANT_CODES))])})
          AND recipient_country IN ({ph})
        GROUP BY year
        ORDER BY year
    """)

    # Build parameter dictionary
    params = {"donor": donor, "sector": sector}
    for i, m in enumerate(GRANT_CODES):
        params[f"m{i}"] = m
    for i, c in enumerate(sorted(AFRICA)):
        params[f"c{i}"] = c

    with engine.begin() as conn:
        rows = conn.execute(sql, params).all()

    # Convert SQL rows to JSON-style list
    return [
        {"year": int(y), "total_grant_usd": float(t or 0.0)}
        for (y, t) in rows
    ]
