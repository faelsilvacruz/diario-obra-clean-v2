import streamlit as st
from login_page import render_login_page, render_password_change_page
from diario_obra_page import render_diario_obra_page
from documentos_colaborador_page import render_documentos_colaborador_page
from user_management_page import render_user_management_page
from backup_page import render_backup_page
from inspecionar_banco_page import render_inspecionar_banco_page
from admin_page import render_admin_page
from drive_users_db_utils import download_users_db_from_drive

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
    
def load_custom_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        
def main():
    st.set_page_config(
        page_title="App RDV Engenharia",
        page_icon="favicon.png",
        layout="wide"
    )

    # ===== Download automático do banco de usuários =====
    download_users_db_from_drive()

    # ===== Login =====
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        render_login_page()
    else:
        if "page" not in st.session_state:
            st.session_state.page = "documentos"

        # ===== Menu de navegação =====
        if st.session_state.page != "alterar_senha":
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            st.write("---")

            user_role = st.session_state.get("role", "")

            with col1:
                if user_role in ["admin", "encarregado"]:
                    if st.button("📓 Diário"):
                        st.session_state.page = "diario"
                        st.rerun()

            with col2:
                if user_role in ["admin", "colaborador", "encarregado"]:
                    if st.button("📂 Documentos"):
                        st.session_state.page = "documentos"
                        st.rerun()

            with col3:
                if user_role == "admin":
                    if st.button("👥 Usuários"):
                        st.session_state.page = "usuarios"
                        st.session_state.user_aba = "Listar Usuários"
                        st.rerun()

            with col4:
                if user_role == "admin":
                    if st.button("💾 Backup"):
                        st.session_state.page = "backup"
                        st.rerun()

            with col5:
                if user_role == "admin":
                    if st.button("🔎 Inspecionar"):
                        st.session_state.page = "inspecionar"
                        st.rerun()

            with col6:
                if user_role == "admin":
                    if st.button("⚙️ Administração"):
                        st.session_state.page = "admin"
                        st.rerun()

        # ===== Roteamento das páginas =====
        if st.session_state.page == "diario" and st.session_state.role in ["admin", "encarregado"]:
            render_diario_obra_page()

        elif st.session_state.page == "documentos" and st.session_state.role in ["admin", "colaborador", "encarregado"]:
            render_documentos_colaborador_page()

        elif st.session_state.page == "usuarios" and st.session_state.role == "admin":
            render_user_management_page()

        elif st.session_state.page == "backup" and st.session_state.role == "admin":
            render_backup_page()

        elif st.session_state.page == "inspecionar" and st.session_state.role == "admin":
            render_inspecionar_banco_page()

        elif st.session_state.page == "admin" and st.session_state.role == "admin":
            render_admin_page()

        elif st.session_state.page == "alterar_senha":
            render_password_change_page()

        elif st.session_state.page == "teste_docs":
            render_novo_layout_documentos()

if __name__ == "__main__":
    main()
