import streamlit as st

def render_detail_panel(selected_food):
    st.subheader("Detail Makanan")
    
    if not selected_food:
        st.info("Pilih salah satu makanan untuk melihat detailnya.")
        return
        
    name = selected_food.get("nama") or selected_food.get("makanan", "").split("/")[-1].replace("_", " ")
    prov = selected_food.get("provinsi", "N/A")
    cat = selected_food.get("kategori", "N/A")
    rasa = selected_food.get("rasa", "N/A")
    bahan = selected_food.get("bahanUtama") or selected_food.get("bahan_utama", "N/A")
    
    st.title(name)
    st.divider()
    st.markdown(f"**📍 Asal Provinsi:** {prov}")
    st.markdown(f"**🗂️ Kategori:** {cat}")
    st.markdown(f"**😋 Cita Rasa:** {rasa}")
    st.markdown(f"**🌾 Bahan Utama:** {bahan}")