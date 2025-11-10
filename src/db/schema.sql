CREATE TABLE IF NOT EXISTS grants (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  donor_country TEXT NOT NULL,
  recipient_country TEXT NOT NULL,
  sector TEXT NOT NULL,
  sub_sector TEXT,
  modality TEXT NOT NULL,
  amount_usd REAL NOT NULL,
  year INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_filters
ON grants (donor_country, recipient_country, sector, modality, year);
