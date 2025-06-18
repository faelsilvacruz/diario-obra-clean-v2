import streamlit as st
from db_utils import (
    get_obras, get_contratos, get_colaboradores,
    add_obra, add_contrato, add_colaborador,
    excluir_obra_por_id, excluir_contrato_por_id, excluir_colaborador_por_id
)

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

    # ===== Exclusão de Obras =====
    with st.expander("❌ Excluir Obra"):
        obras = get_obras()
        if obras:
            opcoes_obras = [f"{obra[0]} - {obra[1]}" for obra in obras]
            obra_selecionada = st.selectbox("Selecione a obra para excluir:", opcoes_obras, key="excluir_obra")

            if obra_selecionada:
                obra_id = int(obra_selecionada.split(" - ")[0])
                if st.button("Excluir Obra"):
                    excluir_obra_por_id(obra_id)
                    st.success("Obra excluída com sucesso!")
                    st.experimental_rerun()
        else:
            st.info("Nenhuma obra cadastrada para excluir.")

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

    # ===== Exclusão de Contratos =====
    with st.expander("❌ Excluir Contrato"):
        contratos = get_contratos()
        if contratos:
            opcoes_contratos = [f"{c[0]} - {c[1]}" for c in contratos]
            contrato_selecionado = st.selectbox("Selecione o contrato para excluir:", opcoes_contratos, key="excluir_contrato")

            if contrato_selecionado:
                contrato_id = int(contrato_selecionado.split(" - ")[0])
                if st.button("Excluir Contrato"):
                    excluir_contrato_por_id(contrato_id)
                    st.success("Contrato excluído com sucesso!")
                    st.experimental_rerun()
        else:
            st.info("Nenhum contrato cadastrado para excluir.")

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

    # ===== Exclusão de Colaboradores =====
    with st.expander("❌ Excluir Colaborador"):
        colaboradores = get_colaboradores()
        if colaboradores:
            opcoes_colabs = [f"{c[0]} - {c[1]}" for c in colaboradores]
            colaborador_selecionado = st.selectbox("Selecione o colaborador para excluir:", opcoes_colabs, key="excluir_colaborador")

            if colaborador_selecionado:
                colaborador_id = int(colaborador_selecionado.split(" - ")[0])
                if st.button("Excluir Colaborador"):
                    excluir_colaborador_por_id(colaborador_id)
                    st.success("Colaborador excluído com sucesso!")
                    st.experimental_rerun()
        else:
            st.info("Nenhum colaborador cadastrado para excluir.")
