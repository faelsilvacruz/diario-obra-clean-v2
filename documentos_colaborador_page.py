import streamlit as st
import pandas as pd

# Importação das funções específicas de cada documento (vamos criar cada uma depois)
from pdf_drive_utils import gerar_pdf_holerite, enviar_email

def render_documentos_colaborador_page():
    st.title("Central de Documentos - RDV Engenharia")

    # Menu interno
    menu_opcao = st.radio(
        "Selecione o tipo de documento:",
        ["Holerite", "Férias", "Informe de Rendimentos", "Documentos Pessoais", "Upload de Documentos"]
    )

    # --- HOLERITE ---
    if menu_opcao == "Holerite":
        st.header("Holerite")

        salario_file = st.file_uploader("Upload da Planilha de Salários", type=["csv", "xlsx"], key="holerite_upload")
        if salario_file:
            df_salarios = pd.read_csv(salario_file) if salario_file.name.endswith(".csv") else pd.read_excel(salario_file)

            colaborador = st.selectbox("Selecione o Colaborador", df_salarios['Nome'].unique(), key="holerite_colab")

            if colaborador:
                dados_colaborador = df_salarios[df_salarios['Nome'] == colaborador].iloc[0]

                st.markdown(f"**Salário Base:** R$ {dados_colaborador['Salario Base']}")
                st.markdown(f"**Horas Extras:** R$ {dados_colaborador['Horas Extras']}")
                st.markdown(f"**Descontos:** R$ {dados_colaborador['Descontos']}")
                st.markdown(f"**Salário Líquido:** R$ {dados_colaborador['Liquido']}")

                if st.button("Gerar PDF Holerite"):
                    gerar_pdf_holerite(dados_colaborador)
                    st.success("PDF do holerite gerado com sucesso!")

                if st.button("Enviar por E-mail"):
                    enviar_email(
                        destinatario=dados_colaborador["Email"],
                        assunto=f"Holerite RDV - {colaborador}",
                        corpo="Segue em anexo o seu Holerite.",
                        anexo_path=f"holerite_{colaborador}.pdf"
                    )
                    st.success("E-mail enviado!")

    # --- FÉRIAS ---
    elif menu_opcao == "Férias":
        st.header("Férias")
        st.info("Em breve: módulo para geração de aviso e recibo de férias.")

    # --- INFORME DE RENDIMENTOS ---
    elif menu_opcao == "Informe de Rendimentos":
        st.header("Informe de Rendimentos")
        st.info("Em breve: módulo para geração de informe anual para IRPF.")

    # --- DOCUMENTOS PESSOAIS ---
    elif menu_opcao == "Documentos Pessoais":
        st.header("Documentos Pessoais")
        st.info("Em breve: área para armazenar RG, CPF, Carteira de Trabalho e outros.")

    # --- UPLOAD DE DOCUMENTOS ---
    elif menu_opcao == "Upload de Documentos":
        st.header("Upload de Documentos")
        st.info("Aqui você poderá fazer upload manual de qualquer documento do colaborador para futura consulta.")
        # Exemplo de upload
        uploaded_file = st.file_uploader("Selecione um arquivo para upload", key="upload_documento")
        if uploaded_file:
            with open(f"uploads/{uploaded_file.name}", "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"Arquivo {uploaded_file.name} salvo com sucesso!")
