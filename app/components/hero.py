import streamlit as st

def render_hero():
    st.markdown("""
    <div class="hero-container">
        <p class="hero-sub">Selamat Datang di</p>
        <h1 class="hero-title">Kuliner <span class="highlight">Nusantara</span></h1>
        <p class="hero-desc">Jelajahi kekayaan kuliner dari seluruh provinsi di Indonesia.</p>
    </div>
    """, unsafe_allow_html=True)
