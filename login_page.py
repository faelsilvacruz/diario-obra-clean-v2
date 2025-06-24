import streamlit as st
import sqlite3
import hashlib

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

def get_user_by_username(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT username, password, role, senha_alterada FROM userstable WHERE username = ?', (username,))
    user_data = c.fetchone()
    conn.close()
    return user_data

def render_login_page():
    st.markdown("""
        <style>
        .stApp {
            background-color: #FFFFFF;
            color: #000000;
        }

        .titulo-principal {
            text-align: center;
            color: #0F2A4D;
            font-size: 30px;
            margin-top: 40px;
            margin-bottom: 30px;
            font-weight: bold;
        }

        input, textarea {
            background-color: #FFFFFF !important;
            color: #000000 !important;
            font-weight: bold !important;
            border: 2px solid #0F2A4D !important;
            border-radius: 6px !important;
            padding: 8px !important;
        }

        input::placeholder, textarea::placeholder {
            color: #555555 !important;
            font-weight: bold !important;
        }

        label {
            font-weight: bold !important;
            color: #0F2A4D !important;
        }

        button {
            background-color: #0F2A4D !important;
            color: white !important;
            border-radius: 8px !important;
            font-weight: bold !important;
            padding: 8px 16px !important;
        }

        button:hover {
            background-color: #14406d !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="titulo-principal">Acesso ao Diário de Obra</div>', unsafe_allow_html=True)

    username = st.text_input('Usuário')
    password = st.text_input('Senha', type='password')

    if st.button('Entrar'):
        user = get_user_by_username(username)
        if user:
            db_username, db_password, db_role, db_senha_alterada = user
            if check_hashes(password, db_password):
                st.session_state.logged_in = True
                st.session_state.username = db_username
                st.session_state.role = db_role
                st.session_state.senha_alterada = db_senha_alterada

                if db_senha_alterada == 0:
                    st.session_state.page = "alterar_senha"
                else:
                    st.session_state.page = "documentos"

                st.rerun()
            else:
                st.error('Senha incorreta.')
        else:
            st.error('Usuário não encontrado.')

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
