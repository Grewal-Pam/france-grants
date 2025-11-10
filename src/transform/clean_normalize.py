import pandas as pd
from src.utils.mappings import SECTOR_MAP, MODALITY_MAP, COUNTRY_FIX

# Your dataset uses these names instead of old ones
COLUMN_MAP = {
    "donor_name": "donor_country",
    "recipient_name": "recipient_country",
    "sector_name": "sector",
    "usd_commitment": "amount",
}

REQUIRED = {"donor_country", "recipient_country", "sector", "modality", "amount", "year"}

def normalize(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns=COLUMN_MAP)  # rename to standard names

    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    out = df.copy()

    # strip strings
    for col in ["donor_country", "recipient_country", "sector", "modality"]:
        out[col] = out[col].astype(str).str.strip()

    # fix country names
    out["recipient_country"] = out["recipient_country"].replace(COUNTRY_FIX)
    out["donor_country"] = out["donor_country"].replace(COUNTRY_FIX)

    # map sector/modality
    out["sector"] = out["sector"].map(lambda s: SECTOR_MAP.get(s, s))
    out["modality"] = out["modality"].map(lambda m: MODALITY_MAP.get(m, m))

    # numeric conversions
    out["amount_usd"] = pd.to_numeric(out["amount"], errors="coerce").fillna(0.0)
    out["year"] = pd.to_numeric(out["year"], errors="coerce").astype("Int64").fillna(0).astype(int)

    keep = ["donor_country", "recipient_country", "sector", "modality", "amount_usd", "year"]
    return out[keep]
