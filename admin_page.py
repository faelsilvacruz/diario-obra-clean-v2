import streamlit as st
from db_utils import get_obras, add_obra

def render_admin_page():
    st.title("⚙️ Administração de Cadastros")

    with st.expander("➕ Cadastrar Nova Obra"):
        with st.form("form_cadastro_obra_admin"):
            novo_nome_obra = st.text_input("Nome da nova obra")
            submitted = st.form_submit_button("Cadastrar Obra")

            if submitted:
                if novo_nome_obra.strip() == "":
                    st.error("Por favor, preencha o nome da obra.")
                else:
                    add_obra(novo_nome_obra.strip())
                    st.success(f"Obra '{novo_nome_obra}' cadastrada com sucesso!")
                    st.experimental_rerun()

    # Aqui depois a gente adiciona os cadastros de Contratos e Colaboradores
