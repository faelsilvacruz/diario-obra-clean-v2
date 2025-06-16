
import streamlit as st
from diario_obra_page import render_diario_obra_page
from documentos_colaborador_page import render_documentos_colaborador_page

# ======= Usuários cadastrados (exemplo simples, depois podemos migrar para SQLite) =======
USERS = {
    "admin": {"senha": "1234", "perfil": "admin"},
    "joao": {"senha": "abc123", "perfil": "colaborador"},
    "maria": {"senha": "senha456", "perfil": "colaborador"},
}

# ======= Controle de Sessão =======
if "logado" not in st.session_state:
    st.session_state.logado = False
    st.session_state.usuario = None
    st.session_state.perfil = None

def login():
    st.title("🔐 Login - RDV Engenharia")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if usuario in USERS and USERS[usuario]["senha"] == senha:
            st.session_state.logado = True
            st.session_state.usuario = usuario
            st.session_state.perfil = USERS[usuario]["perfil"]
            st.success(f"Bem-vindo, {usuario}!")
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha inválidos.")

def logout():
    st.session_state.logado = False
    st.session_state.usuario = None
    st.session_state.perfil = None
    st.experimental_rerun()

# ======= Fluxo principal =======
if not st.session_state.logado:
    login()
else:
    st.sidebar.image("logo_rdv.png", width=200)
    st.sidebar.markdown(f"👤 Usuário: **{st.session_state.usuario}**")
    if st.sidebar.button("Sair"):
        logout()

    menu_opcao = st.sidebar.radio(
        "Menu Principal",
        ["Diário de Obra", "Central de Documentos"] if st.session_state.perfil == "admin" else ["Central de Documentos"]
    )

    if menu_opcao == "Diário de Obra":
        if st.session_state.perfil == "admin":
            render_diario_obra_page()
        else:
            st.warning("Você não tem permissão para acessar o Diário de Obra.")

    elif menu_opcao == "Central de Documentos":
        render_documentos_colaborador_page()
