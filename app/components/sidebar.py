import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.title("Tentang Proyek")
        st.markdown("""
Proyek ini bertujuan untuk membangun sistem pencarian semantik informasi kuliner tradisional Nusantara menggunakan teknologi Semantic Web. Data kuliner yang awalnya disimpan dalam format CSV dikonversi menjadi RDF (Resource Description Framework) dan direpresentasikan menggunakan ontology sehingga dapat diproses menggunakan SPARQL.

Dengan pendekatan ini, informasi kuliner tidak hanya disimpan sebagai data biasa, tetapi juga memiliki hubungan dan makna yang dapat dipahami oleh mesin. Sistem ini diharapkan dapat membantu proses pencarian informasi kuliner berdasarkan berbagai atribut seperti provinsi asal, bahan utama, kategori makanan, dan karakteristik rasa.

### Anggota Kelompok

* **Marchellin Chenika** (140810230002)
* **Audrey Shaina Tjandra** (140810230026)
* **Siti Nailah Eko Putri Alawiyah** (140810230059)
""")
