import streamlit as st
from datetime import datetime
from pytz import timezone

def render_documentos_page():
    # Configuração da página com layout wide para melhor aproveitamento de espaço
    st.set_page_config(
        layout="wide",
        page_title="Central de Documentos - RDV Engenharia",
        page_icon="📂"
    )

    # CSS personalizado que realmente funciona
    st.markdown("""
    <style>
        /* Remove todos os espaçamentos padrão indesejados */
        .stApp {
            padding-top: 1rem;
        }
        
        /* Estilo dos cards de documento */
        .document-card {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            border-left: 4px solid #0F2A4D;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        /* Remove o espaçamento dos containers */
        .stContainer {
            padding: 0 !important;
        }
        
        /* Estilo do botão de download */
        .stDownloadButton button {
            background-color: #0F2A4D !important;
            color: white !important;
            border: none !important;
            border-radius: 6px !important;
            padding: 8px 16px !important;
            margin-top: 10px !important;
        }
        
        /* Remove a borda azul de foco */
        .stDownloadButton button:focus {
            box-shadow: none !important;
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

    # Dados dos documentos (substitua pelos seus dados reais)
    documentos = [
        {
            "nome": "Holerite_Maio_2025.pdf",
            "nome_exibicao": "Holerite Maio 2025",
            "data": "20/05/2025",
            "tamanho": "0.08 MB"
        },
        {
            "nome": "Holerite_Abril_2025.pdf",
            "nome_exibicao": "Holerite Abril 2025",
            "data": "15/04/2025",
            "tamanho": "0.08 MB"
        },
        {
            "nome": "Holerite_Março_2025.pdf",
            "nome_exibicao": "Holerite Março 2025",
            "data": "20/03/2025",
            "tamanho": "0.08 MB"
        }
    ]

    # Exibição dos documentos
    for doc in documentos:
        with st.container():
            # Usando markdown para criar um card personalizado
            st.markdown(f"""
            <div class="document-card">
                <h4>{doc['nome_exibicao']}</h4>
                <p><strong>Data:</strong> {doc['data']}</p>
                <p><strong>Tamanho:</strong> {doc['tamanho']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Botão de download alinhado com o card
            st.download_button(
                label="Baixar Documento",
                data="",  # Substitua pelos bytes do arquivo real
                file_name=doc['nome'],
                key=f"download_{doc['nome']}"
            )
            
            st.markdown("---")  # Linha divisória entre documentos

if __name__ == "__main__":
    render_documentos_page()
