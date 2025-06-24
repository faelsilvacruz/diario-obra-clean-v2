import streamlit as st
import base64

def get_base64_of_bin_file(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def render_header():
    st.markdown("""
        <style>
        /* Reset de margens */
        .stApp {
            margin: 0;
            padding: 0;
        }
        
        /* Container do header - altura mais compacta */
        .header-container {
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #0F2A4D;
            width: 100%;
            height: 100px;  /* Altura reduzida */
            padding: 0;
            margin: 0;
        }
        
        /* Container da logo - ajuste fino */
        .logo-wrapper {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%;
            width: 100%;
        }
        
        /* Imagem com tamanho controlado */
        .logo-img {
            height: 60px;  /* Altura fixa */
            width: auto;   /* Largura proporcional */
            object-fit: contain;
        }
        
        /* Espaçamento para o conteúdo */
        .main-content {
            padding: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header com logo
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
        st.markdown("<div style='color:white;font-size:1.2rem;'>RDV ENGENHARIA</div>", 
                   unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)  # Fecha logo-wrapper
    st.markdown("</div>", unsafe_allow_html=True)  # Fecha header-container

    # Inicia o conteúdo principal
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)

# Exemplo de uso com o conteúdo da imagem
if __name__ == "__main__":
    render_header()
    
    st.title("Documents")
    st.markdown("---")
    
    st.markdown("### Selecione o tipo de documento:")
    st.markdown("- **Holerite**")
    st.markdown("- **Férias**")
    st.markdown("- **Informe de Rendimentos**")
    st.markdown("- **Documentos Pessoais**")
    
    st.markdown("---")
    
    st.markdown(f"### Usuário: raphael.cruz")
    st.markdown(f"24/06/2025 16:29")
    
    st.markdown("---")
    
    st.markdown("**Buscar por nome do documento:**")
    st.text_input("", label_visibility="collapsed")
    
    st.markdown("</div>", unsafe_allow_html=True)  # Fecha main-content
