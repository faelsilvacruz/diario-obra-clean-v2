import streamlit as st
from login_page import render_login_page
from diario_obra_page import render_diario_obra_page
from documentos_colaborador_page import render_documentos_colaborador_page

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
    st.sidebar.markdown(f'<div class="sidebar-user">👤 Usuário: <b>{st.session_state.username}</b></div>', unsafe_allow_html=True)

    menu_itens = []

    if st.session_state.role in ["admin", "encarregado"]:
        menu_itens.append("Diário de Obra")
    menu_itens.append("Central de Documentos")

    if st.session_state.role == "admin":
        menu_itens.append("Gerenciamento de Usuários")

    menu_itens.append("Sair")
    escolha = st.sidebar.radio("", menu_itens)
    return escolha

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()

def main():
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        render_login_page()
    else:
        escolha = render_menu_lateral()

        if escolha == "Diário de Obra":
            if st.session_state.role in ["admin", "encarregado"]:
                render_diario_obra_page()
            else:
                st.error("Você não tem permissão para acessar o Diário de Obra.")

        elif escolha == "Central de Documentos":
            render_documentos_colaborador_page()

        elif escolha == "Gerenciamento de Usuários":
            if st.session_state.role == "admin":
                st.title("👥 Gerenciamento de Usuários")
                st.info("Módulo de gerenciamento ainda será desenvolvido.")
            else:
                st.error("Acesso restrito ao administrador.")

        elif escolha == "Sair":
            logout()

if __name__ == "__main__":
    main()
