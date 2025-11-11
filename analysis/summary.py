import sqlite3, pandas as pd

conn = sqlite3.connect("grants.db")
df = pd.read_sql("SELECT * FROM grants", conn)

summary = {
    "rows": len(df),
    "unique_donors": df["donor_country"].nunique(),
    "unique_recipients": df["recipient_country"].nunique(),
    "unique_agencies": df["agency_name"].nunique(),
    "total_funding_usd": df["amount_usd"].sum()
}

print(summary)

# Export quick stats for logging or downstream use
pd.DataFrame([summary]).to_csv("analysis/summary_stats.csv", index=False)
