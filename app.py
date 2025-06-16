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
    st.session_state.page = "Login"

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
            st.session_state.page = "Home"
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha inválidos.")
    st.markdown('</div>', unsafe_allow_html=True)

def logout():
    st.session_state.logado = False
    st.session_state.usuario = None
    st.session_state.perfil = None
    st.session_state.page = "Login"
    st.experimental_rerun()

def render_menu_lateral():
    st.markdown("""
        <style>
            section[data-testid="stSidebar"] {
                background-color: #0F2A4D;
            }
            .sidebar-title {
                color: white;
                font-weight: bold;
                font-size: 20px;
                margin-bottom: 20px;
            }
            .sidebar-user {
                color: white;
                font-size: 14px;
                margin-bottom: 20px;
            }
            .sidebar-link {
                color: white;
                text-decoration: none;
                display: block;
                margin: 10px 0;
                font-size: 16px;
            }
            .sidebar-link:hover {
                text-decoration: underline;
            }
        </style>
    """, unsafe_allow_html=True)

    st.sidebar.image("logo_rdv.png", width=200)
    st.sidebar.markdown(f'<div class="sidebar-title">Menu Principal</div>', unsafe_allow_html=True)
    st.sidebar.markdown(f'<div class="sidebar-user">👤 Usuário: <b>{st.session_state.usuario}</b></div>', unsafe_allow_html=True)

    menu_html = ""

    # Exibição dinâmica por perfil
    if st.session_state.perfil in ["admin", "encarregado"]:
        menu_html += '<a class="sidebar-link" href="?page=Diario">📓 Diário de Obra</a>'
    menu_html += '<a class="sidebar-link" href="?page=Documentos">📂 Central de Documentos</a>'
    if st.session_state.perfil == "admin":
        menu_html += '<a class="sidebar-link" href="?page=Usuarios">👥 Gerenciamento de Usuários</a>'
    menu_html += '<a class="sidebar-link" href="?page=Sair">🚪 Sair</a>'

    st.sidebar.markdown(menu_html, unsafe_allow_html=True)

# ======= Roteamento =======
def main():
    if not st.session_state.logado:
        login()
    else:
        render_menu_lateral()

        page = st.query_params.get("page") or st.session_state.page

        if page == "Diario":
            if st.session_state.perfil in ["admin", "encarregado"]:
                render_diario_obra_page()
            else:
                st.error("Você não tem permissão para acessar o Diário de Obra.")

        elif page == "Documentos":
            render_documentos_colaborador_page()

        elif page == "Usuarios":
            if st.session_state.perfil == "admin":
                st.title("👥 Gerenciamento de Usuários")
                st.info("Em breve: módulo para cadastro e controle de usuários.")
            else:
                st.error("Acesso restrito ao administrador.")

        elif page == "Sair":
            logout()

        else:
            st.title("Bem-vindo ao Sistema RDV Engenharia")

if __name__ == "__main__":
    main()
