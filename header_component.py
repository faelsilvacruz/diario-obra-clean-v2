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
        .block-container {{
            padding: 0 !important;
            margin: 0 !important;
        }}

        /* Header container ocupando o topo */
        .custom-header {{
            width: 100%;
            height: 140px;
            background-color: #0F2A4D;
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            position: relative;
            z-index: 1;
        }}

        /* Logo centralizada */
        .custom-header img {{
            height: 100px;
            object-fit: contain;
        }}

        /* Botão Sair no canto direito da faixa */
        .logout-button-container {{
            position: absolute;
            right: 30px;
            top: 30px;
        }}

        /* Estilo visual do botão Sair */
        .stButton>button {{
            background-color: white;
            color: #0F2A4D;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: 600;
            border: none;
            cursor: pointer;
        }}

        .stButton>button:hover {{
            background-color: #e0e0e0;
        }}
        </style>

        <div class="custom-header">
            <img src="data:image/png;base64,{logo_base64}">
            <div class="logout-button-container">
                <!-- O botão real vem abaixo via Streamlit -->
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Posiciona o botão Sair fisicamente fora da faixa, mas visualmente dentro (usando colunas invisíveis)
    col1, col2, col3 = st.columns([8, 2, 1])
    with col3:
        if st.button("🚪 Sair", key="header_logout"):
            logout()
