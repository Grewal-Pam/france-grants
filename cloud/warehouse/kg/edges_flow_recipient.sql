CREATE OR REPLACE TABLE
  `france-grants-analytics-478219.france_grants_kg.edges_flow_recipient` AS

SELECT DISTINCT
  flow_type AS source_id,
  recipient AS target_id,
  'FLOW_TYPE_APPLIED_TO' AS relationship_type
FROM `france-grants-analytics-478219.france_grants_gold.fact_financial_flows`
WHERE flow_type IS NOT NULL
  AND recipient IS NOT NULL;
