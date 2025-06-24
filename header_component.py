import streamlit as st
import base64

def get_base64_of_bin_file(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def render_header():
    logo_path = "LOGO_RDV_AZUL.png"
    logo_base64 = get_base64_of_bin_file(logo_path)

    st.markdown(f"""
        <style>
        .block-container {{
            padding: 0 !important;
            margin: 0 !important;
        }}

        .header-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #0F2A4D;
            height: 120px;
            width: 100%;
        }}

        .header-logo img {{
            height: 80px;
            object-fit: contain;
        }}
        </style>

        <div class="header-container">
            <div class="header-logo">
                <img src="data:image/png;base64,{logo_base64}">
            </div>
        </div>
    """, unsafe_allow_html=True)
