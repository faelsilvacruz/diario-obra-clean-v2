import streamlit as st
import pandas as pd
import os
from datetime import datetime
from pathlib import Path
from pdf_drive_utils import gerar_pdf, processar_fotos, enviar_email
from db_utils import get_obras

def render_diario_obra_page():
    @st.cache_data(ttl=3600)
    def carregar_arquivo_csv(nome_arquivo):
        if not os.path.exists(nome_arquivo):
            st.error(f"Erro: Arquivo de dados '{nome_arquivo}' não encontrado.")
            return pd.DataFrame()
        try:
            return pd.read_csv(nome_arquivo)
        except Exception as e:
            st.error(f"Erro ao ler o arquivo '{nome_arquivo}': {e}")
            return pd.DataFrame()

    contratos_df = carregar_arquivo_csv("contratos.csv")
    colab_df = pd.DataFrame()
    colaboradores_lista = []

    # ===== Agora lendo as obras direto do banco =====
    obras_do_banco = get_obras()
    obras_lista = [""] + [obra[1] for obra in obras_do_banco] + ["❗ Obra não encontrada? Fale com o Administrativo"]

    try:
        colab_df = pd.read_csv("colaboradores.csv", quotechar='"', skipinitialspace=True)
        if not colab_df.empty and {"Nome", "Função"}.issubset(colab_df.columns):
            colab_df = colab_df.dropna()
            colab_df["Nome"] = colab_df["Nome"].astype(str).str.strip()
            colab_df["Função"] = colab_df["Função"].astype(str).str.strip()
            colab_df["Nome_Normalizado"] = colab_df["Nome"].str.lower().str.strip()
            colaboradores_lista = colab_df["Nome"].tolist()
    except Exception as e:
        st.error(f"Erro ao carregar 'colaboradores.csv': {e}")
        colab_df = pd.DataFrame()

    if contratos_df.empty:
        st.error("Erro: Contratos não encontrados. Verifique o arquivo 'contratos.csv'.")
        st.stop()

    contratos_lista = [""] + contratos_df["Nome"].tolist()

    st.title("Relatório Diário de Obra - RDV Engenharia")
    obra = st.selectbox("Obra", obras_lista)

    # Caso o usuário escolha a opção de obra não encontrada
    if obra == "❗ Obra não encontrada? Fale com o Administrativo":
        st.warning("Por favor, entre em contato com o Administrativo para cadastrar a nova obra.")
        st.stop()

    local = st.text_input("Local")
    data = st.date_input("Data", datetime.today())
    contrato = st.selectbox("Contrato", contratos_lista)
    clima = st.selectbox("Condições do dia", ["Bom", "Chuva", "Garoa", "Impraticável", "Feriado", "Guarda"])
    maquinas = st.text_area("Máquinas e equipamentos utilizados")
    servicos = st.text_area("Serviços executados no dia")

    st.subheader("Efetivo de Pessoal")
    max_colabs = len(colaboradores_lista) if colaboradores_lista else 8
    qtd_colaboradores = st.number_input("Quantos colaboradores hoje?", min_value=1, max_value=max_colabs, value=1, step=1)
    efetivo_lista = []

    for i in range(int(qtd_colaboradores)):
        with st.container():
            with st.expander(f"Colaborador {i+1}", expanded=True):
                nome = st.selectbox("Nome", [""] + colaboradores_lista, key=f"colab_nome_{i}")
                funcao = ""
                if nome and not colab_df.empty:
                    nome_normalizado = nome.strip().lower()
                    match = colab_df[colab_df["Nome_Normalizado"] == nome_normalizado]
                    if not match.empty:
                        funcao = match.iloc[0]["Função"].strip()
                st.markdown(f"**Função:** {funcao if funcao else 'Selecione o colaborador'}")
                col1, col2 = st.columns(2)
                entrada = col1.time_input("Entrada", value=datetime.strptime("08:00", "%H:%M").time(), key=f"entrada_{i}")
                saida = col2.time_input("Saída", value=datetime.strptime("17:00", "%H:%M").time(), key=f"saida_{i}")
                efetivo_lista.append([nome, funcao, entrada.strftime("%H:%M"), saida.strftime("%H:%M")])

    st.subheader("Controle de Documentação de Segurança")
    col1, col2 = st.columns(2)
    hora_lt = col1.time_input("Hora de Liberação da LT", value=datetime.strptime("07:00", "%H:%M").time())
    hora_apr = col2.time_input("Hora de Liberação da APR", value=datetime.strptime("07:00", "%H:%M").time())
    data_apr = st.date_input("Data da APR", value=datetime.today())
    numero_apr = st.text_input("Número/Código da APR")

    st.subheader("Informações Adicionais")
    ocorrencias = st.text_area("Ocorrências")
    nome_empresa = st.text_input("Responsável Técnico")
    nome_fiscal = st.text_input("Fiscalização")
    fotos = st.file_uploader("Fotos do serviço", accept_multiple_files=True, type=["png", "jpg", "jpeg"])

    if st.button("Salvar e Gerar Relatório"):
        if not obra:
            st.error("Por favor, selecione a Obra.")
            st.stop()
        if not contrato:
            st.error("Por favor, selecione o Contrato.")
            st.stop()
        if not nome_empresa:
            st.error("Preencha o campo Responsável Técnico.")
            st.stop()

        controle_doc_texto = f"""Hora de Liberação da LT: {hora_lt.strftime('%H:%M')}
Hora de Liberação da APR: {hora_apr.strftime('%H:%M')}
Data da APR: {data_apr.strftime('%d/%m/%Y')}
Número/Código da APR: {numero_apr}"""

        fotos_processed_paths = processar_fotos(fotos, obra, data) if fotos else []

        registro = {
            "dados_obra": {
                "obra": obra,
                "local": local,
                "data": data.strftime("%d/%m/%Y"),
                "contrato": contrato
            },
            "colaboradores": efetivo_lista,
            "maquinas": maquinas,
            "servicos": servicos,
            "controle_doc": controle_doc_texto,
            "intercorrencias": ocorrencias,
            "responsavel": nome_empresa,
            "fiscal": nome_fiscal,
            "clima": clima
        }

        pdf_buffer = gerar_pdf(
            registro["dados_obra"],
            registro["colaboradores"],
            registro["maquinas"],
            registro["servicos"],
            registro["controle_doc"],
            registro["intercorrencias"],
            registro["responsavel"],
            registro["fiscal"],
            registro["clima"],
            fotos_processed_paths
        )

        nome_pdf = f"Diario_{obra.replace(' ', '_')}_{data.strftime('%Y-%m-%d')}.pdf"

        st.download_button(
            label="📥 Baixar Relatório PDF",
            data=pdf_buffer,
            file_name=nome_pdf,
            mime="application/pdf",
            type="primary"
        )

        assunto = f"Diário de Obra - {obra} ({data.strftime('%d/%m/%Y')})"
        corpo = f"""<p>Relatório diário gerado:</p>
<ul>
<li>Obra: {obra}</li>
<li>Data: {data.strftime('%d/%m/%Y')}</li>
<li>Responsável: {nome_empresa}</li>
</ul>"""

        pdf_buffer.seek(0)
        if enviar_email(["administrativo@rdvengenharia.com.br", "comercial@rdvengenharia.com.br"], assunto, corpo, pdf_buffer, nome_pdf):
            st.success("E-mail enviado com sucesso!")
        else:
            st.error("Falha ao enviar o e-mail.")
