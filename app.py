import streamlit as st
from login_page import render_login_page
from diario_obra_page import render_diario_obra_page
from documentos_colaborador_page import render_documentos_colaborador_page
from user_management_page import render_user_management_page

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def render_menu_lateral():
    st.markdown("""
        <style>
            section[data-testid="stSidebar"] {
                background-color: #0F2A4D;
            }
            .sidebar-title {
                color: white;
                font-weight: bold;
                font-size: 22px;
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
                margin: 10px 0;
                font-size: 16px;
                cursor: pointer;
            }
            .sidebar-link:hover {
                text-decoration: underline;
            }
        </style>
    """, unsafe_allow_html=True)

    st.sidebar.image("logo_rdv.png", width=200)
    st.sidebar.markdown(f'<div class="sidebar-title">Menu Principal</div>', unsafe_allow_html=True)
    st.sidebar.markdown(f'<div class="sidebar-user">👤 Usuário: <b>{st.session_state.username}</b></div>', unsafe_allow_html=True)

    if st.sidebar.button("📓 Diário de Obra"):
        st.session_state.page = "diario"
        st.rerun()

    if st.sidebar.button("📂 Central de Documentos"):
        st.session_state.page = "documentos"
        st.rerun()

    if st.session_state.role == "admin":
        if st.sidebar.button("👥 Gerenciamento de Usuários"):
            st.session_state.page = "usuarios"
            st.rerun()

    if st.sidebar.button("🚪 Sair"):
        logout()

def main():
    # ======= CSS Global para Fundo Azul Escuro na Área Principal =======
    st.markdown("""
        <style>
        .main {
            background-color: #0E1A2B;
        }
        .block-container {
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        render_login_page()
    else:
        render_menu_lateral()

        page = st.session_state.get("page", "documentos")

        if page == "diario":
            if st.session_state.role in ["admin", "encarregado"]:
                render_diario_obra_page()
            else:
                st.error("Você não tem permissão para acessar o Diário de Obra.")

        elif page == "documentos":
            render_documentos_colaborador_page()

        elif page == "usuarios":
            if st.session_state.role == "admin":
                render_user_management_page()
            else:
                st.error("Acesso restrito ao administrador.")

if __name__ == "__main__":
    main()
