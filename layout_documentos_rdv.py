import streamlit as st
from datetime import datetime
from pytz import timezone

def limpar_nome_documento(nome_arquivo):
    nome_sem_ext = nome_arquivo.replace('.pdf', '')
    nome_espacado = nome_sem_ext.replace('_', ' ')
    return nome_espacado

def render_novo_layout_documentos():
    st.set_page_config(layout="centered", page_title="Central de Documentos - RDV Engenharia", page_icon="📂")

    st.markdown(""" 
    <style>
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
            margin-bottom: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        .stExpander {
            margin-top: 0px !important;
            margin-bottom: 0px !important;
            padding-top: 0px !important;
            padding-bottom: 0px !important;
        }
        .block-container .stContainer {
            padding-top: 0px !important;
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

    docs = [
        {"nome": "Holerite_Maio_2025.pdf", "data": "20/05/2025", "tamanho": "0.08 MB"},
        {"nome": "Holerite_Abril_2025.pdf", "data": "15/04/2025", "tamanho": "0.08 MB"},
        {"nome": "Holerite_Março_2025.pdf", "data": "20/03/2025", "tamanho": "0.08 MB"}
    ]

    for doc in docs:
        st.markdown('<div class="document-card">', unsafe_allow_html=True)
        with st.expander(f"📄 {limpar_nome_documento(doc['nome'])}"):
            st.markdown(f"📅 **Data:** {doc['data']}  \n📦 **Tamanho:** {doc['tamanho']}")
            st.download_button(
                label="📥 Baixar Documento",
                data="",  # Dados reais do PDF
                file_name=doc['nome'],
                key=doc['nome']
            )
        st.markdown('</div>', unsafe_allow_html=True)
