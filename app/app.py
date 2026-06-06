import streamlit as st
import pandas as pd
from services.fuseki import run_query
from services.sparql import (
    get_all_provinces,
    get_all_categories,
    get_all_rasa,
    get_all_bahan_utama,
    search_foods
)
from components.sidebar import render_sidebar
from components.hero import render_hero
from components.filters import render_filters
from components.result_cards import render_food_cards
from components.detail_panel import render_detail_panel
from components.knowledge_graph import render_knowledge_graph

# Set page config
st.set_page_config(
    page_title="Kuliner Nusantara",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS styles
try:
    with open("app/assets/styles.css", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )
except Exception as e:
    st.error(f"Gagal memuat CSS: {e}")

# Fetch filter lists
provinces = []
categories = []
rasas = []
bahan_utamas = []

prov_df = run_query(get_all_provinces())
if not prov_df.empty and "provinsi" in prov_df.columns:
    provinces = prov_df["provinsi"].tolist()

cat_df = run_query(get_all_categories())
if not cat_df.empty and "kategori" in cat_df.columns:
    categories = cat_df["kategori"].tolist()

rasa_df = run_query(get_all_rasa())
if not rasa_df.empty and "rasa" in rasa_df.columns:
    rasas = rasa_df["rasa"].tolist()

bahan_df = run_query(get_all_bahan_utama())
if not bahan_df.empty and "bahanUtama" in bahan_df.columns:
    bahan_utamas = bahan_df["bahanUtama"].tolist()

# Initialize session states
if "search_results" not in st.session_state:
    st.session_state.search_results = run_query(search_foods())

if "selected_food_details" not in st.session_state:
    st.session_state.selected_food_details = None

# Render Sidebar (Tentang Proyek and Mode Gelap only)
render_sidebar()

# Main page layout container wrapper
st.markdown('<div class="main-content-wrapper">', unsafe_allow_html=True)

# Render Hero header
render_hero()

# Render filter controls
search_keyword, selected_province, selected_category, selected_rasa, selected_bahan, search_clicked, reset_clicked = render_filters(
    provinces, categories, rasas, bahan_utamas
)

# Handle Search interaction
if search_clicked:
    st.session_state.search_results = run_query(
        search_foods(
            provinsi=selected_province,
            kategori=selected_category,
            rasa=selected_rasa,
            bahan_utama=selected_bahan,
            keyword=search_keyword
        )
    )
    st.session_state.current_page = 1
    st.session_state.selected_food_details = None
    st.rerun()

# Handle Reset interaction
if reset_clicked:
    st.session_state.search_results = run_query(search_foods())
    st.session_state.current_page = 1
    st.session_state.selected_food_details = None
    st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# Bottom search results and details split layout
col1, col2 = st.columns([7, 5], gap="large")

with col1:
    render_food_cards(st.session_state.search_results)

with col2:
    render_detail_panel(st.session_state.selected_food_details)
    render_knowledge_graph(st.session_state.selected_food_details)

st.markdown('</div>', unsafe_allow_html=True)
