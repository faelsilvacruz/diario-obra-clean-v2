import streamlit as st
import shutil

def render_backup_page():
    st.title("📥 Backup e Restauração do Banco de Usuários")

    st.subheader("📥 Fazer Download do Banco Atual")
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

    st.markdown("---")

    st.subheader("📤 Restaurar Banco de Usuários")
    uploaded_file = st.file_uploader("Selecione um arquivo `.db` para upload e restauração", type=["db"])

    if uploaded_file:
        if st.button("✅ Restaurar Banco de Usuários"):
            try:
                with open("users.db", "wb") as f:
                    f.write(uploaded_file.read())
                st.success("Banco de usuários restaurado com sucesso! Faça login novamente.")
                st.info("Dica: Reinicie o app após restaurar.")
            except Exception as e:
                st.error(f"Erro ao restaurar banco: {e}")
