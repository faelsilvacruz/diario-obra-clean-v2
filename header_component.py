import streamlit as st
import base64
from PIL import Image

def get_base64_of_bin_file(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def render_header():
    st.markdown("""
        <style>
        /* Reset de margens e padding */
        .stApp {
            margin: 0;
            padding: 0;
        }
        
        /* Container do header */
        .header-container {
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #0F2A4D;
            width: 100%;
            height: 150px;
            padding: 0;
            margin: 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        /* Container da logo */
        .logo-wrapper {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%;
        }
        
        /* Estilo da imagem */
        .logo-img {
            max-height: 80%;
            max-width: 80%;
            object-fit: contain;
        }
        
        /* Ajuste para o conteúdo principal */
        .main-content {
            padding: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header com logo centralizada
    st.markdown("<div class='header-container'>", unsafe_allow_html=True)
    st.markdown("<div class='logo-wrapper'>", unsafe_allow_html=True)
    
    try:
        # Método 1: Usando base64 (melhor para performance)
        logo_base64 = get_base64_of_bin_file("LOGO_RDV_AZUL.png")
        st.markdown(
            f'<img class="logo-img" src="data:image/png;base64,{logo_base64}">', 
            unsafe_allow_html=True
        )
        
        # Método alternativo 2: Usando PIL (caso precise redimensionar)
        # logo = Image.open("LOGO_RDV_AZUL.png")
        # st.image(logo, use_column_width='auto', output_format='PNG')
        
    except Exception as e:
        st.error(f"Erro ao carregar logo: {str(e)}")
        # Placeholder caso a logo não carregue
        st.markdown("<div style='color:white;font-size:24px;'>RDV ENGENHARIA</div>", 
                   unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)  # Fecha logo-wrapper
    st.markdown("</div>", unsafe_allow_html=True)  # Fecha header-container

    # Adiciona espaço após o header
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)

# Exemplo de uso com conteúdo
if __name__ == "__main__":
    render_header()
    
    st.title("Documentos")
    st.write("Conteúdo da página abaixo do header...")
    
    st.markdown("</div>", unsafe_allow_html=True)  # Fecha main-content
