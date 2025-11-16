-- Bronze Table (Raw)
CREATE OR REPLACE TABLE `france_grants.bronze_raw_grants` AS
SELECT * FROM `france_grants.external_raw_grants`;

-- Silver Table (Cleaned)
CREATE OR REPLACE TABLE `france_grants.silver_clean_grants` AS
SELECT
  donor_country,
  agency_name,
  recipient_country,
  sector,
  modality,
  amount_usd,
  year
FROM `france_grants.bronze_raw_grants`
WHERE amount_usd >= 0;

-- Gold Table (Analytics)
CREATE OR REPLACE TABLE `france_grants.gold_health_africa` AS
SELECT
  donor_country,
  recipient_country,
  SUM(amount_usd) AS total_amount,
  year
FROM `france_grants.silver_clean_grants`
WHERE recipient_country IN UNNEST(["Kenya","Nigeria","Ghana","Ethiopia","South Africa"])  -- to auto map later
GROUP BY donor_country, recipient_country, year;

--GCP we just make Bronze → Silver → Gold versions.