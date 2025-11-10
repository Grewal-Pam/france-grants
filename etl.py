import sys
from src.ingest.load_sheet import load_csv
from src.transform.clean_normalize import normalize
from src.ingest.load_to_db import write_df

if __name__ == "__main__":
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "data/raw/grants.csv"
    df = load_csv(csv_path)
    clean = normalize(df)
    write_df(clean)
    print(f"Loaded {len(clean):,} rows.")
