CREATE OR REPLACE TABLE
  `france-grants-analytics-478219.france_grants_kg.edges_donor_agency` AS

SELECT DISTINCT
  donor AS source_id,
  agency AS target_id,
  'FUNDS_THROUGH_AGENCY' AS relationship_type
FROM `france-grants-analytics-478219.france_grants_gold.fact_financial_flows`
WHERE donor IS NOT NULL
  AND agency IS NOT NULL;
