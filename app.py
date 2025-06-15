import streamlit as st
from login_page import render_login_page
from user_management_page import render_user_management_page
from diario_obra_page import render_diario_obra_page
from holerite_page import render_holerite_page

st.set_page_config(page_title="Sistema RDV", layout="centered")

# Inicializa estado de login se ainda não existir
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Se não estiver logado, chama a tela de login
if not st.session_state.logged_in:
    render_login_page()
    st.stop()

# Menu lateral
menu_options = ["Diário de Obra", "Holerite", "Gerenciamento de Usuários"]
selected = st.sidebar.selectbox("Menu", menu_options)

# Renderiza a página conforme seleção
if selected == "Diário de Obra":
    render_diario_obra_page()
elif selected == "Holerite":
    render_holerite_page()
elif selected == "Gerenciamento de Usuários":
    render_user_management_page()
