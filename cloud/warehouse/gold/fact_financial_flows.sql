CREATE OR REPLACE TABLE
  `france-grants-analytics-478219.france_grants_gold.fact_financial_flows` AS

SELECT
  -- Keys
  donor_iso3 AS donor,
  recipient_iso3 AS recipient,
  agency_code AS agency,
  flow_code AS flow_type,
  type_of_finance,
  category,
  
  -- Measures
  SAFE_CAST(usd_commitment AS FLOAT64) AS usd_commitment,
  SAFE_CAST(usd_disbursement AS FLOAT64) AS usd_disbursement,
  SAFE_CAST(usd_received AS FLOAT64) AS usd_received,

  -- Time
  SAFE_CAST(year AS INT64) AS year,

  -- Useful attributes
  income_group_code AS income_group,
  region_code AS region,

FROM
  `france-grants-analytics-478219.france_grants_silver.clean_grants`;
