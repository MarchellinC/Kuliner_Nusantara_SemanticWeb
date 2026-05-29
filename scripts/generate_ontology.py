with open("../data/ontology/kuliner_ontology.ttl", "w", encoding="utf-8") as f:

    # Prefix
    f.write("@prefix kuliner: <http://example.org/kuliner/> .\n")
    f.write("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n")
    f.write("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n")
    f.write("@prefix owl: <http://www.w3.org/2002/07/owl#> .\n\n")

    # Ontology
    f.write("kuliner:KulinerOntology rdf:type owl:Ontology .\n\n")

    # Classes
    f.write("# ==========================\n")
    f.write("# Classes\n")
    f.write("# ==========================\n\n")

    f.write("""
    kuliner:Makanan rdf:type owl:Class ;
        rdfs:label "Makanan" .

    kuliner:Provinsi rdf:type owl:Class ;
        rdfs:label "Provinsi" .

    kuliner:BahanUtama rdf:type owl:Class ;
        rdfs:label "Bahan Utama" .

    kuliner:Kategori rdf:type owl:Class ;
        rdfs:label "Kategori" .

    kuliner:Rasa rdf:type owl:Class ;
        rdfs:label "Rasa" .

    """)

    # Datatype Properties
    f.write("\n# ==========================\n")
    f.write("# Datatype Properties\n")
    f.write("# ==========================\n\n")
    f.write("""
    kuliner:namaMakanan rdf:type owl:DatatypeProperty ;
        rdfs:label "Nama Makanan" ;
        rdfs:domain kuliner:Makanan ;
        rdfs:range rdfs:Literal .

    kuliner:berasalDari rdf:type owl:DatatypeProperty ;
        rdfs:label "Berasal Dari" ;
        rdfs:domain kuliner:Makanan ;
        rdfs:range rdfs:Literal .

    kuliner:bahanUtama rdf:type owl:DatatypeProperty ;
        rdfs:label "Bahan Utama" ;
        rdfs:domain kuliner:Makanan ;
        rdfs:range rdfs:Literal .

    kuliner:kategori rdf:type owl:DatatypeProperty ;
        rdfs:label "Kategori" ;
        rdfs:domain kuliner:Makanan ;
        rdfs:range rdfs:Literal .

    kuliner:rasa rdf:type owl:DatatypeProperty ;
        rdfs:label "Rasa" ;
        rdfs:domain kuliner:Makanan ;
        rdfs:range rdfs:Literal .

    """)

print("Ontology berhasil dibuat!")