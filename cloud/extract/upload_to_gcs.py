"""
Upload raw OECD CSV data to Google Cloud Storage (Bronze Layer)

This script will be triggered manually or via Airflow later.
"""

import os
from google.cloud import storage

BUCKET_NAME = os.getenv("GCS_BUCKET", "france-grants-data-pam")
LOCAL_FILE = "data/raw/grants.csv"
DEST_FILE = "bronze/cleaned_grants.csv"

def upload_to_gcs():
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(DEST_FILE)

    blob.upload_from_filename(LOCAL_FILE)
    print(f"✅ Uploaded {LOCAL_FILE} -> gs://{BUCKET_NAME}/{DEST_FILE}")

if __name__ == "__main__":
    upload_to_gcs()


#We'll install google-cloud-storage later once SDK works.