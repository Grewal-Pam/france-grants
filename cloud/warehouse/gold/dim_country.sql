CREATE OR REPLACE TABLE
  `france-grants-analytics-478219.france_grants_gold.dim_country` AS

WITH base AS (
  -- RECIPIENT COUNTRIES
  SELECT
    recipient_iso3 AS iso3,
    recipient_name AS country_name,
    income_group_code,
    region_code
  FROM `france-grants-analytics-478219.france_grants_silver.clean_grants`
  WHERE recipient_iso3 IS NOT NULL

  UNION DISTINCT

  -- DONOR COUNTRIES (no income/region available)
  SELECT
    donor_iso3 AS iso3,
    donor_name AS country_name,
    NULL AS income_group_code,
    NULL AS region_code
  FROM `france-grants-analytics-478219.france_grants_silver.clean_grants`
  WHERE donor_iso3 IS NOT NULL
)

SELECT
  iso3,
  -- pick a stable country name if multiple exist
  ANY_VALUE(country_name) AS country_name,
  ANY_VALUE(income_group_code) AS income_group_code,
  ANY_VALUE(region_code) AS region_code
FROM base
GROUP BY iso3;
