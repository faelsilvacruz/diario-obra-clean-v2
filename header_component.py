import streamlit as st
import base64

def get_base64_of_bin_file(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def render_header():
    st.markdown("""
        <style>
        /* Remover padding padrão do Streamlit */
        .block-container {
            padding: 0 !important;
            margin: 0 !important;
        }

        .header-container {
            display: flex;
            justify-content: center;  /* Centraliza horizontal */
            align-items: center;      /* Centraliza vertical */
            background-color: #0F2A4D;
            padding: 20px;
            height: 150px;  /* Altura da faixa azul */
            width: 100%;
        }

        .header-logo img {
            height: 100px;  /* Tamanho da logo */
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='header-container'>", unsafe_allow_html=True)

    try:
        logo_path = "LOGO_RDV_AZUL.png"
        logo_base64 = get_base64_of_bin_file(logo_path)
        st.markdown(f"""
            <div class='header-logo'>
                <img src="data:image/png;base64,{logo_base64}">
            </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.markdown("<div class='header-logo'></div>", unsafe_allow_html=True)
        st.error(f"Erro ao carregar a logo: {str(e)}")

    st.markdown("</div>", unsafe_allow_html=True)
