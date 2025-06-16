import streamlit as st
from diario_obra_page import render_diario_obra_page
from documentos_colaborador_page import render_documentos_colaborador_page

# ======= MENU LATERAL =======
st.sidebar.image("LOGO_RDV_AZUL-sem fundo(1).png", width=200)
menu_opcao = st.sidebar.radio(
    "Menu Principal",
    ["Diário de Obra", "Central de Documentos", "Configurações"]
)

# ======= NAVEGAÇÃO =======
if menu_opcao == "Diário de Obra":
    render_diario_obra_page()

elif menu_opcao == "Central de Documentos":
    render_documentos_colaborador_page()

elif menu_opcao == "Configurações":
    st.title("⚙️ Configurações")
    st.info("Área para futuras configurações do sistema.")
