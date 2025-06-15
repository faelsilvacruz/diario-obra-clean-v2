import streamlit as st
import sqlite3
import pandas as pd
from login_page import make_hashes, add_userdata, view_all_users

def render_user_management_page():
    st.title("Gerenciamento de Usuários")

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Verificar permissão
    if st.session_state.get("role") != "admin":
        st.warning("Você não tem permissão para acessar esta página.")
        return

    # -------- Adicionar Novo Usuário --------
    st.subheader("Adicionar Novo Usuário")
    with st.form("add_user_form"):
        new_username = st.text_input("Nome de Usuário")
        new_password = st.text_input("Senha", type="password")
        new_role = st.selectbox("Função", ["user", "admin"])
        add_user_submitted = st.form_submit_button("Adicionar Usuário")

        if add_user_submitted:
            if new_username and new_password:
                hashed_new_password = make_hashes(new_password)
                try:
                    add_userdata(new_username, hashed_new_password, new_role)
                    st.success(f"Usuário '{new_username}' adicionado com sucesso como '{new_role}'.")
                except Exception as e:
                    st.error(f"Erro ao adicionar usuário: {e}")
            else:
                st.error("Preencha todos os campos para adicionar um novo usuário.")

    # -------- Listar Usuários Existentes --------
    st.subheader("Usuários Existentes")
    user_data = view_all_users()
    df_users = pd.DataFrame(user_data, columns=['Username', 'Password Hash', 'Role'])
    st.dataframe(df_users, use_container_width=True)

    conn.close()
