import streamlit as st

def render_sidebar():
    with st.sidebar:
        # Logo and Title
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem; padding: 10px;">
            <div style="font-size: 3rem; margin-bottom: -5px;">🍲</div>
            <div style="font-size: 1.6rem; font-weight: 700; color: #1e293b; display: inline-block;">
                Kuliner <span style="color: #ec4899;">Nusantara</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation Menu List
        st.markdown("""
        <div class="sidebar-menu">
            <div class="menu-item active">
                <span class="icon">🏠</span> <span class="text">Beranda</span>
            </div>
            <div class="menu-item">
                <span class="icon">🔍</span> <span class="text">Cari Makanan</span>
            </div>
            <div class="menu-item">
                <span class="icon">🗺️</span> <span class="text">Jelajahi Provinsi</span>
            </div>
            <div class="menu-item">
                <span class="icon">🗂️</span> <span class="text">Kategori</span>
            </div>
            <div class="menu-item">
                <span class="icon">😊</span> <span class="text">Rasa</span>
            </div>
            <div class="menu-item">
                <span class="icon">🍃</span> <span class="text">Bahan Utama</span>
            </div>
            <div class="menu-item">
                <span class="icon">ℹ️</span> <span class="text">Tentang Proyek</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # About Project Card
        st.markdown("""
        <div class="about-card" style="background: rgba(255, 255, 255, 0.5); border-radius: 16px; padding: 15px; margin-bottom: 1rem; border: 1px solid rgba(255,255,255,0.6);">
            <h4 style="margin-top: 0; color: #334155; font-size: 0.95rem;">Tentang Proyek</h4>
            <p style="font-size: 0.8rem; color: #475569; line-height: 1.4;">
                Aplikasi ini dibangun menggunakan teknologi Semantic Web (RDF, OWL, SPARQL) dengan data kuliner nusantara.
            </p>
            <div style="font-size: 1.2rem; color: #ec4899;">💖</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Mode Gelap Toggle (Visual representation)
        st.toggle("Mode Gelap", value=False, key="dark_mode")
