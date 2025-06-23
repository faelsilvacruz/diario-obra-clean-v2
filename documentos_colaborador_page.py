import streamlit as st
from datetime import datetime
import pandas as pd
from drive_utils import listar_documentos_por_tipo

def render_documentos_colaborador_page():
    st.set_page_config(
        page_title="Central de Documentos - RDV Engenharia",
        page_icon="📄",
        layout="wide"
    )

    st.markdown("""
    <style>
        .sidebar .sidebar-content {
            background-color: #f8f9fa;
        }
        .document-card {
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }
        .document-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        .header {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        .sidebar-title {
            color: #3498db;
        }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar de navegação
    with st.sidebar:
        st.markdown('<h2 class="sidebar-title">📁 Navegação</h2>', unsafe_allow_html=True)
        doc_type = st.radio(
            "Selecione o tipo de documento:",
            ["Holerite", "Férias", "Informe de Rendimentos", "Documentos Pessoais"],
            key="doc_type"
        )

        st.markdown("---")
        st.markdown(f"🔹 Usuário: **{st.session_state['username']}**")
        st.markdown(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    # Título principal
    st.markdown('<h1 class="header">📄 Central de Documentos</h1>', unsafe_allow_html=True)
    st.markdown(f'<h3>Documentos - {doc_type}</h3>', unsafe_allow_html=True)

    # Lista de documentos reais do usuário
    documentos = listar_documentos_por_tipo(st.session_state['username'], doc_type)

    if documentos:
        df = pd.DataFrame(documentos)

        cols_header = st.columns([3, 2, 1, 2])
        cols_header[0].markdown("**📄 Documento**")
        cols_header[1].markdown("**📅 Data**")
        cols_header[2].markdown("**📦 Tamanho**")
        cols_header[3].markdown("**🔗 Ação**")

        for idx, doc in df.iterrows():
            cols = st.columns([3, 2, 1, 2])
            cols[0].markdown(f'📄 {doc["nome"]}')
            cols[1].markdown(doc["data"])
            cols[2].markdown(doc["tamanho"])

            with cols[3]:
                st.download_button(
                    label="📥 Download",
                    data=doc["conteudo"],  # O conteúdo real do arquivo (bytes)
                    file_name=doc["nome"],
                    key=f"download_{idx}"
                )

            st.markdown("---")
    else:
        st.info("Nenhum documento disponível nesta categoria.")
