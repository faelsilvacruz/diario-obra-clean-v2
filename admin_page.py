import streamlit as st
from db_utils import get_obras, add_obra, add_contrato, add_colaborador

def render_admin_page():
    st.title("⚙️ Administração de Cadastros")

    # ===== Cadastro de Obras =====
    with st.expander("🏗️ Cadastrar Nova Obra"):
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

    # ===== Cadastro de Contratos =====
    with st.expander("📄 Cadastrar Novo Contrato"):
        obras = get_obras()
        obras_dict = {f"{obra[1]} (ID: {obra[0]})": obra[0] for obra in obras}

        with st.form("form_cadastro_contrato_admin"):
            nome_contrato = st.text_input("Nome do contrato")
            obra_selecionada = st.selectbox("Obra vinculada", list(obras_dict.keys()))

            submitted = st.form_submit_button("Cadastrar Contrato")

            if submitted:
                if nome_contrato.strip() == "":
                    st.error("Por favor, preencha o nome do contrato.")
                else:
                    obra_id = obras_dict[obra_selecionada]
                    add_contrato(obra_id, nome_contrato.strip())
                    st.success(f"Contrato '{nome_contrato}' cadastrado com sucesso!")
                    st.experimental_rerun()

    # ===== Cadastro de Colaboradores =====
    with st.expander("👷 Cadastrar Novo Colaborador"):
        with st.form("form_cadastro_colaborador_admin"):
            nome_colaborador = st.text_input("Nome do colaborador")
            funcao = st.text_input("Função")

            submitted = st.form_submit_button("Cadastrar Colaborador")

            if submitted:
                if nome_colaborador.strip() == "" or funcao.strip() == "":
                    st.error("Por favor, preencha todos os campos.")
                else:
                    add_colaborador(nome_colaborador.strip(), funcao.strip())
                    st.success(f"Colaborador '{nome_colaborador}' cadastrado com sucesso!")
                    st.experimental_rerun()
