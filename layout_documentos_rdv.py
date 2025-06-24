import streamlit as st
from datetime import datetime
from pytz import timezone

def render_novo_layout_documentos():
    st.set_page_config(layout="centered", page_title="Central de Documentos - RDV Engenharia", page_icon="📂")

    st.markdown("""
    <style>
        .expander-header {
            font-weight: bold;
            color: #0F2A4D;
        }
        .stDownloadButton>button {
            background-color: #0F2A4D;
            color: white;
            border-radius: 6px;
            padding: 8px 16px;
        }
        .stDownloadButton>button:hover {
            background-color: #163A5C;
            color: white;
        }
        .document-card {
            background-color: #f8f9fa;
            border-left: 5px solid #0F2A4D;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.title("📂 Navegação de Documentos")

        doc_type = st.radio(
            "Tipo de Documento:",
            ["Holerite", "Férias", "Informe de Rendimentos", "Documentos Pessoais"]
        )

        st.markdown(f"👤 **Usuário:** raphael.cruz")

        fuso_brasilia = timezone('America/Sao_Paulo')
        hora_local = datetime.now(fuso_brasilia).strftime('%d/%m/%Y %H:%M')
        st.markdown(f"📅 **Data:** {hora_local}")

    st.title(f"📑 Documentos - {doc_type}")

    # Simulação de documentos
    docs = [
        {"nome": "Holerite_Maio_2025.pdf", "data": "20/05/2025", "tamanho": "0.08 MB"},
        {"nome": "Holerite_Abril_2025.pdf", "data": "15/04/2025", "tamanho": "0.08 MB"},
        {"nome": "Holerite_Março_2025.pdf", "data": "20/03/2025", "tamanho": "0.08 MB"}
    ]

    for doc in docs:
        with st.container():
            st.markdown('<div class="document-card">', unsafe_allow_html=True)
            with st.expander(f"📄 {doc['nome']}"):
                st.markdown(f"📅 **Data:** {doc['data']}  \n📦 **Tamanho:** {doc['tamanho']}")
                st.download_button(
                    label="📥 Baixar Documento",
                    data="",  # Depois, insira os bytes reais do arquivo
                    file_name=doc['nome'],
                    key=doc['nome']
                )
            st.markdown('</div>', unsafe_allow_html=True)
