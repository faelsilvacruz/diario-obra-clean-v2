import streamlit as st
import sqlite3
import pandas as pd

def render_inspecionar_banco_page():
    st.title("🔎 Inspecionar Banco de Usuários")

    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        # Listar todas as tabelas existentes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tabelas = cursor.fetchall()

        st.subheader("📋 Tabelas Encontradas no Banco:")
        if tabelas:
            for tabela in tabelas:
                st.markdown(f"- {tabela[0]}")
        else:
            st.info("Nenhuma tabela encontrada no banco users.db.")

        conn.close()

    except Exception as e:
        st.error(f"Erro ao acessar o banco: {e}")
