import streamlit as st

def render_stats(total_makanan, total_provinsi, total_kategori, total_rasa):
    cols = st.columns(4)
    
    with cols[0]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="icon-circle pink-bg">🍲</div>
            <div class="metric-info">
                <h3>{total_makanan}</h3>
                <p>Total Makanan dalam Dataset</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with cols[1]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="icon-circle teal-bg">🗺️</div>
            <div class="metric-info">
                <h3>{total_provinsi}</h3>
                <p>Provinsi di Indonesia</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with cols[2]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="icon-circle green-bg">🗂️</div>
            <div class="metric-info">
                <h3>{total_kategori}</h3>
                <p>Kategori Makanan</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with cols[3]:
        st.markdown(f"""
        <div class="metric-card">
            <div class="icon-circle yellow-bg">😊</div>
            <div class="metric-info">
                <h3>{total_rasa}</h3>
                <p>Jenis Rasa Utama</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
