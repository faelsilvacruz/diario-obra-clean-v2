import streamlit as st
from datetime import datetime
from pytz import timezone

def render_novo_layout_documentos():
    st.set_page_config(
        layout="wide",
        page_title="Central de Documentos - RDV Engenharia",
        page_icon="📂"
    )

    # ===== CSS PERSONALIZADO =====
    st.markdown("""
    <style>
    .stExpander {
        background-color: #1a2639 !important;
        color: white !important;
        border: 1px solid #2e3e55 !important;
        border-radius: 8px !important;
        padding: 12px !important;
        margin-bottom: 12px !important;
    }
    
    .stExpander > summary {
        background-color: #224C7B !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 10px;
        font-weight: bold;
        cursor: pointer;
    }
    
    .stExpander div {
        font-size: 1rem;
        line-height: 1.6;
    }
    
    .stDownloadButton > button {
        background-color: #224C7B !important;
        color: white !important;
        border-radius: 5px;
        padding: 8px 16px;
        border: none;
    }
    
    .stDownloadButton > button:hover {
        background-color: #2f64a7 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ===== SIDEBAR =====
    with st.sidebar:
        st.title("📂 Navegação")
        doc_type = st.radio(
            "Tipo de Documento:",
            ["Holerite", "Férias", "Informe de Rendimentos", "Documentos Pessoais"]
        )
        st.markdown("---")
        st.markdown(f"👤 **Usuário:** raphael.cruz")

        fuso_brasilia = timezone('America/Sao_Paulo')
        hora_local = datetime.now(fuso_brasilia).strftime('%d/%m/%Y %H:%M')
        st.markdown(f"📅 **Data:** {hora_local}")

    # ===== TÍTULO PRINCIPAL =====
    st.title(f"📑 Documentos - {doc_type}")

    # ===== LISTA DE DOCUMENTOS =====
    documentos = [
        {"nome": "Holerite_Maio_2025.pdf", "nome_exibicao": "Holerite Maio 2025", "data": "20/05/2025", "tamanho": "0.08 MB"},
        {"nome": "Holerite_Abril_2025.pdf", "nome_exibicao": "Holerite Abril 2025", "data": "15/04/2025", "tamanho": "0.08 MB"},
        {"nome": "Holerite_Março_2025.pdf", "nome_exibicao": "Holerite Março 2025", "data": "20/03/2025", "tamanho": "0.08 MB"}
    ]

    # ===== EXIBIÇÃO DE DOCUMENTOS =====
    for doc in documentos:
        with st.expander(doc["nome_exibicao"]):
            st.write(f"📅 **Data:** {doc['data']}")
            st.write(f"📦 **Tamanho:** {doc['tamanho']}")
            st.download_button(
                label="📥 Baixar Documento",
                data="",  # Aqui você coloca os bytes reais do arquivo
                file_name=doc["nome"],
                key=f"download_{doc['nome']}"
            )

if __name__ == "__main__":
    render_documentos_page()
