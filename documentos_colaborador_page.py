import streamlit as st
from datetime import datetime
from drive_utils import listar_arquivos_por_usuario  # Sua função atual de busca no Drive

def render_documentos_colaborador_page():
    st.set_page_config(
        page_title="Central de Documentos - RDV Engenharia",
        page_icon="📄",
        layout="wide"
    )

    # CSS para o layout bonito
    st.markdown("""
    <style>
        .document-card {
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: transform 0.2s;
            background-color: #f8f9fa;
        }
        .document-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        .sidebar-title {
            color: #3498db;
        }
        .small-text {
            font-size: 0.85em;
            color: #888;
        }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar com filtro de tipo de documento
    with st.sidebar:
        st.markdown('<h2 class="sidebar-title">📁 Navegação</h2>', unsafe_allow_html=True)
        opcao = st.radio(
            "Selecione o tipo de documento:",
            ["Holerite", "Férias", "Informe de Rendimentos", "Documentos Pessoais"]
        )
        st.markdown("---")
        st.markdown(f"🔹 Usuário: **{st.session_state.get('username', 'não identificado')}**")
        st.markdown(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    # Conteúdo principal
    st.markdown(f"<h1>📄 Central de Documentos - {opcao}</h1>", unsafe_allow_html=True)

    username = st.session_state.get('username', '')
    if not username:
        st.error("Erro: Usuário não identificado na sessão.")
        return

    arquivos = listar_arquivos_por_usuario(opcao, username)

    if not arquivos:
        st.info("Nenhum documento encontrado nesta categoria.")
        return

    # Exibição em formato de cards
    for arquivo in arquivos:
        st.markdown(f"""
        <div class="document-card">
            <h4>📄 {arquivo['name']}</h4>
            <p class="small-text">Link: <a href="{arquivo['webViewLink']}" target="_blank">Abrir no Google Drive</a></p>
        </div>
        """, unsafe_allow_html=True)
