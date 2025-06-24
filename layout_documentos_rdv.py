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
        /* Estilos gerais */
        .document-card {
            background-color: #f8f9fa;
            border-radius: 8px;
            margin-bottom: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: all 0.2s ease;
        }
        .document-card:hover {
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        /* Estilos do botão */
        .stDownloadButton>button {
            background-color: #0F2A4D !important;
            color: white !important;
            border-radius: 6px !important;
            padding: 8px 16px !important;
            border: none !important;
            font-size: 14px !important;
        }
        .stDownloadButton>button:hover {
            background-color: #163A5C !important;
            transform: translateY(-1px);
        }
        
        /* Estilos do expander - SOLUÇÃO PARA BARRA BRANCA */
        .stExpander > div {
            background-color: transparent !important;
            border: none !important;
        }
        .stExpander > div > div {
            padding: 0 !important;
        }
        .stExpander > label {
            background-color: #f8f9fa !important;
            padding: 12px 15px !important;
            border-radius: 6px !important;
            margin-bottom: 0 !important;
        }
        .stExpander > label:hover {
            background-color: #e9ecef !important;
        }
        .stExpander > label:focus-within {
            box-shadow: none !important;
        }
        
        /* Remove espaçamentos indesejados */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar
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

    # Conteúdo principal
    st.title(f"📑 Documentos - {doc_type}")
    
    docs = [
        {"nome": "Holerite_Maio_2025.pdf", "data": "20/05/2025", "tamanho": "0.08 MB"},
        {"nome": "Holerite_Abril_2025.pdf", "data": "15/04/2025", "tamanho": "0.08 MB"},
        {"nome": "Holerite_Março_2025.pdf", "data": "20/03/2025", "tamanho": "0.08 MB"}
    ]

    for doc in docs:
        with st.container():
            st.markdown('<div class="document-card">', unsafe_allow_html=True)
            
            with st.expander(f"📄 {limpar_nome_documento(doc['nome'])}", expanded=False):
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.markdown(f"**📅 Data:** {doc['data']}")
                with col2:
                    st.markdown(f"**📦 Tamanho:** {doc['tamanho']}")
                
                st.download_button(
                    label="📥 Baixar Documento",
                    data="",  # Substitua pelos bytes do arquivo
                    file_name=doc['nome'],
                    key=f"download_{doc['nome']}"
                )
            
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    render_novo_layout_documentos()
