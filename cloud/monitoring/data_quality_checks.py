"""
Basic SQL data quality checks on BigQuery tables
"""

from google.cloud import bigquery

client = bigquery.Client()

checks = {
    "no_negative_amounts": "SELECT COUNT(*) FROM france_grants.silver_clean_grants WHERE amount_usd < 0",
    "no_null_countries": "SELECT COUNT(*) FROM france_grants.silver_clean_grants WHERE donor_country IS NULL OR recipient_country IS NULL",
}

for name, query in checks.items():
    count = list(client.query(query))[0][0]
    print(f"{name}: {count}")
