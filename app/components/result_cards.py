import streamlit as st

def render_food_cards(df, page_size=10):
    if df is None or df.empty:
        st.markdown("""
        <div style="text-align: center; padding: 40px; color: #64748b;">
            <span style="font-size: 3rem; display: block; margin-bottom: 10px;">🍲</span>
            Tidak ada kuliner yang ditemukan. Coba ubah filter pencarian Anda.
        </div>
        """, unsafe_allow_html=True)
        return

    total_results = len(df)
    
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
        <h3 style="margin: 0; color: #1e293b; font-size: 1.25rem; font-weight: 600;">Hasil Pencarian</h3>
        <span class="count-badge">{total_results} hasil ditemukan</span>
    </div>
    """, unsafe_allow_html=True)

    # Initialize current page
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 1

    total_pages = (total_results + page_size - 1) // page_size
    if st.session_state.current_page > total_pages:
        st.session_state.current_page = max(1, total_pages)

    start_idx = (st.session_state.current_page - 1) * page_size
    end_idx = min(start_idx + page_size, total_results)
    
    page_items = df.iloc[start_idx:end_idx]

    # Render each food card item entirely within one HTML structure to prevent layout breaks
    for i, (_, row) in enumerate(page_items.iterrows(), start=start_idx + 1):
        uri = row["makanan"]
        name = row.get("nama") or uri.split("/")[-1].replace("_", " ")
        prov = row.get("provinsi", "N/A")
        cat = row.get("kategori", "N/A")
        rasa = row.get("rasa", "N/A")
        
        st.markdown(f"""
        <div class="search-item-card">
            <div class="card-left">
                <span class="index-num-box">{i}</span>
            </div>
            <div class="card-right">
                <a class="food-title-link" href="?select_food={uri}" target="_self">{name}</a>
                <div class="food-meta-row">
                    <div style="display: flex; gap: 8px;">
                        <span class="tag-badge cat-tag">{cat}</span>
                        <span class="tag-badge taste-tag">{rasa}</span>
                    </div>
                    <div class="loc-text">
                        📌 {prov}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Render Pagination controls using columns
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    p_cols = st.columns([1, 3, 1])
    
    with p_cols[0]:
        if st.session_state.current_page > 1:
            if st.button("◀", key="prev_page", use_container_width=True):
                st.session_state.current_page -= 1
                st.rerun()
                
    with p_cols[1]:
        st.markdown(f"""
        <div class="pagination-info">
            Halaman {st.session_state.current_page} dari {total_pages}
        </div>
        """, unsafe_allow_html=True)
        
    with p_cols[2]:
        if st.session_state.current_page < total_pages:
            if st.button("▶", key="next_page", use_container_width=True):
                st.session_state.current_page += 1
                st.rerun()
