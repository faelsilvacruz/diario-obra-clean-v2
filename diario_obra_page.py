import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
from pathlib import Path
import shutil
from PIL import Image as PILImage
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.colors import HexColor, black, lightgrey, white, darkgrey
from reportlab.lib.utils import ImageReader
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

from app import gerar_pdf, processar_fotos, upload_para_drive_seguro, enviar_email, creds, temp_icon_path_for_cleanup, LOGO_PDF_PATH, DRIVE_FOLDER_ID
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
        obras_df = carregar_arquivo_csv("obras.csv")
        contratos_df = carregar_arquivo_csv("contratos.csv")
        colab_df = pd.DataFrame()
        colaboradores_lista = []
        try:
            colab_df = pd.read_csv("colaboradores.csv", quotechar='"', skipinitialspace=True)
            if not colab_df.empty and {"Nome", "Função"}.issubset(colab_df.columns):
                colab_df = colab_df.dropna()
                colab_df["Nome"] = colab_df["Nome"].astype(str).str.strip()
                colab_df["Função"] = colab_df["Função"].astype(str).str.strip()
                colab_df["Nome_Normalizado"] = colab_df["Nome"].str.lower().str.strip()
                colaboradores_lista = colab_df["Nome"].tolist()
            else:
                st.error("'colaboradores.csv' deve ter colunas 'Nome' e 'Função'.")
        except Exception as e:
            st.error(f"Erro ao carregar 'colaboradores.csv': {e}")
            colab_df = pd.DataFrame()
        if obras_df.empty or contratos_df.empty:
            st.stop()
        obras_lista = [""] + obras_df["Nome"].tolist()
        contratos_lista = [""] + contratos_df["Nome"].tolist()
        st.title("Relatório Diário de Obra - RDV Engenharia")
        st.subheader("Dados Gerais da Obra")
        obra = st.selectbox("Obra", obras_lista)
        local = st.text_input("Local")
        data = st.date_input("Data", datetime.today())
        contrato = st.selectbox("Contrato", contratos_lista)
        clima = st.selectbox("Condições do dia",
                             ["Bom", "Chuva", "Garoa", "Impraticável", "Feriado", "Guarda"])
        maquinas = st.text_area("Máquinas e equipamentos utilizados")
        servicos = st.text_area("Serviços executados no dia")
        st.markdown("---")
        st.subheader("Efetivo de Pessoal")
        max_colabs = len(colaboradores_lista) if colaboradores_lista else 8
        qtd_colaboradores = st.number_input(
            "Quantos colaboradores hoje?",
            min_value=1,
            max_value=max_colabs,
            value=1,
            step=1
        )
        efetivo_lista = []
        for i in range(int(qtd_colaboradores)):
            with st.container():
                with st.expander(f"Colaborador {i+1}", expanded=True):
                    nome = st.selectbox("Nome", [""] + colaboradores_lista, key=f"colab_nome_reativo_{i}")
                    funcao = ""
                    if nome and not colab_df.empty:
                        nome_normalizado = nome.strip().lower()
                        match = colab_df[colab_df["Nome_Normalizado"] == nome_normalizado]
                        if not match.empty:
                            funcao = match.iloc[0]["Função"].strip()
                    st.markdown("Função:")
                    valor_exibir = funcao if funcao else "Selecione o colaborador para exibir a função"
                    cor_valor = "#fff" if funcao else "#888"
                    st.markdown(
                        f"""
                        <div style="background:#262730;color:{cor_valor};padding:9px 14px;
                        border-radius:7px;border:1.5px solid #363636;font-size:16px;
                        font-family:inherit;margin-bottom:10px;margin-top:2px;height:38px;
                        display:flex;align-items:center;">{valor_exibir}</div>
                        """,
                        unsafe_allow_html=True
                    )
                    col1, col2 = st.columns(2)
                    with col1:
                        entrada = st.time_input("Entrada", value=datetime.strptime("08:00", "%H:%M").time(), key=f"colab_entrada_reativo_{i}")
                    with col2:
                        saida = st.time_input("Saída", value=datetime.strptime("17:00", "%H:%M").time(), key=f"colab_saida_reativo_{i}")
                    efetivo_lista.append({
                        "Nome": nome,
                        "Função": funcao,
                        "Entrada": entrada.strftime("%H:%M"),
                        "Saída": saida.strftime("%H:%M")
                    })
        st.markdown("---")
        st.subheader("Informações Adicionais")
        ocorrencias = st.text_area("Ocorrências")
        nome_empresa = st.text_input("Responsável pela empresa")
        nome_fiscal = st.text_input("Nome da fiscalização")
        fotos = st.file_uploader("Fotos do serviço", accept_multiple_files=True, type=["png", "jpg", "jpeg"])
        if st.button("Salvar e Gerar Relatório"):
            temp_dir_obj_for_cleanup = None
            fotos_processed_paths = []
            try:
                if not obra or obra == "":
                    st.error("Por favor, selecione a 'Obra'.")
                    st.stop()
                if not contrato or contrato == "":
                    st.error("Por favor, selecione o 'Contrato'.")
                    st.stop()
                if not nome_empresa:
                    st.error("Por favor, preencha o campo 'Responsável pela empresa'.")
                    st.stop()
                registro = {
                    "Obra": obra,
                    "Local": local,
                    "Data": data.strftime("%d/%m/%Y"),
                    "Contrato": contrato,
                    "Clima": clima,
                    "Máquinas": maquinas,
                    "Serviços": servicos,
                    "Efetivo": json.dumps(efetivo_lista, ensure_ascii=False),
                    "Ocorrências": ocorrencias,
                    "Responsável Empresa": nome_empresa,
                    "Fiscalização": nome_fiscal
                }
                with st.spinner("Processando fotos..."):
                    fotos_processed_paths = processar_fotos(fotos, obra, data) if fotos else []
                    if fotos_processed_paths:
                        temp_dir_obj_for_cleanup = Path(fotos_processed_paths[0]).parent
                    elif fotos:
                        st.warning("Nenhuma foto foi processada corretamente. O PDF pode não conter imagens.")
                with st.spinner("Gerando PDF..."):
                    nome_pdf = f"Diario_{obra.replace(' ', '_')}_{data.strftime('%Y-%m-%d')}.pdf"
                    pdf_buffer = gerar_pdf(registro, fotos_processed_paths)
                    if pdf_buffer is None:
                        st.error("Falha ao gerar o PDF. Verifique os logs.")
                        st.stop()
                st.download_button(
                    label="📥 Baixar Relatório PDF",
                    data=pdf_buffer,
                    file_name=nome_pdf,
                    mime="application/pdf",
                    type="primary"
                )
