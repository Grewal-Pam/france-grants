CREATE OR REPLACE TABLE
  `france-grants-analytics-478219.france_grants_kg.edges_agency_recipient` AS

SELECT DISTINCT
  agency AS source_id,
  recipient AS target_id,
  'IMPLEMENTS_PROJECT_IN' AS relationship_type
FROM `france-grants-analytics-478219.france_grants_gold.fact_financial_flows`
WHERE agency IS NOT NULL
  AND recipient IS NOT NULL;
