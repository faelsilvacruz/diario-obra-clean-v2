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

    header_html = f"""
        <style>
        .block-container {{
            padding: 0 !important;
            margin: 0 !important;
        }}

        .custom-header {{
            position: relative;
            width: 100%;
            height: 140px;
            background-color: #0F2A4D;
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }}

        .custom-header img {{
            height: 100px;
            object-fit: contain;
        }}

        .logout-button {{
            position: absolute;
            right: 30px;
            top: 30px;
        }}

        .logout-button button {{
            background-color: white;
            color: #0F2A4D;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: 600;
            border: none;
            cursor: pointer;
        }}

        .logout-button button:hover {{
            background-color: #e0e0e0;
        }}
        </style>

        <div class="custom-header">
            <img src="data:image/png;base64,{logo_base64}">
            <div class="logout-button">
                <form action="#" method="post">
                    <button type="submit">🚪 Sair</button>
                </form>
            </div>
        </div>
    """

    # Exibe o header
    st.markdown(header_html, unsafe_allow_html=True)

    # Lógica do botão Sair
    if st.form_submit_button("🚪 Sair"):
        logout()
