import pandas as pd

# Baca dataset
df = pd.read_csv("../data/raw/dataset makanan.csv")

# Bersihkan subject URI
def clean_subject(text):
    return (
        str(text)
        .replace(" ", "_")
        .replace("-", "_")
        .replace("'", "")
        .replace("’", "")
        .replace('"', "")
        .replace("\n", "")
        .replace("\r", "")
    )

# Bersihkan isi literal
def clean_literal(text):
    return (
        str(text)
        .replace("\n", " ")
        .replace("\r", " ")
        .replace('"', '\\"')
        .strip()
    )

# Buat file TTL
with open("../data/rdf/kuliner_nusantara.ttl", "w", encoding="utf-8") as f:

    # Prefix
    f.write("@prefix kuliner: <http://example.org/kuliner/> .\n")
    f.write("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n\n")

    # Data
    for _, row in df.iterrows():

        subject = clean_subject(row["Nama Makanan"])

        nama = clean_literal(row["Nama Makanan"])
        provinsi = clean_literal(row["Provinsi"])
        bahan = clean_literal(row["Bahan Utama"])
        kategori = clean_literal(row["Kategori"])
        rasa = clean_literal(row["Rasa"])

        f.write(f"kuliner:{subject}\n")
        f.write("    rdf:type kuliner:Makanan ;\n")
        f.write(f'    kuliner:namaMakanan "{nama}" ;\n')
        f.write(f'    kuliner:berasalDari "{provinsi}" ;\n')
        f.write(f'    kuliner:bahanUtama "{bahan}" ;\n')
        f.write(f'    kuliner:kategori "{kategori}" ;\n')
        f.write(f'    kuliner:rasa "{rasa}" .\n\n')

print("File kuliner_nusantara.ttl berhasil dibuat!")