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
        .rdv-header {{
            width: 100%;
            background-color: #0F2A4D;
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .rdv-header img {{
            height: 50px;
            object-fit: contain;
        }}

        .rdv-sair-form button {{
            background-color: white !important;
            color: #0F2A4D !important;
            border-radius: 6px !important;
            padding: 6px 16px !important;
            font-weight: bold !important;
            border: none !important;
            cursor: pointer !important;
        }}

        .rdv-sair-form button:hover {{
            background-color: #e0e0e0 !important;
        }}
        </style>
    """, unsafe_allow_html=True)

    # Render faixa azul com logo à esquerda e botão sair à direita (com st.form invisível)
    col1, col2 = st.columns([8, 1])

    with col1:
        st.markdown(f"<div class='rdv-header'><img src='data:image/png;base64,{logo_base64}'></div>", unsafe_allow_html=True)

    with col2:
        with st.form(key="logout_form"):
            st.markdown("<div class='rdv-sair-form'>", unsafe_allow_html=True)
            if st.form_submit_button("🚪 Sair"):
                logout()
            st.markdown("</div>", unsafe_allow_html=True)
