import streamlit as st
import sqlite3
import hashlib

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def get_connection():
    return sqlite3.connect('users.db')

def view_all_users():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT username, role, senha_alterada FROM userstable")
    data = c.fetchall()
    conn.close()
    return data

def add_user(username, password, role):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO userstable(username, password, role, senha_alterada) VALUES (?,?,?,0)',
              (username, make_hashes(password), role))
    conn.commit()
    conn.close()

def update_user(username, new_password, new_role):
    conn = get_connection()
    c = conn.cursor()
    if new_password:
        c.execute('UPDATE userstable SET password=?, role=?, senha_alterada=0 WHERE username=?',
                  (make_hashes(new_password), new_role, username))
    else:
        c.execute('UPDATE userstable SET role=? WHERE username=?',
                  (new_role, username))
    conn.commit()
    conn.close()

def delete_user(username):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM userstable WHERE username=?', (username,))
    conn.commit()
    conn.close()

def render_user_management_page():
    st.title("👥 Gerenciamento de Usuários")

    # Controle de qual aba está ativa
    if "user_aba" not in st.session_state:
        st.session_state.user_aba = "Listar Usuários"

    # Apenas muda o valor da aba se o usuário selecionar algo novo
    aba = st.radio(
        "Selecione uma ação:",
        ["Listar Usuários", "Adicionar Usuário", "Editar Usuário", "Excluir Usuário", "Status de Troca de Senha"],
        key="aba_user",
        index=["Listar Usuários", "Adicionar Usuário", "Editar Usuário", "Excluir Usuário", "Status de Troca de Senha"].index(st.session_state.user_aba)
    )

    # Atualiza o estado da aba ativa
    st.session_state.user_aba = aba

    if aba == "Listar Usuários":
        st.subheader("📋 Lista de Usuários")
        usuarios = view_all_users()
        for u in usuarios:
            status = "✅" if u[2] == 1 else "❌"
            st.text(f"Usuário: {u[0]} | Perfil: {u[1]} | Senha Alterada: {status}")

    elif aba == "Adicionar Usuário":
        st.subheader("➕ Adicionar Novo Usuário")
        novo_user = st.text_input("Nome de Usuário", key="add_user")
        nova_senha = st.text_input("Senha", type="password", key="add_pass")
        novo_role = st.selectbox("Perfil", ["admin", "encarregado", "colaborador"], key="add_role")
        if st.button("Salvar Novo Usuário"):
            if novo_user and nova_senha:
                add_user(novo_user, nova_senha, novo_role)
                st.success(f"Usuário '{novo_user}' adicionado com sucesso!")
                st.session_state.user_aba = "Listar Usuários"
                st.experimental_rerun()
            else:
                st.error("Por favor, preencha todos os campos.")

    elif aba == "Editar Usuário":
        st.subheader("✏️ Editar Usuário Existente")
        usuarios = [u[0] for u in view_all_users()]
        if usuarios:
            usuario_alvo = st.selectbox("Selecione o Usuário", usuarios, key="edit_user")
            nova_senha = st.text_input("Nova Senha (deixe em branco para manter a atual)", type="password", key="edit_pass")
            novo_role = st.selectbox("Novo Perfil", ["admin", "encarregado", "colaborador"], key="edit_role")
            if st.button("Atualizar Usuário"):
                update_user(usuario_alvo, nova_senha, novo_role)
                st.success(f"Usuário '{usuario_alvo}' atualizado com sucesso!")
                st.session_state.user_aba = "Listar Usuários"
                st.experimental_rerun()
        else:
            st.warning("Nenhum usuário encontrado.")

    elif aba == "Excluir Usuário":
        st.subheader("❌ Excluir Usuário")
        usuarios = [u[0] for u in view_all_users()]
        if usuarios:
            usuario_delete = st.selectbox("Selecione o Usuário", usuarios, key="delete_user")
            if st.button(f"Excluir '{usuario_delete}'"):
                delete_user(usuario_delete)
                st.success(f"Usuário '{usuario_delete}' excluído com sucesso!")
                st.session_state.user_aba = "Listar Usuários"
                st.experimental_rerun()
        else:
            st.warning("Nenhum usuário encontrado.")

    elif aba == "Status de Troca de Senha":
        st.subheader("🔑 Status de Troca de Senha")
        usuarios = view_all_users()
        for u in usuarios:
            status = "✅ Sim" if u[2] == 1 else "❌ Não"
            st.markdown(f"- **Usuário:** `{u[0]}` | **Perfil:** `{u[1]}` | **Senha Alterada:** {status}")
