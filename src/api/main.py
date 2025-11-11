from fastapi import FastAPI, Query
from sqlalchemy import create_engine, text
from src.utils.africa import AFRICA

import os
import pandas as pd
from sqlalchemy import create_engine
from src.ingest.load_sheet import load_csv
from src.ingest.load_to_db import write_df

DB_PATH = "grants.db"
CSV_PATH = "data/raw/grants.csv"

def bootstrap_database():
    """Ensure the grants.db file and table exist."""
    if not os.path.exists(DB_PATH):
        print("⚙️  Initializing database...")

        if os.path.exists(CSV_PATH):
            print("📄 Loading CSV data...")
            df = load_csv(CSV_PATH)
        else:
            # ✅ Fallback: create minimal DataFrame for CI or fresh envs
            print("⚠️ No CSV found — creating test dataset for CI.")
            df = pd.DataFrame([
                {"donor_country": "France", "recipient_country": "Togo",
                 "sector": "Health", "modality": "Grant",
                 "amount_usd": 100.0, "year": 2023},
                {"donor_country": "France", "recipient_country": "Senegal",
                 "sector": "Education", "modality": "Grant",
                 "amount_usd": 200.0, "year": 2022}
            ])

        try:
            write_df(df, DB_PATH)
            print(f"✅ Created {DB_PATH} with {len(df)} rows.")
        except Exception as e:
            print(f"❌ Database initialization failed: {e}")

    else:
        # quick sanity check
        engine = create_engine(f"sqlite:///{DB_PATH}")
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT name FROM sqlite_master WHERE type='table' AND name='grants';")
            )
            if result.fetchone() is None:
                print("⚠️ No table found — rebuilding DB.")
                os.remove(DB_PATH)
                bootstrap_database()

# Run bootstrap at import time
bootstrap_database()


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
