import streamlit as st
import sqlite3
import hashlib
from PIL import Image
from drive_users_db_utils import upload_users_db_to_drive  # Upload automático do banco

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
            background-color: #0F2A4D;
            color: white;
        }

        .titulo-principal {
            text-align: center;
            color: white;
            font-size: 30px;
            margin-top: 40px;
            margin-bottom: 30px;
            font-weight: bold;
        }

        label, .css-1cpxqw2, .css-14xtw13 {
            color: white !important;
            font-weight: bold !important;
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

        .main {
            padding: 0 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="titulo-principal">Sistema RDV Engenharia</div>', unsafe_allow_html=True)

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

    # ✅ Exibir logo centralizada ao final
    try:
        logo = Image.open("LOGO_RDV_AZUL-sem fundo.png")

        # Redimensionar proporcionalmente se for muito grande
        max_width = 300
        if logo.width > max_width:
            ratio = max_width / float(logo.width)
            new_height = int(float(logo.height) * float(ratio))
            logo = logo.resize((max_width, new_height), Image.LANCZOS)

        # Adiciona um espaçamento antes da logo
        st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

        # Centraliza a logo com columns
        _, center_col, _ = st.columns([1, 2, 1])
        with center_col:
            st.image(logo, use_container_width=True, output_format="PNG")

    except FileNotFoundError:
        st.warning("Arquivo de logo não encontrado. Verifique o caminho: LOGO_RDV_AZUL-sem fundo.png")
    except Exception as e:
        st.error(f"Erro ao carregar a logo: {str(e)}")

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

            # ✅ Upload automático para o Google Drive
            upload_users_db_to_drive()

            st.success("Senha alterada com sucesso! Redirecionando...")
            st.session_state.page = "documentos"
            st.rerun()
        else:
            st.error("As senhas não conferem ou estão em branco.")
