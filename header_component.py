import streamlit as st
from PIL import Image
from datetime import datetime

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def render_header():
    st.markdown("""
        <style>
        /* Estilos gerais */
        .stApp {
            background-color: #f5f5f5;
        }
        
        /* Header */
        .header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #0F2A4D;
            padding: 12px 24px;
            margin: -1rem -1rem 1.5rem -1rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .header-left {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .header-title {
            color: white;
            font-size: 1.4rem;
            font-weight: 600;
            margin: 0;
        }
        
        .header-logout button {
            background-color: white !important;
            color: #0F2A4D !important;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: 600;
            border: none;
            transition: all 0.3s ease;
        }
        
        .header-logout button:hover {
            background-color: #e0e0e0 !important;
            transform: translateY(-1px);
        }
        
        /* Sidebar */
        .sidebar .sidebar-content {
            background-color: white;
            padding: 20px;
            box-shadow: 2px 0 10px rgba(0,0,0,0.05);
        }
        
        /* Conteúdo principal */
        .main-content {
            background-color: white;
            border-radius: 8px;
            padding: 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        
        /* Cards de documentos */
        .document-card {
            border-left: 4px solid #0F2A4D;
            padding: 16px;
            margin-bottom: 12px;
            background-color: #f9f9f9;
            border-radius: 0 8px 8px 0;
            transition: all 0.2s ease;
        }
        
        .document-card:hover {
            background-color: #f0f0f0;
            transform: translateX(4px);
        }
        
        .document-date {
            color: #666;
            font-size: 0.85rem;
        }
        
        .document-size {
            color: #666;
            font-size: 0.85rem;
        }
        
        /* Botões */
        .stButton>button {
            border-radius: 6px !important;
            font-weight: 600 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("<div class='header-container'>", unsafe_allow_html=True)
    
    # Parte Esquerda: Logo + Título
    st.markdown("<div class='header-left'>", unsafe_allow_html=True)
    try:
        logo = Image.open("LOGO_RDV_AZUL.png")
        st.image(logo, width=60)  # Tamanho reduzido para melhor proporção
    except:
        st.markdown("<div style='width:60px;'></div>", unsafe_allow_html=True)
    st.markdown("<h1 class='header-title'>Sistema RDV Engenharia</h1>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Parte Direita: Botão Sair
    if st.button("🚪 Sair", key="header_logout"):
        logout()
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_documentos_page():
    # Sidebar
    with st.sidebar:
        st.title("📂 Navegação")
        tipo_documento = st.radio(
            "Selecione o tipo de documento:",
            ["Holerite", "Férias", "Informe de Rendimentos", "Documentos Pessoais"]
        )
        
        st.markdown("---")
        st.markdown(f"**Usuário:** {st.session_state.username}")
        st.markdown(f"**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # Conteúdo principal
    st.title("📁 Documentos")
    
    # Barra de busca
    busca = st.text_input("Buscar por nome do documento:", placeholder="Digite o nome do documento...")
    
    # Exemplo de card de documento
    with st.container():
        st.markdown("""
        <div class="document-card">
            <h4>Holerite Maio 2025</h4>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="document-date">23/06/2025</span>
                <span class="document-size">0.08 MB</span>
            </div>
            <div style="margin-top: 12px;">
                <button class="stButton">Abrir Documento</button>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Exemplo de uso
if __name__ == "__main__":
    render_header()
    render_documentos_page()
