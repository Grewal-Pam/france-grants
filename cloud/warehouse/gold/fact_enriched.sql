CREATE OR REPLACE TABLE
  `france-grants-analytics-478219.france_grants_gold.fact_enriched` AS

SELECT
  --  COUNTRY INFO (Recipient + Donor for mapping)
  f.recipient AS recipient_iso3,
  rc.country_name AS recipient_country,
  f.donor AS donor_iso3,
  dc.country_name AS donor_country,

  -- AGENCY INFO
  f.agency AS agency_code,
  da.agency_name,

  --  FLOW TYPE INFO
  f.flow_type AS flow_code,
  dft.flow_name,
  dft.type_of_finance,
  dft.category,

  --  MEASURES
  f.usd_commitment,
  f.usd_disbursement,
  f.usd_received,

  -- TIME
  f.year,

  --  ATTRIBUTES (HUMAN-READABLE)
  f.region,
  f.income_group AS income_group_code,
  dig.income_group_name

FROM `france-grants-analytics-478219.france_grants_gold.fact_financial_flows` f

--  Recipient country join
LEFT JOIN `france-grants-analytics-478219.france_grants_gold.dim_country` rc
  ON f.recipient = rc.iso3

--  Donor country join
LEFT JOIN `france-grants-analytics-478219.france_grants_gold.dim_country` dc
  ON f.donor = dc.iso3

--  Agency join
LEFT JOIN `france-grants-analytics-478219.france_grants_gold.dim_agency` da
  ON f.agency = da.agency_code

-- Flow type join
LEFT JOIN `france-grants-analytics-478219.france_grants_gold.dim_flow_type` dft
  ON f.flow_type = dft.flow_code

--  Income group name join
LEFT JOIN `france-grants-analytics-478219.france_grants_gold.dim_income_group` dig
  ON f.income_group = dig.income_group_code;
