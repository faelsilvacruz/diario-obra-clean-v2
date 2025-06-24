import streamlit as st
import base64

def get_base64_of_bin_file(filepath):
    with open(filepath, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def render_header():
    logo_base64 = get_base64_of_bin_file("LOGO_RDV_AZUL.png")

    full_header_html = f"""
        <style>
        .block-container {{
            padding: 0 !important;
            margin: 0 !important;
        }}

        .custom-header {{
            width: 100%;
            height: 140px;
            background-color: #0F2A4D;
            display: flex;
            justify-content: center;
            align-items: center;
        }}

        .custom-header img {{
            height: 100px;
            object-fit: contain;
        }}
        </style>

        <div class="custom-header">
            <img src="data:image/png;base64,{logo_base64}">
        </div>
    """

    st.markdown(full_header_html, unsafe_allow_html=True)
