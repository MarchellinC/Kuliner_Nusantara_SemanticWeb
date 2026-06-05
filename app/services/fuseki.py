import os
import re
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import streamlit as st

FUSEKI_ENDPOINT = "http://localhost:3030/kuliner/query"

def parse_turtle_fallback():
    # Attempt to locate the turtle file relative to this script
    ttl_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "rdf", "kuliner_nusantara.ttl")
    if not os.path.exists(ttl_path):
        return pd.DataFrame()
        
    with open(ttl_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Split content by blocks
    blocks = content.split("\n\n")
    foods = []
    
    for block in blocks:
        if "rdf:type kuliner:Makanan" in block:
            m = re.search(r"kuliner:([a-zA-Z0-9_\-]+)", block)
            if not m:
                continue
            id_name = m.group(1)
            
            nama = re.search(r'kuliner:namaMakanan\s+"([^"]+)"', block)
            provinsi = re.search(r'kuliner:berasalDari\s+"([^"]+)"', block)
            bahan = re.search(r'kuliner:bahanUtama\s+"([^"]+)"', block)
            kategori = re.search(r'kuliner:kategori\s+"([^"]+)"', block)
            rasa = re.search(r'kuliner:rasa\s+"([^"]+)"', block)
            
            foods.append({
                "makanan": f"http://example.org/kuliner/{id_name}",
                "nama": nama.group(1) if nama else id_name.replace("_", " "),
                "provinsi": provinsi.group(1) if provinsi else "N/A",
                "bahanUtama": bahan.group(1) if bahan else "N/A",
                "kategori": kategori.group(1) if kategori else "N/A",
                "rasa": rasa.group(1) if rasa else "N/A"
            })
    return pd.DataFrame(foods)

def run_query(query):
    try:
        sparql = SPARQLWrapper(FUSEKI_ENDPOINT)
        # Timeout after 1.5 seconds to quickly fall back if service is down
        sparql.setTimeout(1.5)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)

        results = sparql.query().convert()

        rows = []
        for result in results["results"]["bindings"]:
            row = {}
            for key, value in result.items():
                row[key] = value["value"]
            rows.append(row)

        return pd.DataFrame(rows)
    except Exception as e:
        # Fallback to local turtle parsing
        df = parse_turtle_fallback()
        if df.empty:
            return pd.DataFrame()
            
        # Handle Stats Query
        if "COUNT(" in query:
            if "totalMakanan" in query:
                return pd.DataFrame([{
                    "totalMakanan": str(len(df)),
                    "totalProvinsi": str(df["provinsi"].nunique()),
                    "totalKategori": str(df["kategori"].nunique()),
                    "totalRasa": str(df["rasa"].nunique())
                }])
            elif "total" in query:
                # Approximate number of triples in turtle file (about 6 triples per food + headers)
                return pd.DataFrame([{"total": str(len(df) * 6 + 12)}])
                
        # Dropdown lists Queries
        if "SELECT DISTINCT ?provinsi" in query:
            return pd.DataFrame({"provinsi": sorted(df["provinsi"].unique())})
            
        if "SELECT DISTINCT ?kategori" in query:
            return pd.DataFrame({"kategori": sorted(df["kategori"].unique())})
            
        if "SELECT DISTINCT ?rasa" in query:
            return pd.DataFrame({"rasa": sorted(df["rasa"].unique())})
            
        if "SELECT DISTINCT ?bahanUtama" in query:
            return pd.DataFrame({"bahanUtama": sorted(df["bahanUtama"].unique())})
            
        # Search queries
        filtered_df = df.copy()
        
        match_prov = re.search(r'kuliner:berasalDari\s+"([^"]+)"', query)
        if match_prov:
            filtered_df = filtered_df[filtered_df["provinsi"] == match_prov.group(1)]
            
        match_cat = re.search(r'kuliner:kategori\s+"([^"]+)"', query)
        if match_cat:
            filtered_df = filtered_df[filtered_df["kategori"] == match_cat.group(1)]
            
        match_rasa = re.search(r'kuliner:rasa\s+"([^"]+)"', query)
        if match_rasa:
            filtered_df = filtered_df[filtered_df["rasa"] == match_rasa.group(1)]
            
        match_bahan = re.search(r'kuliner:bahanUtama\s+"([^"]+)"', query)
        if match_bahan:
            filtered_df = filtered_df[filtered_df["bahanUtama"] == match_bahan.group(1)]
            
        match_regex = re.search(r'FILTER\(regex\(\?nama,\s+"([^"]+)"', query)
        if match_regex:
            kw = match_regex.group(1)
            filtered_df = filtered_df[filtered_df["nama"].str.contains(kw, case=False, na=False)]
            
        return filtered_df