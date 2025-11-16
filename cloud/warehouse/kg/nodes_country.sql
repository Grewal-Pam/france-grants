CREATE OR REPLACE TABLE
  `france-grants-analytics-478219.france_grants_kg.nodes_country` AS

SELECT DISTINCT
  iso3 AS node_id,
  country_name AS name,
  income_group_code,
  region_code,
  'Country' AS node_type
FROM `france-grants-analytics-478219.france_grants_gold.dim_country`
WHERE iso3 IS NOT NULL;
