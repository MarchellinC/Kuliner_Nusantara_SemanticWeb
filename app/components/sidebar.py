import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <h1 style="font-weight:800;font-size:1.8rem;">Tentang Proyek</h1>

        <hr>

        <h3>Sistem Pencarian Semantik Kuliner Tradisional Nusantara Berbasis RDF dan SPARQL</h3>

        <div style="text-align: justify;">
        Proyek ini bertujuan untuk membangun sistem pencarian semantik informasi kuliner tradisional Nusantara menggunakan teknologi Semantic Web. Data kuliner yang awalnya disimpan dalam format CSV dikonversi menjadi RDF (Resource Description Framework) dan direpresentasikan menggunakan ontology sehingga dapat diproses menggunakan SPARQL.

        <br><br>

        Dengan pendekatan ini, informasi kuliner tidak hanya disimpan sebagai data biasa, tetapi juga memiliki hubungan dan makna yang dapat dipahami oleh mesin. Sistem ini diharapkan dapat membantu proses pencarian informasi kuliner berdasarkan berbagai atribut seperti provinsi asal, bahan utama, kategori makanan, dan karakteristik rasa.
        </div>

        <hr>

        <h3>Tujuan</h3>

        <div style="text-align: justify;">
        <ul>
            <li>Mengubah dataset kuliner tradisional Nusantara dari format CSV ke RDF Turtle (.ttl).</li>
            <li>Membangun ontology untuk merepresentasikan konsep dan hubungan dalam domain kuliner.</li>
            <li>Menghasilkan representasi ontology dalam format RDF/XML.</li>
            <li>Menyimpan dan mengelola data RDF menggunakan Apache Jena Fuseki.</li>
            <li>Menyediakan fasilitas pencarian informasi menggunakan query SPARQL.</li>
        </ul>
        </div>

        <hr>

        <h3>Anggota Kelompok</h3>

        <ul>
            <li><b>Marchellin Chenika</b> (140810230002)</li>
            <li><b>Audrey Shaina Tjandra</b> (140810230026)</li>
            <li><b>Siti Nailah Eko Putri Alawiyah</b> (140810230059)</li>
        </ul>
        """, unsafe_allow_html=True)