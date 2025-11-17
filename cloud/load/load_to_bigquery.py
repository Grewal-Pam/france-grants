"""
Load raw file from GCS into BigQuery (BRONZE LAYER)
Replaces the table on every load to avoid duplicates.
"""

from google.cloud import bigquery
import os

PROJECT = os.getenv("GCP_PROJECT", "france-grants-analytics-478219")
DATASET = "france_grants_bronze"
URI = "gs://france-grants-bronze/raw/grants.csv"

def load_csv_to_bq():
    client = bigquery.Client(project=PROJECT)

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        allow_quoted_newlines=True,
        allow_jagged_rows=True,
        ignore_unknown_values=True,
        max_bad_records=1000,

        write_disposition="WRITE_TRUNCATE"
        # This ensures the table is REPLACED, not appended.
    )

    table_id = f"{PROJECT}.{DATASET}.external_raw_grants"

    load_job = client.load_table_from_uri(
        URI,
        table_id,
        job_config=job_config
    )
    load_job.result()

    print(f"LOADED fresh data into {table_id} (WRITE_TRUNCATE enabled)")

if __name__ == "__main__":
    load_csv_to_bq()
