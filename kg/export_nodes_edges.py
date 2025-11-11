import sqlite3
import pandas as pd
from src.utils.africa import AFRICA

# Load DB
conn = sqlite3.connect("grants.db")
df = pd.read_sql("SELECT * FROM grants", conn)

# Semantic flags
df["is_africa"] = df["recipient_country"].isin(AFRICA)
df["is_health"] = df["sector"].str.contains("Health", case=False, na=False)

# Nodes
countries = pd.DataFrame({
    "id": df["recipient_country"].unique(),
    "type": "recipient_country"
})
countries["is_africa"] = countries["id"].isin(AFRICA)

donor = pd.DataFrame({
    "id": df["donor_country"].unique(),
    "type": "donor_country"
})

agencies = pd.DataFrame({
    "id": df["agency_name"].unique(),
    "type": "agency"
})

sectors = pd.DataFrame({
    "id": df["sector"].unique(),
    "type": "sector"
})

nodes = pd.concat([countries, donor, agencies, sectors], ignore_index=True).drop_duplicates()

# Edges: Donor -> Agency
edges_donor_agency = df[["donor_country", "agency_name"]].drop_duplicates()
edges_donor_agency.columns = ["source", "target"]
edges_donor_agency["relation"] = "funds_through"

# Edges: Agency -> Recipient
edges_agency_recipient = df[["agency_name", "recipient_country"]].drop_duplicates()
edges_agency_recipient.columns = ["source", "target"]
edges_agency_recipient["relation"] = "funds_to"

# Edges: Agency -> Sector
edges_agency_sector = df[["agency_name", "sector"]].drop_duplicates()
edges_agency_sector.columns = ["source", "target"]
edges_agency_sector["relation"] = "supports_sector"

edges = pd.concat([
    edges_donor_agency,
    edges_agency_recipient,
    edges_agency_sector
], ignore_index=True)

# Filter for health grants to Africa
health_africa_df = df[df["is_africa"] & df["is_health"]]

edges_health_africa = health_africa_df[["agency_name", "recipient_country"]].drop_duplicates()
edges_health_africa.columns = ["source", "target"]
edges_health_africa["relation"] = "funds_health_in_africa"

# Save outputs
nodes.to_csv("kg/nodes.csv", index=False)
edges.to_csv("kg/edges.csv", index=False)
edges_health_africa.to_csv("kg/edges_health_africa.csv", index=False)

print("✅ KG Export Complete:")
print("   - nodes.csv")
print("   - edges.csv")
print("   - edges_health_africa.csv")
