import os
import sys
from pathlib import Path
import streamlit as st
import pandas as pd
from datetime import datetime
from pdf_drive_utils import gerar_pdf_holerite, enviar_email

def render_documentos_colaborador_page():
    st.title("📄 Central de Documentos - RDV Engenharia")

    # Menu Interno
    opcao = st.radio(
        "Selecione o tipo de documento:",
        ["Holerite", "Férias", "Informe de Rendimentos", "Documentos Pessoais", "Upload Manual de Documentos"]
    )

    # ================= HOLERITE =================
    if opcao == "Holerite":
        st.header("📑 Gerar Holerite")

        salario_file = st.file_uploader("📥 Upload da planilha de salários (CSV ou Excel)", type=["csv", "xlsx"], key="holerite_upload")
        if salario_file:
            if salario_file.name.endswith(".csv"):
                df_salarios = pd.read_csv(salario_file)
            else:
                df_salarios = pd.read_excel(salario_file)

            colaboradores = df_salarios['Nome'].unique()
            colaborador = st.selectbox("👷 Selecione o Colaborador", colaboradores, key="holerite_colab")

            if colaborador:
                dados = df_salarios[df_salarios['Nome'] == colaborador].iloc[0]

                st.subheader("💰 Resumo do Holerite:")
                st.write(f"**Salário Base:** R$ {dados['Salario Base']:.2f}")
                st.write(f"**Horas Extras:** R$ {dados['Horas Extras']:.2f}")
                st.write(f"**Vale Alimentação:** R$ {dados['Vale Alimentacao']:.2f}")
                st.write(f"**Descontos:** R$ {dados['Descontos']:.2f}")
                st.markdown(f"### 💵 Salário Líquido: R$ **{dados['Liquido']:.2f}**")

                if st.button("📤 Gerar PDF do Holerite"):
                    pdf_buffer = gerar_pdf_holerite(dados)
                    if pdf_buffer:
                        st.success("PDF do Holerite gerado com sucesso!")
                        st.download_button(
                            label="📥 Baixar Holerite PDF",
                            data=pdf_buffer,
                            file_name=f"Holerite_{colaborador.replace(' ', '_')}.pdf",
                            mime="application/pdf"
                        )

                if st.button("✉️ Enviar por E-mail"):
                    corpo_html = f"<p>Segue em anexo o Holerite do colaborador <b>{colaborador}</b>.</p>"
                    pdf_buffer = gerar_pdf_holerite(dados)
                    if pdf_buffer:
                        sucesso = enviar_email(
                            destinatarios=[dados["Email"]],
                            assunto=f"Holerite RDV - {colaborador}",
                            corpo_html=corpo_html,
                            pdf_buffer=pdf_buffer,
                            nome_pdf=f"Holerite_{colaborador.replace(' ', '_')}.pdf"
                        )
                        if sucesso:
                            st.success(f"E-mail enviado para {dados['Email']}!")
                        else:
                            st.error("Erro ao enviar e-mail.")

    # ================= FÉRIAS =================
    elif opcao == "Férias":
        st.header("🏖️ Módulo de Férias")
        st.info("Em breve: geração de aviso e recibo de férias.")

    # ================= INFORME DE RENDIMENTOS =================
    elif opcao == "Informe de Rendimentos":
        st.header("📊 Informe de Rendimentos")
        st.info("Em breve: geração de informe anual para declaração do IR.")

    # ================= DOCUMENTOS PESSOAIS =================
    elif opcao == "Documentos Pessoais":
        st.header("📁 Documentos Pessoais")
        st.info("Em breve: área para salvar RG, CPF, Carteira de Trabalho e outros.")

    # ================= UPLOAD MANUAL =================
    elif opcao == "Upload Manual de Documentos":
        st.header("⬆️ Upload Manual de Documentos")
        arquivo = st.file_uploader("📥 Selecione o arquivo para upload", key="upload_doc_manual")
        if arquivo:
            nome_arquivo = f"uploads/{arquivo.name}"
            with open(nome_arquivo, "wb") as f:
                f.write(arquivo.getbuffer())
            st.success(f"Arquivo '{arquivo.name}' salvo localmente na pasta 'uploads'.")
