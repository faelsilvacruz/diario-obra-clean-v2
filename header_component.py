import streamlit as st
from PIL import Image

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def render_header():
    st.markdown("""
        <style>
        .header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #0F2A4D;
            padding: 10px 20px;
            margin: -1rem -1rem 20px;  /* Compensa o padding padrão do Streamlit */
            border-radius: 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .header-left {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .header-logo {
            height: 50px;
            display: flex;
            align-items: center;
        }
        .header-title {
            color: white;
            font-size: 22px;
            font-weight: bold;
            white-space: nowrap;
        }
        .header-logout {
            display: flex;
            align-items: center;
        }
        .header-logout button {
            background-color: #FFFFFF !important;
            color: #0F2A4D !important;
            border-radius: 6px !important;
            padding: 6px 16px !important;
            font-weight: bold !important;
            border: none !important;
            margin: 0 !important;
        }
        .header-logout button:hover {
            background-color: #D9D9D9 !important;
        }

        /* Ajuste para telas pequenas (responsividade) */
        @media screen and (max-width: 600px) {
            .header-title {
                font-size: 18px;
            }
            .header-logo img {
                width: 40px;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='header-container'>", unsafe_allow_html=True)

    # ==== Parte Esquerda: Logo + Nome ====
    st.markdown("<div class='header-left'>", unsafe_allow_html=True)

    try:
        logo = Image.open("LOGO_RDV_AZUL.png")  # 👉 Use a logo com fundo visível
        # Redimensionar para garantir que não fique gigante
        logo = logo.resize((50, int(50 * (logo.height / logo.width))), Image.LANCZOS)
        st.markdown("<div class='header-logo'>", unsafe_allow_html=True)
        st.image(logo, width=50)
        st.markdown("</div>", unsafe_allow_html=True)
    except Exception as e:
        st.markdown("<div class='header-logo'></div>", unsafe_allow_html=True)
        st.error(f"Erro ao carregar a logo: {str(e)}")

    st.markdown("<div class='header-title'>Sistema RDV Engenharia</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)  # Fecha header-left

    # ==== Parte Direita: Botão Sair ====
    st.markdown("<div class='header-logout'>", unsafe_allow_html=True)
    if st.button("🚪 Sair", key="header_logout"):
        logout()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # Fecha header-container
