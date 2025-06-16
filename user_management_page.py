import streamlit as st
import sqlite3
import hashlib

# ======= Funções de hash =======
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

# ======= Conexão com o banco =======
def get_connection():
    return sqlite3.connect('users.db')

# ======= Listar todos os usuários =======
def view_all_users():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT username, role FROM userstable")
    data = c.fetchall()
    conn.close()
    return data

# ======= Adicionar novo usuário =======
def add_user(username, password, role):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO userstable(username, password, role) VALUES (?,?,?)',
              (username, make_hashes(password), role))
    conn.commit()
    conn.close()

# ======= Atualizar senha e role =======
def update_user(username, new_password, new_role):
    conn = get_connection()
    c = conn.cursor()
    if new_password:
        c.execute('UPDATE userstable SET password=?, role=? WHERE username=?',
                  (make_hashes(new_password), new_role, username))
    else:
        c.execute('UPDATE userstable SET role=? WHERE username=?',
                  (new_role, username))
    conn.commit()
    conn.close()

# ======= Deletar usuário =======
def delete_user(username):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM userstable WHERE username=?', (username,))
    conn.commit()
    conn.close()

# ======= Página principal =======
def render_user_management_page():
    st.title("👥 Gerenciamento de Usuários")

    aba = st.radio("Selecione uma ação:", ["Listar Usuários", "Adicionar Usuário", "Editar Usuário", "Excluir Usuário"])

    # ======= Listar =======
    if aba == "Listar Usuários":
        st.subheader("📋 Lista de Usuários")
        usuarios = view_all_users()
        for u in usuarios:
            st.text(f"Usuário: {u[0]} | Perfil: {u[1]}")

    # ======= Adicionar =======
    elif aba == "Adicionar Usuário":
        st.subheader("➕ Adicionar Novo Usuário")
        novo_user = st.text_input("Nome de Usuário")
        nova_senha = st.text_input("Senha", type="password")
        novo_role = st.selectbox("Perfil", ["admin", "encarregado", "colaborador"])
        if st.button("Salvar Novo Usuário"):
            if novo_user and nova_senha:
                add_user(novo_user, nova_senha, novo_role)
                st.success(f"Usuário '{novo_user}' adicionado com sucesso!")
            else:
                st.error("Por favor, preencha todos os campos.")

    # ======= Editar =======
    elif aba == "Editar Usuário":
        st.subheader("✏️ Editar Usuário Existente")
        usuarios = [u[0] for u in view_all_users()]
        usuario_alvo = st.selectbox("Selecione o Usuário", usuarios)
        nova_senha = st.text_input("Nova Senha (deixe em branco para manter a atual)", type="password")
        novo_role = st.selectbox("Novo Perfil", ["admin", "encarregado", "colaborador"])
        if st.button("Atualizar Usuário"):
            update_user(usuario_alvo, nova_senha, novo_role)
            st.success(f"Usuário '{usuario_alvo}' atualizado com sucesso!")

    # ======= Excluir =======
    elif aba == "Excluir Usuário":
        st.subheader("❌ Excluir Usuário")
        usuarios = [u[0] for u in view_all_users()]
        usuario_delete = st.selectbox("Selecione o Usuário", usuarios)
        if st.button(f"Excluir '{usuario_delete}'"):
            delete_user(usuario_delete)
            st.success(f"Usuário '{usuario_delete}' excluído com sucesso!")
