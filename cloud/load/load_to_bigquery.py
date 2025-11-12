"""
Load raw file from GCS into BigQuery
"""

from google.cloud import bigquery
import os

PROJECT = os.getenv("GCP_PROJECT", "france-grants-analytics")
DATASET = "france_grants"
URI = "gs://france-grants-bronze/raw/grants.csv"

def load_csv_to_bq():
    client = bigquery.Client(project=PROJECT)

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
    )

    table_id = f"{PROJECT}.{DATASET}.external_raw_grants"

    load_job = client.load_table_from_uri(URI, table_id, job_config=job_config)
    load_job.result()

    print(f"✅ Loaded raw CSV into {table_id}")

if __name__ == "__main__":
    load_csv_to_bq()
