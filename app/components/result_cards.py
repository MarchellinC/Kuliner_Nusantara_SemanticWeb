import streamlit as st

RASA_COLOR = {
    "Pedas":        ("#fee2e2", "#dc2626"),
    "Manis":        ("#e0f5e9", "#16a34a"), 
    "Gurih":        ("#e0f5e9", "#16a34a"), 
    "Asam":         ("#e0f2fe", "#0284c7"),
    "Pedas Gurih":  ("#ffedd5", "#ea580c"),
    "Manis Gurih":  ("#e0f5e9", "#16a34a"),
    "Asam Pedas":   ("#fee2e2", "#dc2626"),
    "Pedas Asam":   ("#fee2e2", "#dc2626"),
    "Manis Pedas":  ("#fce7f3", "#db2777"),
    "Tawar":        ("#f1f5f9", "#64748b"),
    "Gurih Asam":   ("#d1fae5", "#059669"),
    "Asam Manis":   ("#e0f2fe", "#0284c7"),
    "Asam Gurih":   ("#d1fae5", "#059669"),
    "Pedas Pahit":  ("#f3e8ff", "#9333ea"),
    "Pedas Manis":  ("#fce7f3", "#db2777"),
    "Asam Segar":   ("#cffafe", "#0891b2"),
    "Gurih Manis":  ("#e0f5e9", "#16a34a"),
}

KATEGORI_CARD_BG = {
    "Makanan Berat":      ("#fffbeb", "#f59e0b"),
    "Makanan Ringan":     ("#fdf2f8", "#db2777"), 
    "Makanan Pendamping": ("#f0fdf4", "#10b981"),
    "Makanan Ekstrem":    ("#faf5ff", "#8b5cf6"),
    "Minuman":            ("#eff6ff", "#3b82f6"),
}


