CREATE OR REPLACE TABLE
  `france-grants-analytics-478219.france_grants_kg.nodes_flow_type` AS

SELECT DISTINCT
  flow_code AS node_id,
  flow_name AS name,
  modality,
  type_of_finance,
  category,
  'FlowType' AS node_type
FROM `france-grants-analytics-478219.france_grants_gold.dim_flow_type`;
