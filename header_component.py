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
        .custom-header {{
            width: 100%;
            background-color: #0F2A4D;
            padding: 20px 0;
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}

        .custom-header img {{
            height: 80px;
            object-fit: contain;
        }}
        </style>

        <div class="custom-header">
            <img src="data:image/png;base64,{logo_base64}">
        </div>
    """, unsafe_allow_html=True)