def render_food_cards(df, page_size=10):

    if df is None or df.empty:
        st.markdown(
            "<div style='background:#fff;border-radius:16px;padding:3rem 2rem;"
            "text-align:center;box-shadow:0 2px 8px rgba(0,0,0,0.06)'>"
            "<div style='font-size:3rem;margin-bottom:12px'>🍲</div>"
            "<p style='color:#a8a29e;font-size:0.9rem;margin:0'>"
            "Tidak ada kuliner ditemukan.</p></div>",
            unsafe_allow_html=True
        )
        return

    total_results = len(df)

    if "current_page" not in st.session_state:
        st.session_state.current_page = 1
    total_pages = max(1, (total_results + page_size - 1) // page_size)
    if st.session_state.current_page > total_pages:
        st.session_state.current_page = max(1, total_pages)
    start_idx = (st.session_state.current_page - 1) * page_size
    end_idx   = min(start_idx + page_size, total_results)

    # Header Hasil Pencarian
    st.markdown(
        "<div style='display:flex;justify-content:space-between;align-items:center;"
        "margin-bottom:1.5rem'>"
        "<p style='font-size:1.1rem;font-weight:700;color:#1c1917;margin:0'>"
        "Hasil Pencarian</p>"
        "<span style='background:#f59e0b;color:#1c1917;"
        "padding:6px 14px;border-radius:20px;font-size:0.78rem;font-weight:700'>"
        + str(total_results) + " kuliner</span></div>",
        unsafe_allow_html=True
    )

    # CSS Khusus untuk Trik "Invisible Button"
    st.markdown("""
    <style>
    /* 1. Atur container Streamlit jadi relatif biar tombolnya nggak lari ke atas layar */
    div[data-testid="stVerticalBlock"]:has(.food-card-wrapper) {
        position: relative;
        gap: 0 !important; 
        margin-bottom: 24px !important;
    }

    /* 2. Tangkap kotak Streamlit yang isinya tombol, bikin posisinya melayang (absolute) nutupin HTML card */
    div.element-container:has(.food-card-wrapper) + div.element-container {
        position: absolute !important;
        top: 0; left: 0; 
        width: 100%; height: 100%;
        opacity: 0 !important; /* Bikin transparan mutlak */
        z-index: 10;
    }

    /* 3. Paksa ukuran tombol melar nutupin full area */
    div.element-container:has(.food-card-wrapper) + div.element-container button {
        width: 100% !important; 
        height: 100% !important;
        cursor: pointer !important;
    }

    /* 4. Desain HTML Card-nya sendiri (Sesuai Gambar Kedua) */
    .custom-food-card-html {
        background: linear-gradient(to bottom, #f4fbf7, #edf7f2);
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    /* Efek hover pas container dilewati mouse */
    div[data-testid="stVerticalBlock"]:has(.food-card-wrapper):hover .custom-food-card-html {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }

    .card-top-row-html {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 14px;
    }

    .card-num-html {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        min-width: 34px;
        height: 34px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #475569;
        font-weight: 700;
        font-size: 0.85rem;
    }

    .card-title-html {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 6px 16px;
        font-size: 0.95rem;
        font-weight: 600;
        color: #334155;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
        display: flex;
        align-items: center;
        height: 34px;
    }

    .card-bottom-row-html {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 8px;
        padding-left: 2px;
    }

    .fc-badge-new {
        display: inline-block; 
        padding: 4px 12px; 
        border-radius: 20px;
        font-size: 0.72rem; 
        font-weight: 600;
    }

    .card-location-html {
        color: #64748b;
        font-size: 0.78rem;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)

    for i in range(start_idx, end_idx):
        row  = df.iloc[i]
        num  = i + 1
        uri  = row["makanan"]
        name = row.get("nama") or uri.split("/")[-1].replace("_", " ")
        prov = row.get("provinsi", "N/A")
        cat  = row.get("kategori", "N/A")
        rasa = row.get("rasa", "N/A")

        rasa_bg, rasa_txt = RASA_COLOR.get(rasa, ("#e0f5e9", "#16a34a"))
        cat_bg, cat_txt   = KATEGORI_CARD_BG.get(cat, ("#f0f9ff", "#0ea5e9"))

        badge_cat  = f"<span class='fc-badge-new' style='background:{cat_bg}; color:{cat_txt};'>{cat}</span>"
        badge_rasa = f"<span class='fc-badge-new' style='background:{rasa_bg}; color:{rasa_txt};'>{rasa}</span>"

        # Bikin satu container Streamlit buat ngebungkus HTML dan Tombol
        with st.container():
            
            # 1. Gambar Card Full murni pakai HTML
            st.markdown(f"""
            <div class="food-card-wrapper custom-food-card-html">
                <div class="card-top-row-html">
                    <div class="card-num-html">{num}</div>
                    <div class="card-title-html">{name}</div>
                </div>
                <div class="card-bottom-row-html">
                    <div style="display:flex; gap:8px; flex-wrap:wrap;">
                        {badge_cat}
                        {badge_rasa}
                    </div>
                    <div class="card-location-html">📍 {prov}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 2. Tombol asli diselipin di bawahnya (akan otomatis disulap jadi transparan & ditarik ke atas sama CSS kita)
            if st.button("Pilih " + name, key="food_btn_" + uri + "_" + str(i)):
                st.session_state.selected_food_details = row.to_dict()
                st.rerun()

    # Navigasi Halaman (Pagination)
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    pc1, pc2, pc3 = st.columns([1, 3, 1])
    with pc1:
        if st.session_state.current_page > 1:
            if st.button("◀", key="prev_page", use_container_width=True):
                st.session_state.current_page -= 1
                st.rerun()
    with pc2:
        st.markdown(
            "<div style='text-align:center;color:#a8a29e;font-size:0.82rem;padding:8px 0'>"
            "Halaman <strong style='color:#1c1917'>" + str(st.session_state.current_page) + "</strong>"
            " dari " + str(total_pages) + "</div>",
            unsafe_allow_html=True
        )
    with pc3:
        if st.session_state.current_page < total_pages:
            if st.button("▶", key="next_page", use_container_width=True):
                st.session_state.current_page += 1
                st.rerun()