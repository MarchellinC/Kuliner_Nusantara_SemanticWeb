import streamlit as st
import streamlit.components.v1 as components
import json

def render_knowledge_graph(selected_food):
    if not selected_food:
        return

    # Load CSS styles
    try:
        with open("app/assets/kg_styles.css", encoding="utf-8") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )
    except Exception as e:
        st.error(f"Gagal memuat CSS Knowledge Graph: {e}")

    # Extract food details
    name  = selected_food.get("nama") or selected_food.get("makanan", "").split("/")[-1].replace("_", " ")
    prov  = selected_food.get("provinsi", "N/A")
    cat   = selected_food.get("kategori", "N/A")
    rasa  = selected_food.get("rasa", "N/A")
    bahan = selected_food.get("bahanUtama") or selected_food.get("bahan_utama", "N/A")

    # Define rasa styling matching Detail Panel colors
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
    rasa_bg, rasa_txt = RASA_COLOR.get(rasa, ("#f1f5f9", "#64748b"))

    name_esc = json.dumps(name)
    prov_esc = json.dumps(prov)
    cat_esc = json.dumps(cat)
    rasa_esc = json.dumps(rasa)
    bahan_esc = json.dumps(bahan)

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
        <style type="text/css">
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
            html, body {{
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                background-color: transparent;
                font-family: 'Plus Jakarta Sans', sans-serif;
            }}
            .kg-card {{
                background: #ffffff;
                border-radius: 20px;
                box-shadow: 0 2px 12px rgba(0,0,0,0.07), 0 0 0 1px rgba(0,0,0,0.04);
                overflow: hidden;
            }}
            .kg-header {{
                padding: 1.4rem 1.6rem 1.2rem;
                border-bottom: 1px solid rgba(0,0,0,0.05);
                background: linear-gradient(135deg, #fff7ed, #fdf2f8 55%, #f0fdf4);
            }}
            .kg-title {{
                font-size: 1.5rem;
                font-weight: 800;
                color: #1c1917;
                margin: 0;
                line-height: 1.2;
                letter-spacing: -0.4px;
            }}
            .kg-body {{
                padding: 1.2rem 1.6rem;
                min-height: 500px;
                background: #ffffff;
                box-sizing: border-box;
            }}
            #network {{
                width: 100%;
                height: 500px;
                background-color: transparent;
            }}
        </style>
    </head>
    <body>
    <div class="kg-card">
        <div class="kg-header">
            <h3 class="kg-title">Knowledge Graph</h3>
        </div>
        <div class="kg-body">
            <div id="network"></div>
        </div>
    </div>
    <script type="text/javascript">
        var nodes = new vis.DataSet([
            {{ 
                id: 1, 
                label: {name_esc}, 
                color: {{ background: '#ffffff', border: '#f59e0b', highlight: {{ background: '#fef3c7', border: '#d97706' }} }}, 
                size: 26, 
                shape: 'dot', 
                borderWidth: 3,
                font: {{ face: 'Plus Jakarta Sans, sans-serif', size: 14, color: '#1c1917', bold: true }} 
            }},
            {{ 
                id: 2, 
                label: {prov_esc}, 
                color: {{ background: '#fce7f3', border: '#db2777', highlight: {{ background: '#fbcfe8', border: '#be185d' }} }}, 
                size: 20, 
                shape: 'dot', 
                borderWidth: 2,
                font: {{ face: 'Plus Jakarta Sans, sans-serif', size: 11, color: '#4b5563', bold: true }} 
            }},
            {{ 
                id: 3, 
                label: {cat_esc}, 
                color: {{ background: '#ede9fe', border: '#6d28d9', highlight: {{ background: '#ddd6fe', border: '#5b21b6' }} }}, 
                size: 20, 
                shape: 'dot', 
                borderWidth: 2,
                font: {{ face: 'Plus Jakarta Sans, sans-serif', size: 11, color: '#4b5563', bold: true }} 
            }},
            {{ 
                id: 4, 
                label: {rasa_esc}, 
                color: {{ background: {json.dumps(rasa_bg)}, border: {json.dumps(rasa_txt)}, highlight: {{ background: {json.dumps(rasa_bg)}, border: {json.dumps(rasa_txt)} }} }}, 
                size: 20, 
                shape: 'dot', 
                borderWidth: 2,
                font: {{ face: 'Plus Jakarta Sans, sans-serif', size: 11, color: '#4b5563', bold: true }} 
            }},
            {{ 
                id: 5, 
                label: {bahan_esc}, 
                color: {{ background: '#fef9c3', border: '#ca8a04', highlight: {{ background: '#fef08a', border: '#a16207' }} }}, 
                size: 20, 
                shape: 'dot', 
                borderWidth: 2,
                font: {{ face: 'Plus Jakarta Sans, sans-serif', size: 11, color: '#4b5563', bold: true }} 
            }}
        ]);

        var edges = new vis.DataSet([
            {{ from: 1, to: 2, label: 'asalProvinsi', color: {{ color: '#cbd5e1' }}, font: {{ face: 'Plus Jakarta Sans, sans-serif', size: 9, color: '#64748b', align: 'horizontal' }}, arrows: 'to' }},
            {{ from: 1, to: 3, label: 'kategori', color: {{ color: '#cbd5e1' }}, font: {{ face: 'Plus Jakarta Sans, sans-serif', size: 9, color: '#64748b', align: 'horizontal' }}, arrows: 'to' }},
            {{ from: 1, to: 4, label: 'citaRasa', color: {{ color: '#cbd5e1' }}, font: {{ face: 'Plus Jakarta Sans, sans-serif', size: 9, color: '#64748b', align: 'horizontal' }}, arrows: 'to' }},
            {{ from: 1, to: 5, label: 'bahanUtama', color: {{ color: '#cbd5e1' }}, font: {{ face: 'Plus Jakarta Sans, sans-serif', size: 9, color: '#64748b', align: 'horizontal' }}, arrows: 'to' }}
        ]);

        var container = document.getElementById('network');
        var data = {{
            nodes: nodes,
            edges: edges
        }};
        var options = {{
            physics: {{
                enabled: true,
                barnesHut: {{
                    gravitationalConstant: -1800,
                    centralGravity: 0.2,
                    springLength: 90,
                    springConstant: 0.05,
                    damping: 0.09,
                    avoidOverlap: 0.2
                }}
            }},
            interaction: {{
                zoomView: false,
                dragView: true
            }}
        }};
        var network = new vis.Network(container, data, options);
    </script>
    </body>
    </html>
    """

    components.html(html_content, height=620)
