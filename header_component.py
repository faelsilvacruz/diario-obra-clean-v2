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
        .custom-header-container {{
            width: 100%;
            background-color: #0F2A4D;
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}

        .custom-header-logo img {{
            height: 60px;
            object-fit: contain;
        }}

        .custom-logout-button button {{
            background-color: white;
            color: #0F2A4D;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: 600;
            border: none;
            cursor: pointer;
        }}

        .custom-logout-button button:hover {{
            background-color: #e0e0e0;
        }}
        </style>
    """, unsafe_allow_html=True)

    # Bloco do header (Logo + Botão Sair)
    col_logo, col_button = st.columns([8, 2])

    with col_logo:
        st.markdown(
            f"<div class='custom-header-logo'><img src='data:image/png;base64,{logo_base64}'></div>",
            unsafe_allow_html=True
        )

    with col_button:
        if st.button("🚪 Sair", key="header_logout"):
            logout()
