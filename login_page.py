import streamlit as st
import sqlite3
import hashlib

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

def login_user(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT username, password, role, senha_alterada FROM userstable WHERE username = ?', (username,))
    data = c.fetchone()
    conn.close()
    return data

def render_login_page():
    st.markdown("""
        <style>
        .stApp {
            background-color: #0F2A4D;
        }
        .titulo-principal {
            text-align: center;
            color: white;
            font-size: 30px;
            margin-top: 40px;
            margin-bottom: 30px;
            font-weight: bold;
        }
        .login-inputs {
            max-width: 400px;
            margin: auto;
            background: transparent;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="titulo-principal">Acesso ao Diário de Obra</div>', unsafe_allow_html=True)

    username = st.text_input('Usuário')
    password = st.text_input('Senha', type='password')

    if st.button('Entrar'):
        user_data = login_user(username)
        if user_data and check_hashes(password, user_data[1]):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = user_data[2]
            st.session_state.senha_alterada = user_data[3]

            if st.session_state.senha_alterada == 0:
                st.session_state.page = "alterar_senha"
            else:
                st.session_state.page = "documentos"

            st.rerun()
        else:
            st.error('Usuário ou senha inválidos.')

def render_password_change_page():
    st.title("🔑 Alteração Obrigatória de Senha")
    nova_senha = st.text_input("Nova Senha", type="password")
    confirmar_senha = st.text_input("Confirme a Nova Senha", type="password")

    if st.button("Salvar Nova Senha"):
        if nova_senha == confirmar_senha and nova_senha.strip() != "":
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            hashed_pswd = make_hashes(nova_senha)
            c.execute("UPDATE userstable SET password=?, senha_alterada=1 WHERE username=?", (hashed_pswd, st.session_state.username))
            conn.commit()
            conn.close()
            st.success("Senha alterada com sucesso! Redirecionando...")
            st.session_state.page = "documentos"
            st.rerun()
        else:
            st.error("As senhas não conferem ou estão em branco.")
