import streamlit as st
from datetime import datetime
from drive_utils import listar_arquivos_por_usuario  # Sua função atual de busca no Drive

def render_documentos_colaborador_page():
    # Configuração da página
    st.set_page_config(
        page_title="Central de Documentos - RDV Engenharia",
        page_icon="📂",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # CSS personalizado aprimorado
    st.markdown("""
    <style>
        :root {
            --primary-color: #2c3e50;
            --secondary-color: #3498db;
            --accent-color: #e74c3c;
            --light-bg: #f8f9fa;
            --card-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .document-card {
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: var(--card-shadow);
            transition: all 0.3s ease;
            background-color: white;
            border-left: 4px solid var(--secondary-color);
        }
        .document-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }
        .sidebar .sidebar-content {
            background-color: var(--light-bg);
            padding: 20px;
        }
        .sidebar-title {
            color: var(--primary-color);
            font-size: 1.2rem;
            margin-bottom: 20px;
        }
        .user-info {
            background-color: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: var(--card-shadow);
        }
        .page-header {
            color: var(--primary-color);
            border-bottom: 2px solid var(--secondary-color);
            padding-bottom: 10px;
            margin-bottom: 30px;
        }
        .document-name {
            font-weight: 600;
            color: var(--primary-color);
            margin-bottom: 5px;
        }
        .document-meta {
            font-size: 0.85rem;
            color: #666;
            display: flex;
            gap: 15px;
            margin-top: 10px;
        }
        .download-btn {
            background-color: var(--secondary-color) !important;
            color: white !important;
            border: none !important;
            border-radius: 6px !important;
            padding: 8px 16px !important;
            margin-top: 10px;
        }
        .download-btn:hover {
            background-color: #2980b9 !important;
        }
        .stRadio > div {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .stRadio [role="radiogroup"] {
            gap: 8px;
        }
        .empty-state {
            text-align: center;
            padding: 40px;
            color: #666;
        }
        .empty-state svg {
            font-size: 3rem;
            margin-bottom: 15px;
            color: #ddd;
        }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar com navegação e informações do usuário
    with st.sidebar:
        st.markdown('<h2 class="sidebar-title">📂 Navegação de Documentos</h2>', unsafe_allow_html=True)
        
        opcao = st.radio(
            "Selecione o tipo de documento:",
            ["Holerite", "Férias", "Informe de Rendimentos", "Documentos Pessoais"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Área de informações do usuário
        st.markdown('<div class="user-info">'
                    f'<p style="font-weight:600;margin-bottom:5px;">👤 Informações do Usuário</p>'
                    f'<p><strong>Nome:</strong> {st.session_state.get("username", "não identificado")}</p>'
                    f'<p><strong>Data:</strong> {datetime.now().strftime("%d/%m/%Y %H:%M")}</p>'
                    '</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("ℹ️ Em caso de problemas, contate o RH")

    # Conteúdo principal
    st.markdown(f'<h1 class="page-header">📂 Central de Documentos</h1>', unsafe_allow_html=True)
    st.markdown(f'<h3 style="color: var(--primary-color);">{opcao}</h3>', unsafe_allow_html=True)

    username = st.session_state.get('username', '')
    if not username:
        st.error("Erro: Usuário não identificado na sessão.")
        return

    # Carregar documentos com estado para mostrar loading
    with st.spinner(f"Carregando {opcao.lower()}..."):
        arquivos = listar_arquivos_por_usuario(opcao, username)

    if not arquivos:
        st.markdown("""
        <div class="empty-state">
            <div>📭</div>
            <h3>Nenhum documento encontrado</h3>
            <p>Não há documentos disponíveis nesta categoria no momento.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    # Exibição em formato de cards aprimorados
    for arquivo in arquivos:
        # Extrair data do nome do arquivo (se possível)
        doc_name = arquivo['name']
        doc_date = "Última modificação: " + datetime.strptime(arquivo['modifiedTime'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%d/%m/%Y') if 'modifiedTime' in arquivo else ""
        
        st.markdown(f"""
        <div class="document-card">
            <div class="document-name">📄 {doc_name}</div>
            <div class="document-meta">
                <span>{doc_date}</span>
                <span>Tamanho: {round(int(arquivo.get('size', 0))/1024/1024, 2)} MB</span>
            </div>
            <a href="{arquivo['webViewLink']}" target="_blank">
                <button class="download-btn">Abrir Documento</button>
            </a>
        </div>
        """, unsafe_allow_html=True)

    # Rodapé
    st.markdown("---")
    st.markdown("© 2023 RDV Engenharia • Todos os direitos reservados", unsafe_allow_html=True)
