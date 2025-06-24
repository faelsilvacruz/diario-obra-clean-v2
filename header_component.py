import streamlit as st
from PIL import Image
import base64

def get_base64_of_bin_file(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def render_header():
    st.markdown("""
        <style>
        /* Remove o padding lateral padrão do Streamlit */
        .block-container {
            padding: 0 !important;
            margin: 0 !important;
        }

        .header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #0F2A4D;
            padding: 12px 24px;
            width: 100%;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .header-left {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .header-logo img {
            height: 50px;
        }

        .header-title {
            color: white;
            font-size: 1.4rem;
            font-weight: 600;
            margin: 0;
            white-space: nowrap;
        }

        .header-logout {
            display: flex;
            align-items: center;
        }

        .header-logout button {
            background-color: white !important;
            color: #0F2A4D !important;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: 600;
            border: none;
            transition: all 0.3s ease;
        }

        .header-logout button:hover {
            background-color: #e0e0e0 !important;
            transform: translateY(-1px);
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='header-container'>", unsafe_allow_html=True)

    # Parte Esquerda: Logo + Nome
    st.markdown("<div class='header-left'>", unsafe_allow_html=True)
    try:
        logo_path = "LOGO_RDV_AZUL.png"
        logo_base64 = get_base64_of_bin_file(logo_path)
        st.markdown(f"""
            <div class='header-logo'>
                <img src="data:image/png;base64,{logo_base64}">
            </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.markdown("<div class='header-logo'></div>", unsafe_allow_html=True)
        st.error(f"Erro ao carregar a logo: {str(e)}")

    st.markdown("<div class='header-title'>Sistema RDV Engenharia</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)  # Fecha header-left

    # Parte Direita: Botão Sair
    st.markdown("<div class='header-logout'>", unsafe_allow_html=True)
    if st.button("🚪 Sair", key="header_logout"):
        logout()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # Fecha header-container
