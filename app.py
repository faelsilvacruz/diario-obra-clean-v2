import streamlit as st
from diario_obra_page import render_diario_obra_page
from documentos_colaborador_page import render_documentos_colaborador_page

# ======= Controle de Usuários e Perfis =======
USERS = {
    "admin": {"senha": "1234", "perfil": "admin"},
    "encarregado": {"senha": "obra123", "perfil": "encarregado"},
    "joao": {"senha": "colab123", "perfil": "colaborador"},
    "maria": {"senha": "colab456", "perfil": "colaborador"}
}

# ======= Sessão =======
if "logado" not in st.session_state:
    st.session_state.logado = False
    st.session_state.usuario = None
    st.session_state.perfil = None

def login():
    st.markdown("""
        <style>
            .centered {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 80vh;
                flex-direction: column;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="centered">', unsafe_allow_html=True)
    st.title("🔐 Login - RDV Engenharia")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if usuario in USERS and USERS[usuario]["senha"] == senha:
            st.session_state.logado = True
            st.session_state.usuario = usuario
            st.session_state.perfil = USERS[usuario]["perfil"]
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha inválidos.")
    st.markdown('</div>', unsafe_allow_html=True)

def logout():
    st.session_state.logado = False
    st.session_state.usuario = None
    st.session_state.perfil = None
    st.experimental_rerun()

# ======= Layout do Menu Lateral Estilizado =======
def render_menu_lateral():
    st.markdown("""
        <style>
            .css-1d391kg {background-color: #0F2A4D;}
            .css-1d391kg .block-container {padding-top: 0;}
            .sidebar-title {
                color: white;
                font-weight: bold;
                font-size: 18px;
                margin-bottom: 20px;
            }
            .sidebar-user {
                color: white;
                font-size: 14px;
                margin-bottom: 10px;
            }
            .sidebar-link {
                color: white;
                text-decoration: none;
                display: block;
                margin: 8px 0;
            }
            .sidebar-link:hover {
                text-decoration: underline;
            }
        </style>
    """, unsafe_allow_html=True)

    st.sidebar.image("logo_rdv.png", width=200)
    st.sidebar.markdown(f'<div class="sidebar-title">Menu Principal</div>', unsafe_allow_html=True)
    st.sidebar.markdown(f'<div class="sidebar-user">👤 Usuário: <b>{st.session_state.usuario}</b></div>', unsafe_allow_html=True)

    opcoes = []
    if st.session_state.perfil in ["admin", "encarregado"]:
        opcoes.append("Diário de Obra")
    opcoes.append("Central de Documentos")
    if st.session_state.perfil == "admin":
        opcoes.append("Gerenciamento de Usuários")
    opcoes.append("Sair")

    escolha = st.sidebar.radio("", opcoes)
    return escolha

# ======= Fluxo Principal =======
if not st.session_state.logado:
    login()
else:
    escolha = render_menu_lateral()

    if escolha == "Diário de Obra":
        if st.session_state.perfil in ["admin", "encarregado"]:
            render_diario_obra_page()
        else:
            st.error("Você não tem permissão para acessar o Diário de Obra.")

    elif escolha == "Central de Documentos":
        render_documentos_colaborador_page()

    elif escolha == "Gerenciamento de Usuários":
        if st.session_state.perfil == "admin":
            st.title("👥 Gerenciamento de Usuários")
            st.info("Módulo de gerenciamento ainda será desenvolvido.")
        else:
            st.error("Acesso restrito ao administrador.")

    elif escolha == "Sair":
        logout()
