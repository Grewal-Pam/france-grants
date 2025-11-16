CREATE OR REPLACE TABLE
  `france-grants-analytics-478219.france_grants_gold.dim_country` AS

WITH countries AS (
  SELECT DISTINCT
    recipient_iso3 AS iso3,
    recipient_name AS country_name,
    income_group_code,
    region_code
  FROM `france-grants-analytics-478219.france_grants_silver.clean_grants`
  WHERE recipient_iso3 IS NOT NULL

  UNION DISTINCT

  SELECT DISTINCT
    donor_iso3 AS iso3,
    donor_name AS country_name,
    CAST(NULL AS STRING) AS income_group_code,
    CAST(NULL AS STRING) AS region_code
  FROM `france-grants-analytics-478219.france_grants_silver.clean_grants`
  WHERE donor_iso3 IS NOT NULL
)

SELECT * FROM countries;
