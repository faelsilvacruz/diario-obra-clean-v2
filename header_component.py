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
            padding: 16px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        .logo-center {{
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .logo-center img {{
            height: 60px;
            object-fit: contain;
        }}
        .logout-button-container button {{
            background-color: white !important;
            color: #0F2A4D !important;
            font-weight: bold;
            border-radius: 8px;
            padding: 6px 18px;
            border: none;
            cursor: pointer;
        }}
        .logout-button-container button:hover {{
            background-color: #e0e0e0 !important;
        }}
        </style>

        <div class="custom-header">
            <div class="logo-center">
                <img src="data:image/png;base64,{logo_base64}" alt="Logo RDV">
            </div>
            <div class="logout-button-container">
                <form action="?logout" method="post">
                    <button type="submit">🚪 Sair</button>
                </form>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.query_params.get("logout") is not None:
        logout()
