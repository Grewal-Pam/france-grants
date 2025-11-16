"""
Generate RDF triples (Turtle format) from KG CSV exports
Aligned with schema.org vocabulary
"""

import pandas as pd

nodes = pd.read_csv("kg/nodes.csv")
edges = pd.read_csv("kg/edges.csv")

def uri(x):
    safe = str(x).replace(" ", "_")  # ensure URI-safe
    return f"<http://example.org/entity/{safe}>"

with open("kg/graph.ttl", "w") as f:
    # Prefixes
    f.write("@prefix schema: <https://schema.org/> .\n")
    f.write("@prefix ex: <http://example.org/> .\n\n")

    # ---------------------
    # Nodes (Entities)
    # ---------------------
    for _, row in nodes.iterrows():
        subj = uri(row["id"])

        # Map type dynamically (very light semantics)
        rdf_type = "schema:Grant" if "grant" in str(row["type"]).lower() else "schema:Place"
        f.write(f"{subj} a {rdf_type} .\n")

        # Africa flag
        if "is_africa" in row and row["is_africa"] == True:
            f.write(f"{subj} schema:location <http://example.org/region/Africa> .\n")

        f.write("\n")

    # ---------------------
    # Edges (Relations)
    # ---------------------
    for _, row in edges.iterrows():
        s = uri(row["source"])
        o = uri(row["target"])

        # convert relation into a schema.org property format
        pred = f"schema:{str(row['relation']).replace(' ', '_')}"

        f.write(f"{s} {pred} {o} .\n")
