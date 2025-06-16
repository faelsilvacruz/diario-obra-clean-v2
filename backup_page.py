import streamlit as st

def render_backup_page():
    st.title("📥 Backup do Banco de Usuários")

    try:
        with open("users.db", "rb") as file:
            st.download_button(
                label="📥 Fazer download do users.db",
                data=file,
                file_name="users_backup.db",
                mime="application/octet-stream"
            )
    except FileNotFoundError:
        st.error("Arquivo users.db não encontrado.")
