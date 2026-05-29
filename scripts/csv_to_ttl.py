import pandas as pd

# Baca dataset
df = pd.read_csv("../data/raw/dataset makanan.csv")

# Buat file TTL
with open("../data/rdf/kuliner_nusantara.ttl", "w", encoding="utf-8") as f:

    # Prefix
    f.write("@prefix kuliner: <http://example.org/kuliner/> .\n")
    f.write("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n\n")

    # Data
    for _, row in df.iterrows():

        subject = row["Nama Makanan"].replace(" ", "_").replace("-", "_")

        f.write(f"kuliner:{subject}\n")
        f.write("    rdf:type kuliner:Makanan ;\n")
        f.write(f'    kuliner:namaMakanan "{row["Nama Makanan"]}" ;\n')
        f.write(f'    kuliner:berasalDari "{row["Provinsi"]}" ;\n')
        f.write(f'    kuliner:bahanUtama "{row["Bahan Utama"]}" ;\n')
        f.write(f'    kuliner:kategori "{row["Kategori"]}" ;\n')
        f.write(f'    kuliner:rasa "{row["Rasa"]}" .\n\n')

print("File kuliner_nusantara.ttl berhasil dibuat!")