CREATE OR REPLACE TABLE
  `france-grants-analytics-478219.france_grants_gold.dim_flow_type` AS

SELECT DISTINCT
  flow_code,
  flow_name,
  modality,
  type_of_finance,
  category
FROM
  `france-grants-analytics-478219.france_grants_silver.clean_grants`;
