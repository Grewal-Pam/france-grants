import unicodedata

# Canonical entities -> list of variants in data
ENTITY_CANONICALS = {
    "French Ministry of Foreign Affairs (MAE)": [
        "COOP DECENTRAL/MAE",
        "MAE",
        "Coop decentral/MAE"
    ],
    "French Ministry of Interior": [
        "Ministry of Interior"
    ],
    "French Ministry of Education & Research": [
        "Ministry of Education, Higher education and Research",
        "Ministry of Education and Research"
    ],
    "French Interministerial Agencies": [
        "Interdepartmental",
        "Interministerial",
        "Inter-departmental"
    ],
    "Local Government (France)": [
        "Local Government",
        "Gouvernment local", # typo in data
        "Gouvernement local"
    ],
    "Central Government (France)": [
        "Central Government",
        "Gouvernement central"
    ],
    "Other Public Agencies (France)": [
        "Autre entité publique dans le pays donneur"
    ],
    "Donor Country NGO": [
        "Donor country-based NGO",
        "ONG basée dans un pays donneur"
    ]
}

# --- TEXT NORMALIZATION HELPER ----
def normalize(x: str) -> str:
    if not x:
        return ""
    x = unicodedata.normalize("NFKD", x)
    x = "".join(c for c in x if not unicodedata.combining(c))
    x = x.lower()
    x = x.replace(",", "").replace(".", "").replace("/", " ").strip()
    return x

# --- RESOLVER FUNCTION ---
def resolve_entity(name: str) -> str:
    if not name:
        return None

    clean = normalize(name)

    for canonical, variants in ENTITY_CANONICALS.items():
        for v in variants:
            if normalize(v) == clean:
                return canonical

    # fallback: return original, capitalized a bit
    return name.strip()