# ... (depois de gerar o PDF e antes do envio de e-mail) ...
                with st.spinner("Enviando para Google Drive..."):
                    try:
                        # Recria o serviço sempre que for usar (seguro para múltiplos uploads)
                        service = build("drive", "v3", credentials=creds, static_discovery=False)
                        pdf_buffer.seek(0)
                        media = MediaIoBaseUpload(pdf_buffer, mimetype='application/pdf', resumable=True)
                        file_metadata = {'name': nome_pdf, 'parents': [DRIVE_FOLDER_ID]}
                        file = service.files().create(
                            body=file_metadata,
                            media_body=media,
                            fields='id',
                            supportsAllDrives=True
                        ).execute()
                        drive_id = file.get("id")
                        if drive_id:
                            st.success(f"PDF salvo no Google Drive! ID: {drive_id}")
                            st.markdown(f"[Abrir no Drive](https://drive.google.com/file/d/{drive_id}/view)")
                            # --- Envio de e-mail, se desejar ---
                            with st.spinner("Enviando e-mail..."):
                                assunto = f"Diário de Obra - {obra} ({data.strftime('%d/%m/%Y')})"
                                corpo = f"""
                                <p>Relatório diário gerado:</p>
                                <ul>
                                    <li>Obra: {obra}</li>
                                    <li>Data: {data.strftime('%d/%m/%Y')}</li>
                                    <li>Responsável: {nome_empresa}</li>
                                </ul>
                                """
                                if enviar_email(
                                    ["administrativo@rdvengenharia.com.br"],
                                    assunto, corpo, drive_id
                                ):
                                    st.success("E-mail enviado com sucesso!")
                                else:
                                    st.warning("PDF salvo no Drive, mas falha no envio do e-mail.")
                        else:
                            st.error("Upload feito, mas não foi possível recuperar o ID do arquivo no Google Drive.")
                    except Exception as e:
                        st.error(f"Falha no upload para o Google Drive. Erro: {e}")

            finally:
                try:
                    if temp_dir_obj_for_cleanup and temp_dir_obj_for_cleanup.exists():
                        shutil.rmtree(temp_dir_obj_for_cleanup)
                except Exception:
                    pass
                try:
                    if temp_icon_path_for_cleanup and os.path.exists(temp_icon_path_for_cleanup):
                        os.remove(temp_icon_path_for_cleanup)
                except Exception:
                    pass
