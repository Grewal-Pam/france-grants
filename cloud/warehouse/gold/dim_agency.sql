CREATE OR REPLACE TABLE
  `france-grants-analytics-478219.france_grants_gold.dim_agency` AS

SELECT DISTINCT
  agency_code,
  agency_name,
  donor_iso3 AS donor
FROM
  `france-grants-analytics-478219.france_grants_silver.clean_grants`
WHERE agency_code IS NOT NULL;
