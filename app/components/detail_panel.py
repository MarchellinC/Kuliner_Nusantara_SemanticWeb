import streamlit as st
import base64
import os

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            return f"data:image/png;base64,{encoded}"
    return None

RASA_COLOR = {
    "Pedas":        ("#fee2e2", "#dc2626"),
    "Manis":        ("#fef9c3", "#ca8a04"),
    "Gurih":        ("#dcfce7", "#16a34a"),
    "Asam":         ("#e0f2fe", "#0284c7"),
    "Pedas Gurih":  ("#ffedd5", "#ea580c"),
    "Manis Gurih":  ("#fef9c3", "#ca8a04"),
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
    "Gurih Manis":  ("#fef9c3", "#ca8a04"),
}

KATEGORI_ICON = {
    "Makanan Berat":      "app/assets/makanan_berat.png",
    "Makanan Ringan":     "app/assets/makanan_ringan.png",
    "Makanan Pendamping": "app/assets/makanan_pendamping.png",
    "Makanan Ekstrem":    "app/assets/makanan_ekstrem.png",
    "Minuman":            "app/assets/minuman.png",
}

# CSS untuk detail panel — inject sekali
_DETAIL_CSS = """
<style>
.dp-card {
    background: #ffffff;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07), 0 0 0 1px rgba(0,0,0,0.04);
}
.dp-header {
    padding: 1.4rem 1.6rem 1.2rem;
    border-bottom: 1px solid rgba(0,0,0,0.05);
}
.dp-icon  { font-size: 2rem; line-height: 1; margin-bottom: 0.4rem; }
.dp-name  {
    font-size: 1.5rem; font-weight: 800; color: #1c1917;
    margin: 0 0 0.5rem; line-height: 1.2; letter-spacing: -0.4px;
}
.dp-badge {
    display: inline-block;
    padding: 3px 11px; border-radius: 20px;
    font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.05em; text-transform: uppercase;
}
.dp-body  { padding: 1.2rem 1.6rem; display: flex; flex-direction: column; gap: 0.9rem; }
.dp-row   { display: flex; align-items: center; gap: 0.8rem; }
.dp-icon-box {
    border-radius: 10px;
    width: 2.2rem; height: 2.2rem; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
}
.dp-label {
    color: #a8a29e; font-size: 0.63rem; text-transform: uppercase;
    letter-spacing: 0.09em; font-weight: 700; margin-bottom: 2px;
}
.dp-value { font-weight: 600; font-size: 0.88rem; color: #1c1917; line-height: 1.3; }
.dp-empty {
    background: #ffffff; border-radius: 20px;
    padding: 3rem 2rem; text-align: center;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
}
.dp-empty-icon { font-size: 2.8rem; margin-bottom: 0.8rem; }
.dp-empty-text { color: #a8a29e; font-size: 0.88rem; font-weight: 500; line-height: 1.6; }
</style>
"""


def render_detail_panel(selected_food):
    st.markdown(_DETAIL_CSS, unsafe_allow_html=True)

    # ── Empty state ──────────────────────────────────────────────
    if not selected_food:
        st.markdown("""
        <div class="dp-empty">
            <div class="dp-empty-icon">🗺️</div>
            <p class="dp-empty-text">
                Pilih salah satu makanan<br>untuk melihat detailnya.
            </p>
        </div>""", unsafe_allow_html=True)
        return

    # ── Ekstrak data ─────────────────────────────────────────────
    name  = selected_food.get("nama") or selected_food.get("makanan", "").split("/")[-1].replace("_", " ")
    prov  = selected_food.get("provinsi", "N/A")
    cat   = selected_food.get("kategori", "N/A")
    rasa  = selected_food.get("rasa", "N/A")
    bahan = selected_food.get("bahanUtama") or selected_food.get("bahan_utama", "N/A")

    rasa_bg, rasa_txt = RASA_COLOR.get(rasa, ("#f1f5f9", "#64748b"))
    kat_path = KATEGORI_ICON.get(cat, "")
    
    # Cek apakah file PNG ada, jika ya gunakan image tag HTML, jika tidak gunakan emoji
    kat_b64 = get_image_base64(kat_path) if kat_path else None
    if kat_b64:
        icon_html = f"<img src='{kat_b64}' style='width: 2.2rem; height: 2.2rem; object-fit: contain;' />"
    else:
        icon_html = "🍴" # Fallback emoji generik

    # ── Render satu blok HTML — tidak ada widget native di dalamnya ──
    st.markdown(
        "<div class='dp-card'>"

        # Header
        + "<div class='dp-header' style='background:linear-gradient(135deg,#fff7ed,#fdf2f8 55%,#f0fdf4);'>"
        + "<div class='dp-icon'>" + icon_html + "</div>"
        + "<p class='dp-name'>" + name + "</p>"
        + "<span class='dp-badge' style='background:" + rasa_bg + ";color:" + rasa_txt + ";'>" + rasa + "</span>"
        + "</div>"

        # Body
        + "<div class='dp-body'>"

        # Asal provinsi
        + "<div class='dp-row'>"
        + "<div class='dp-icon-box' style='background:#fce7f3;'>📍</div>"
        + "<div><p class='dp-label'>Asal Provinsi</p><p class='dp-value'>" + prov + "</p></div>"
        + "</div>"

        # Kategori
        + "<div class='dp-row'>"
        + "<div class='dp-icon-box' style='background:#ede9fe;'>🏷️</div>"
        + "<div><p class='dp-label'>Kategori</p><p class='dp-value'>" + cat + "</p></div>"
        + "</div>"

        # Cita rasa
        + "<div class='dp-row'>"
        + "<div class='dp-icon-box' style='background:" + rasa_bg + ";'>😋</div>"
        + "<div><p class='dp-label'>Cita Rasa</p><p class='dp-value' style='color:" + rasa_txt + ";font-weight:700;'>" + rasa + "</p></div>"
        + "</div>"

        # Bahan utama
        + "<div class='dp-row'>"
        + "<div class='dp-icon-box' style='background:#fef9c3;'>🌾</div>"
        + "<div><p class='dp-label'>Bahan Utama</p><p class='dp-value'>" + bahan + "</p></div>"
        + "</div>"

        + "</div>"  # end body
        + "</div>",  # end card

        unsafe_allow_html=True
    )