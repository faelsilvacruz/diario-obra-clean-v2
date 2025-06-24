import streamlit as st
from datetime import datetime
from drive_utils import listar_arquivos_por_usuario

def render_documentos_colaborador_page():
    st.set_page_config(
        page_title="Central de Documentos - RDV Engenharia",
        page_icon="📂",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # CSS personalizado com identidade RDV
    st.markdown("""
    <style>
        :root {
            --primary-color: #0F2A4D;
            --secondary-color: #446084;
            --light-bg: #F9FAFB;
        }
        .document-card {
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            background-color: white;
            border-left: 5px solid var(--primary-color);
        }
        .document-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        }
        .download-btn {
            background-color: var(--primary-color) !important;
            color: white !important;
            border-radius: 6px !important;
            padding: 8px 16px !important;
            border: none !important;
        }
        .download-btn:hover {
            background-color: #0C1E38 !important;
        }
        .sidebar-title {
            color: var(--primary-color);
            font-weight: 600;
            margin-bottom: 10px;
        }
        .user-info {
            background-color: white;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        }
        .page-header {
            color: var(--primary-color);
            border-bottom: 2px solid var(--secondary-color);
            padding-bottom: 8px;
            margin-bottom: 20px;
        }
        .document-name {
            font-weight: 600;
            color: var(--primary-color);
        }
        .document-meta {
            font-size: 0.85rem;
            color: #555;
            margin-top: 8px;
        }
        .empty-state {
            text-align: center;
            padding: 40px;
            color: #666;
        }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown('<h2 class="sidebar-title">📂 Navegação de Documentos</h2>', unsafe_allow_html=True)

        opcao = st.radio(
            "Selecione o tipo de documento:",
            ["Holerite", "Férias", "Informe de Rendimentos", "Documentos Pessoais"],
            label_visibility="collapsed"
        )

        st.markdown("---")
        st.markdown(f"""
        <div class="user-info">
            <strong>👤 Usuário:</strong> {st.session_state.get("username", "não identificado")}<br>
            <strong>📅 Data:</strong> {datetime.now().strftime("%d/%m/%Y %H:%M")}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("ℹ️ Problemas? Fale com o RH.")

    # Título principal
    st.markdown(f'<h1 class="page-header">📂 Central de Documentos</h1>', unsafe_allow_html=True)
    st.markdown(f'<h3 style="color: var(--primary-color);">{opcao}</h3>', unsafe_allow_html=True)

    username = st.session_state.get('username', '')
    if not username:
        st.error("Erro: Usuário não identificado na sessão.")
        return

    # Campo de busca
    termo_busca = st.text_input("🔎 Buscar por nome do documento:")

    # Buscar documentos do Google Drive
    with st.spinner(f"Carregando {opcao.lower()}..."):
        arquivos = listar_arquivos_por_usuario(opcao, username)

    # Filtro por nome
    if termo_busca:
        arquivos = [a for a in arquivos if termo_busca.lower() in a['name'].lower()]

    # Ordenar do mais recente para o mais antigo
    def parse_data(arquivo):
        try:
            return datetime.strptime(arquivo['modifiedTime'], '%Y-%m-%dT%H:%M:%S.%fZ')
        except:
            return datetime.min

    arquivos = sorted(arquivos, key=parse_data, reverse=True)

    if not arquivos:
        st.markdown("""
        <div class="empty-state">
            📭<br>
            <h3>Nenhum documento encontrado</h3>
            <p>Verifique os filtros ou tente outro termo de busca.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    # Exibir documentos como cards
    for arquivo in arquivos:
        nome_doc = arquivo['name']
        link = arquivo['webViewLink']
        tamanho_mb = round(int(arquivo.get('size', 0)) / 1024 / 1024, 2) if 'size' in arquivo else "-"
        ultima_mod = ""
        if 'modifiedTime' in arquivo:
            try:
                ultima_mod = datetime.strptime(arquivo['modifiedTime'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%d/%m/%Y')
            except:
                pass

        st.markdown(f"""
        <div class="document-card">
            <div class="document-name">📄 {nome_doc}</div>
            <div class="document-meta">
                <span>📅 {ultima_mod}</span> | <span>📦 {tamanho_mb} MB</span>
            </div>
            <a href="{link}" target="_blank">
                <button class="download-btn">Abrir Documento</button>
            </a>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("© RDV Engenharia - Criando Caminhos!", unsafe_allow_html=True)
