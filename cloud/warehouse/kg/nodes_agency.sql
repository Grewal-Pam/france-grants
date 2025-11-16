CREATE OR REPLACE TABLE
  `france-grants-analytics-478219.france_grants_kg.nodes_agency` AS

SELECT DISTINCT
  agency_code AS node_id,
  agency_name AS name,
  donor AS donor_iso3,
  'Agency' AS node_type
FROM `france-grants-analytics-478219.france_grants_gold.dim_agency`
WHERE agency_code IS NOT NULL;
