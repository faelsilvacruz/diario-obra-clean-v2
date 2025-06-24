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
            margin-bottom: 20px;
            border-radius: 0;
        }
        .header-title {
            color: white;
            font-size: 22px;
            font-weight: bold;
        }
        .header-logo img {
            max-height: 50px;
        }
        .header-logout button {
            background-color: #FFFFFF !important;
            color: #0F2A4D !important;
            border-radius: 6px !important;
            padding: 6px 12px !important;
            font-weight: bold !important;
            border: none !important;
        }
        .header-logout button:hover {
            background-color: #D9D9D9 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='header-container'>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 6, 1])

    with col1:
        try:
            logo = Image.open("LOGO_RDV_AZUL.png")  # 👉 Use a logo com fundo visível (azul ou branco)
            st.image(logo, use_container_width=False, width=80)
        except:
            st.write("")

    with col2:
        st.markdown("<div class='header-title'>Sistema RDV Engenharia</div>", unsafe_allow_html=True)

    with col3:
        with st.container():
            if st.button("🚪 Sair", key="header_logout"):
                logout()

    st.markdown("</div>", unsafe_allow_html=True)
