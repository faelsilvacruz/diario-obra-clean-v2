import streamlit as st
import sqlite3
import pandas as pd
import shutil
from drive_users_db_utils import upload_users_db_to_drive

def listar_usuarios():
    try:
        conn = sqlite3.connect("users.db")
        df = pd.read_sql_query("SELECT username, role FROM userstable", conn)
        conn.close()
        return df
    except Exception as e:
        return None

def render_backup_page():
    st.title("📥 Backup e Restauração do Banco de Usuários")

    # ===== Estilo visual só para esta página =====
    st.markdown("""
        <style>
        .backup-section {
            background-color: #ffffff;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }
        .stButton>button {
            background-color: #0F2A4D;
            color: white;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: bold;
            border: none;
        }
        .stButton>button:hover {
            background-color: #15406E;
        }
        </style>
    """, unsafe_allow_html=True)

    # ====== Seção: Download do Banco ======
    st.markdown("<div class='backup-section'>", unsafe_allow_html=True)
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
    st.markdown("</div>", unsafe_allow_html=True)

    # ====== Seção: Upload / Restauração ======
    st.markdown("<div class='backup-section'>", unsafe_allow_html=True)
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
    st.markdown("</div>", unsafe_allow_html=True)

    # ====== Seção: Lista de Usuários ======
    st.markdown("<div class='backup-section'>", unsafe_allow_html=True)
    st.subheader("👥 Usuários Cadastrados Atualmente")
    usuarios_df = listar_usuarios()
    if usuarios_df is not None and not usuarios_df.empty:
        st.dataframe(usuarios_df)
    else:
        st.info("Nenhum usuário encontrado no banco atual.")
    st.markdown("</div>", unsafe_allow_html=True)

    # ====== Seção: Upload para o Google Drive ======
    st.markdown("<div class='backup-section'>", unsafe_allow_html=True)
    st.subheader("📤 Atualizar Banco de Usuários no Google Drive")
    if st.button("🔼 Fazer Upload do Banco Atual"):
        upload_users_db_to_drive()
    st.markdown("</div>", unsafe_allow_html=True)
