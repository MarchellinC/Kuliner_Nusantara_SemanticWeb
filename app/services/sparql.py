PREFIX = """
PREFIX kuliner: <http://example.org/kuliner/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
"""
def get_all_provinces():
    return PREFIX + """
    SELECT DISTINCT ?provinsi
    WHERE {
        ?makanan kuliner:berasalDari ?provinsi .
    }
    ORDER BY ?provinsi
    """

def get_all_categories():
    return PREFIX + """
    SELECT DISTINCT ?kategori
    WHERE {
        ?makanan kuliner:kategori ?kategori .
    }
    ORDER BY ?kategori
    """

def get_all_rasa():
    return PREFIX + """
    SELECT DISTINCT ?rasa
    WHERE {
        ?makanan kuliner:rasa ?rasa .
    }
    ORDER BY ?rasa
    """

def get_all_bahan_utama():
    return PREFIX + """
    SELECT DISTINCT ?bahanUtama
    WHERE {
        ?makanan kuliner:bahanUtama ?bahanUtama .
    }
    ORDER BY ?bahanUtama
    """

def search_foods(provinsi=None, kategori=None, rasa=None, bahan_utama=None, keyword=None):
    conditions = []
    
    # Always match basic fields
    conditions.append("?makanan rdf:type kuliner:Makanan .")
    conditions.append("?makanan kuliner:namaMakanan ?nama .")
    
    if provinsi and provinsi != "Semua Provinsi":
        conditions.append(f'?makanan kuliner:berasalDari "{provinsi}" .')
        conditions.append(f'BIND("{provinsi}" AS ?provinsi)')
    else:
        conditions.append('?makanan kuliner:berasalDari ?provinsi .')

    if kategori and kategori != "Semua Kategori":
        conditions.append(f'?makanan kuliner:kategori "{kategori}" .')
        conditions.append(f'BIND("{kategori}" AS ?kategori)')
    else:
        conditions.append('?makanan kuliner:kategori ?kategori .')

    if rasa and rasa != "Semua Rasa":
        conditions.append(f'?makanan kuliner:rasa "{rasa}" .')
        conditions.append(f'BIND("{rasa}" AS ?rasa)')
    else:
        conditions.append('?makanan kuliner:rasa ?rasa .')

    if bahan_utama and bahan_utama != "Semua Bahan":
        conditions.append(f'?makanan kuliner:bahanUtama "{bahan_utama}" .')
        conditions.append(f'BIND("{bahan_utama}" AS ?bahanUtama)')
    else:
        conditions.append('?makanan kuliner:bahanUtama ?bahanUtama .')

    if keyword:
        conditions.append(f'FILTER(regex(?nama, "{keyword}", "i"))')

    where_clause = "\n        ".join(conditions)
    return PREFIX + f"""
    SELECT DISTINCT ?makanan ?nama ?provinsi ?kategori ?rasa ?bahanUtama
    WHERE {{
        {where_clause}
    }}
    ORDER BY ?nama
    """

def get_stats():
    return PREFIX + """
    SELECT 
      (COUNT(DISTINCT ?makanan) as ?totalMakanan)
      (COUNT(DISTINCT ?provinsi) as ?totalProvinsi)
      (COUNT(DISTINCT ?kategori) as ?totalKategori)
      (COUNT(DISTINCT ?rasa) as ?totalRasa)
    WHERE {
      ?makanan rdf:type kuliner:Makanan .
      OPTIONAL { ?makanan kuliner:berasalDari ?provinsi }
      OPTIONAL { ?makanan kuliner:kategori ?kategori }
      OPTIONAL { ?makanan kuliner:rasa ?rasa }
    }
    """

def get_total_triples():
    return """
    SELECT (COUNT(*) as ?total)
    WHERE {
        ?s ?p ?o
    }
    """