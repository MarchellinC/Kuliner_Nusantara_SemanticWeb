import streamlit as st
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON

# Configuration & Custom CSS
st.set_page_config(
    page_title="Kuliner Nusantara Semantic Search",
    page_icon="🍲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium CSS Styling
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Main Title Styling */
    .main-title {
        background: -webkit-linear-gradient(45deg, #FF6B6B, #FF8E53, #FFA73D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 0px !important;
        padding-bottom: 0px !important;
        text-align: center;
    }
    
    .sub-title {
        text-align: center;
        color: #888;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    /* Card Styling */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    /* Metrics/Info Box */
    .info-box {
        background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        border: 1px solid #333;
        transition: transform 0.3s ease;
    }
    .info-box:hover {
        transform: translateY(-5px);
    }
    
    .info-box h3 {
        color: #FFA73D;
        margin: 0;
        font-size: 1.2rem;
    }
    .info-box p {
        color: #fff;
        font-size: 2rem;
        font-weight: bold;
        margin: 10px 0 0 0;
    }
    
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(90deg, #FF6B6B, #FFA73D);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(255,107,107,0.4);
    }
</style>
""", unsafe_allow_html=True)


# SPARQL Configuration
FUSEKI_URL = "http://localhost:3030/kuliner/query"

@st.cache_data(ttl=300)
def execute_sparql(query):
    """Fungsi untuk mengeksekusi query SPARQL dan mengembalikan pandas DataFrame"""
    try:
        sparql = SPARQLWrapper(FUSEKI_URL)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        
        # Konversi hasil ke format list of dict
        data = []
        for result in results["results"]["bindings"]:
            row = {}
            for key in result.keys():
                row[key] = result[key]["value"]
            data.append(row)
            
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error saat menghubungi endpoint SPARQL: {e}")
        return pd.DataFrame()

# Helper Queries to Get Filter Options
@st.cache_data(ttl=600)
def get_options(property_name):
    query = f"""
    PREFIX kuliner: <http://example.org/kuliner/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
    SELECT DISTINCT ?value
    WHERE {{
      ?makanan rdf:type kuliner:Makanan .
      ?makanan kuliner:{property_name} ?value .
    }}
    ORDER BY ?value
    """
    df = execute_sparql(query)
    if not df.empty and 'value' in df.columns:
        return ["Semua"] + df['value'].tolist()
    return ["Semua"]

# Main UI
def main():
    st.markdown('<p class="main-title">🍲 Kuliner Nusantara</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Sistem Pencarian Semantik Kuliner Tradisional Nusantara (RDF & SPARQL)</p>', unsafe_allow_html=True)

    # Memuat opsi filter dari endpoint
    with st.spinner("Memuat filter data dari Fuseki..."):
        provinsi_opts = get_options("berasalDari")
        kategori_opts = get_options("kategori")
        rasa_opts = get_options("rasa")

    # Layout Sidebar untuk Pencarian
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3081/3081162.png", width=100)
        st.markdown("### 🔍 Filter Pencarian")
        
        search_nama = st.text_input("Nama Makanan", placeholder="Contoh: Sate, Nasi...")
        
        search_provinsi = st.selectbox("Provinsi Asal", provinsi_opts)
        search_kategori = st.selectbox("Kategori", kategori_opts)
        search_rasa = st.selectbox("Karakteristik Rasa", rasa_opts)
        search_bahan = st.text_input("Bahan Utama", placeholder="Contoh: Daging, Beras...")
        
        btn_search = st.button("Cari Kuliner")

    # Dynamic Query Generation
    filters = []
    
    if search_nama:
        filters.append(f'FILTER(CONTAINS(LCASE(?nama), LCASE("{search_nama}")))')
    
    if search_provinsi != "Semua":
        filters.append(f'?makanan kuliner:berasalDari "{search_provinsi}" .')
    
    if search_kategori != "Semua":
        filters.append(f'?makanan kuliner:kategori "{search_kategori}" .')
        
    if search_rasa != "Semua":
        filters.append(f'?makanan kuliner:rasa "{search_rasa}" .')
        
    if search_bahan:
        filters.append(f'FILTER(CONTAINS(LCASE(?bahan), LCASE("{search_bahan}")))')

    # Menyatukan filter
    filter_string = "\n      ".join(filters)
    
    # Query Utama
    main_query = f"""
    PREFIX kuliner: <http://example.org/kuliner/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    
    SELECT ?nama ?provinsi ?kategori ?bahan ?rasa
    WHERE {{
      ?makanan rdf:type kuliner:Makanan .
      ?makanan kuliner:namaMakanan ?nama .
      ?makanan kuliner:berasalDari ?provinsi .
      ?makanan kuliner:kategori ?kategori .
      ?makanan kuliner:bahanUtama ?bahan .
      ?makanan kuliner:rasa ?rasa .
      
      {filter_string}
    }}
    ORDER BY ?nama
    """

    # Saat awal atau saat tombol ditekan
    if not filter_string and not btn_search:
        # Tampilkan beberapa data awal
        st.info("👋 Selamat datang! Silakan gunakan filter di menu samping untuk mencari kuliner, atau lihat daftar lengkap di bawah ini.")
    
    if btn_search or True:
        with st.spinner("Mencari data ke Apache Jena Fuseki..."):
            df_results = execute_sparql(main_query)
            
            if not df_results.empty:
                # Kolom informasi
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f'''
                    <div class="info-box">
                        <h3>Total Hasil</h3>
                        <p>{len(df_results)}</p>
                    </div>
                    ''', unsafe_allow_html=True)
                
                # Mengubah nama kolom
                df_results.rename(columns={
                    'nama': 'Nama Makanan',
                    'provinsi': 'Provinsi Asal',
                    'kategori': 'Kategori',
                    'bahan': 'Bahan Utama',
                    'rasa': 'Karakteristik Rasa'
                }, inplace=True, errors='ignore')
                
                st.markdown("### 📋 Hasil Pencarian")
                st.dataframe(
                    df_results,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.warning("Data tidak ditemukan. Coba gunakan filter pencarian yang berbeda atau pastikan Apache Jena Fuseki sedang berjalan.")

    # Menampilkan Raw Query
    with st.expander("🛠️ Lihat Query SPARQL (Raw)"):
        st.code(main_query, language="sparql")
        st.markdown(f"**Endpoint Tujuan:** `{FUSEKI_URL}`")
        st.info("Pastikan Anda sudah menjalankan Fuseki Server dan memiliki dataset di endpoint tersebut.")

if __name__ == "__main__":
    main()
