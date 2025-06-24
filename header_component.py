import streamlit as st
import base64

def get_base64_of_bin_file(filepath):
    with open(filepath, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def render_header():
    logo_base64 = get_base64_of_bin_file("LOGO_RDV_AZUL.png")

    st.markdown(f"""
        <style>
        .header-bar {{
            width: 100%;
            background-color: #0F2A4D;
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}

        .header-logo img {{
            height: 60px;
            object-fit: contain;
        }}

        .header-button button {{
            background-color: white;
            color: #0F2A4D;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: 600;
            border: none;
            cursor: pointer;
        }}

        .header-button button:hover {{
            background-color: #e0e0e0;
        }}
        </style>
    """, unsafe_allow_html=True)

    # Estrutura HTML da barra com logo e botão sair
    st.markdown("<div class='header-bar'>", unsafe_allow_html=True)

    # LOGO
    st.markdown(
        f"<div class='header-logo'><img src='data:image/png;base64,{logo_base64}'></div>",
        unsafe_allow_html=True
    )

    # BOTÃO SAIR
    with st.container():
        col1, col2 = st.columns([8, 2])
        with col2:
            if st.button("🚪 Sair", key="header_logout"):
                logout()

    st.markdown("</div>", unsafe_allow_html=True)
