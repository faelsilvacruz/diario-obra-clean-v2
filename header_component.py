import streamlit as st
import base64

def get_base64_of_bin_file(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def render_header():
    st.markdown("""
        <style>
        /* Reset de margens padrão */
        .stApp {
            margin: 0;
            padding: 0;
        }

        .block-container {
            padding: 0 !important;
        }

        .header-container {
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #0F2A4D;
            width: 100%;
            height: 120px;  /* Altura total da faixa azul */
            padding: 0;
            margin: 0;
        }

        .logo-wrapper {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%;
        }

        .logo-img {
            height: 80px;
            width: auto;
            object-fit: contain;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='header-container'>", unsafe_allow_html=True)
    st.markdown("<div class='logo-wrapper'>", unsafe_allow_html=True)

    try:
        logo_base64 = get_base64_of_bin_file("LOGO_RDV_AZUL.png")
        st.markdown(
            f'<img class="logo-img" src="data:image/png;base64,{logo_base64}">', 
            unsafe_allow_html=True
        )
    except Exception as e:
        st.error(f"Erro ao carregar logo: {str(e)}")
        st.markdown("<div style='color:white;font-size:1.5rem;'>RDV ENGENHARIA</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # Fecha logo-wrapper
    st.markdown("</div>", unsafe_allow_html=True)  # Fecha header-container
