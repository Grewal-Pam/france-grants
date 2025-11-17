CREATE OR REPLACE TABLE
  `france-grants-analytics-478219.france_grants_gold.dim_income_group` AS

SELECT DISTINCT
  income_group_code,
  income_group_name
FROM
  `france-grants-analytics-478219.france_grants_silver.clean_grants`;
