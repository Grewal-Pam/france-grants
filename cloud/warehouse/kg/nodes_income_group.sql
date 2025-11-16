CREATE OR REPLACE TABLE
  `france-grants-analytics-478219.france_grants_kg.nodes_income_group` AS

SELECT DISTINCT
  income_group_code AS node_id,
  income_group_name AS name,
  'IncomeGroup' AS node_type
FROM `france-grants-analytics-478219.france_grants_gold.dim_income_group`
WHERE income_group_code IS NOT NULL;
