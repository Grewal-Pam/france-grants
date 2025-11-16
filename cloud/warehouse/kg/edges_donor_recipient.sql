CREATE OR REPLACE TABLE
  `france-grants-analytics-478219.france_grants_kg.edges_donor_recipient` AS

SELECT
  donor AS source_id,
  recipient AS target_id,
  'FUNDS' AS relationship_type,
  SAFE_CAST(usd_disbursement AS FLOAT64) AS amount,
  year
FROM `france-grants-analytics-478219.france_grants_gold.fact_financial_flows`
WHERE donor IS NOT NULL
  AND recipient IS NOT NULL;
