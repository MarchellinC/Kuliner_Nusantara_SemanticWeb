import streamlit as st

def render_filters(provinces, categories, rasas, bahan_utamas):
    st.markdown("""
    <div style="margin-top: 1rem; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 10px;">
        <span style="font-size: 1.5rem; color: #475569;">🔍</span>
        <h3 style="margin: 0; color: #1e293b; font-weight: 600; font-size: 1.25rem;">Cari Makanan</h3>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        selected_province = st.selectbox(
            "Pilih Provinsi",
            ["Semua Provinsi"] + provinces,
            key="filter_provinsi"
        )
        
    with c2:
        selected_category = st.selectbox(
            "Pilih Kategori",
            ["Semua Kategori"] + categories,
            key="filter_kategori"
        )
        
    with c3:
        selected_rasa = st.selectbox(
            "Pilih Rasa",
            ["Semua Rasa"] + rasas,
            key="filter_rasa"
        )
        
    with c4:
        selected_bahan = st.selectbox(
            "Pilih Bahan Utama",
            ["Semua Bahan"] + bahan_utamas,
            key="filter_bahan"
        )
        
    bc1, bc2, bc3 = st.columns([1, 1, 4])
    
    with bc1:
        search_clicked = st.button("Cari", use_container_width=True, type="primary")
        
    with bc2:
        reset_clicked = st.button("Reset", use_container_width=True)
        
    with bc3:
        st.markdown("""
        <div class="info-banner">
            <span style="font-size: 1.1rem; margin-right: 5px;">💡</span>
            Gunakan filter di atas untuk menemukan makanan khas sesuai preferensi Anda.
        </div>
        """, unsafe_allow_html=True)
        
    return selected_province, selected_category, selected_rasa, selected_bahan, search_clicked, reset_clicked
