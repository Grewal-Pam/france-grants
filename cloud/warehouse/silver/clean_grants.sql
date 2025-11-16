CREATE OR REPLACE TABLE
  `france-grants-analytics-478219.france_grants_silver.clean_grants` AS

SELECT
  SAFE_CAST(year AS INT64) AS year,

  -- Donor fields
  donor_code,
  de_donorcode AS donor_iso3,
  LOWER(TRIM(donor_name)) AS donor_name,

  agency_code,
  LOWER(TRIM(agency_name)) AS agency_name,

  -- Project identifiers
  crs_id,
  project_id,
  SAFE_CAST(initial_report AS INT64) AS initial_report,

  -- Recipient fields
  recipient_code,
  de_recipientcode AS recipient_iso3,
  LOWER(TRIM(recipient_name)) AS recipient_name,

  recipient_region_code,
  de_regioncode AS region_code,
  LOWER(TRIM(recipient_region)) AS region_name,

  recipient_income_code,
  de_incomegroupcode AS income_group_code,
  LOWER(TRIM(incomegroup_name)) AS income_group_name,

  -- Flow details
  flow_code,
  LOWER(TRIM(flow_name)) AS flow_name,

  bi_multi,
  category,
  type_of_finance,
  modality,

  -- Financial amounts (convert STRING → FLOAT64)
  SAFE_CAST(usd_commitment AS FLOAT64) AS usd_commitment,
  SAFE_CAST(usd_disbursement AS FLOAT64) AS usd_disbursement,
  SAFE_CAST(usd_received AS FLOAT64) AS usd_received

FROM
  `france-grants-analytics-478219.france_grants_bronze.external_raw_grants`;
