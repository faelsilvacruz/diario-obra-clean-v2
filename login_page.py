import streamlit as st
import sqlite3
import hashlib

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

conn = sqlite3.connect('users.db')
c = conn.cursor()

def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    return data

def render_login_page():
    st.markdown(
        """
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
        .logo-rodape {
            margin-top: 50px;
            text-align: center;
        }
        .logo-rodape img {
            display: block;
            margin-left: auto;
            margin-right: auto;
            max-width: 250px;
            height: auto;
            width: 100%;
        }
        </style>
        """, unsafe_allow_html=True
    )

    st.markdown('<div class="titulo-principal">Acesso ao Diário de Obra</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="login-inputs">', unsafe_allow_html=True)

        username = st.text_input('Usuário')
        password = st.text_input('Senha', type='password')

        if st.button('Entrar'):
            hashed_pswd = make_hashes(password)
            result = login_user(username, hashed_pswd)
            if result:
                st.success(f'Bem-vindo, {username}! Login realizado com sucesso.')
                st.session_state["username"] = username
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                st.error('Usuário ou senha inválidos.')

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="logo-rodape">', unsafe_allow_html=True)
    st.image('logo_rdv.png', use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
