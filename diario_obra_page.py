import streamlit as st
from fpdf import FPDF
from datetime import datetime
import io
import os

class DiarioObraPDF(FPDF):
    # ... (Seu código da classe permanece igual)
    pass  # Mantenha tudo da classe como já está

def gerar_pdf_fpfd(dados_obra, colaboradores, maquinas, servicos, intercorrencias, responsavel, fiscal, clima, fotos_paths=None):
    # ... (Todo o código da função gerar_pdf_fpfd também permanece igual)
    pass  # Mantenha o conteúdo que você já tem

def render_diario_obra_page():
    st.title("Gerar Diário de Obra - RDV Engenharia")

    # Coleta os dados
    dados_obra = {
        "obra": st.text_input("Obra", "Colecta - Suzano"),
        "local": st.text_input("Local", "Administrativo"),
        "data": st.text_input("Data", datetime.now().strftime("%d/%m/%Y")),
        "contrato": st.text_input("Contrato", "Lopes Engenharia")
    }
    clima = st.selectbox("Condições do dia", ["Bom", "Chuva", "Garoa", "Impraticável", "Feriado", "Guarda"], index=0)
    servicos = st.text_area("Serviços executados", "Uso de andaimes. Em linguística, a noção de texto é ampla e ainda aberta...")
    maquinas = st.text_area("Máquinas/Equipamentos", "Andaimes, betoneira, ferramentas manuais")
    intercorrencias = st.text_area("Intercorrências", "Sem intercorrências")
    responsavel = st.text_input("Responsável Técnico", "Wellyngton Silveira")
    fiscal = st.text_input("Fiscalização", "Pedro Pascal")

    st.subheader("Colaboradores")
    collabs = []
    num_colabs = st.number_input("Quantos colaboradores?", min_value=1, max_value=10, value=3)
    for i in range(int(num_colabs)):
        cols = st.columns(4)
        nome = cols[0].text_input(f"Nome {i+1}", key=f"nome_{i}")
        funcao = cols[1].text_input(f"Função {i+1}", key=f"func_{i}")
        entrada = cols[2].text_input(f"Entrada {i+1}", value="08:00", key=f"ent_{i}")
        saida = cols[3].text_input(f"Saída {i+1}", value="17:00", key=f"sai_{i}")
        collabs.append([nome, funcao, entrada, saida])

    st.subheader("Fotos do serviço (opcional)")
    fotos_upload = st.file_uploader("Selecione fotos", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    fotos_paths = []
    if fotos_upload:
        for up in fotos_upload:
            temp_path = f"/tmp/{up.name}"
            with open(temp_path, "wb") as f:
                f.write(up.getbuffer())
            fotos_paths.append(temp_path)

    if st.button("Gerar e Baixar PDF"):
        pdf_buffer = gerar_pdf_fpfd(
            dados_obra, collabs, maquinas, servicos,
            intercorrencias, responsavel, fiscal, clima, fotos_paths
        )
        st.success("PDF gerado com sucesso!")
        st.download_button(
            label="📥 Baixar Relatório PDF",
            data=pdf_buffer,
            file_name="Diario_Obra_RDV.pdf",
            mime="application/pdf"
        )
