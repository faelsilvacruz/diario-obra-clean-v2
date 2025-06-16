
import streamlit as st
from login_page import render_login_page, render_password_change_page
from diario_obra_page import render_diario_obra_page
from documentos_colaborador_page import render_documentos_colaborador_page
from user_management_page import render_user_management_page
from backup_page import render_backup_page
from inspecionar_banco_page import render_inspecionar_banco_page

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def main():
    st.set_page_config(page_title="App RDV Engenharia", layout="wide")

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
        if st.session_state.get("page") == "alterar_senha":
            render_password_change_page()
            return

        st.title(f"📋 Aplicativo RDV Engenharia - Usuário: {st.session_state.username}")

        col1, col2, col3, col4, col5, col6 = st.columns(6)

        st.write("---")
        pagina = None

        with col1:
            if st.button("📓 Diário"):
                pagina = "diario"

        with col2:
            if st.button("📂 Documentos"):
                pagina = "documentos"

        with col3:
            if st.button("👥 Usuários"):
                pagina = "usuarios"

        with col4:
            if st.button("💾 Backup"):
                pagina = "backup"

        with col5:
            if st.button("🔎 Inspecionar"):
                pagina = "inspecionar"

        with col6:
            if st.button("🚪 Sair"):
                logout()

        if pagina == "diario":
            if st.session_state.role in ["admin", "encarregado"]:
                render_diario_obra_page()
            else:
                st.error("Você não tem permissão para acessar o Diário de Obra.")

        elif pagina == "documentos":
            render_documentos_colaborador_page()

        elif pagina == "usuarios":
            if st.session_state.role == "admin":
                render_user_management_page()
            else:
                st.error("Acesso restrito ao administrador.")

        elif pagina == "backup":
            if st.session_state.role == "admin":
                render_backup_page()
            else:
                st.error("Acesso restrito ao administrador.")

        elif pagina == "inspecionar":
            if st.session_state.role == "admin":
                render_inspecionar_banco_page()
            else:
                st.error("Acesso restrito ao administrador.")

if __name__ == "__main__":
    main()
