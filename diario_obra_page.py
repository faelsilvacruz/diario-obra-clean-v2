import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path
from PIL import Image as PILImage
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor, black, lightgrey, white, darkgrey
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os
import io
import json
import yagmail
import tempfile
import shutil

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.errors import HttpError

# ======= CONSTANTES =======
DRIVE_FOLDER_ID = "1BUgZRcBrKksC3eUytoJ5mv_nhMRdAv1d"
LOGO_PDF_PATH = "LOGO_RDV_AZUL-sem fundo.png"

def gerar_pdf(registro, fotos_paths):
    buffer = io.BytesIO()
    try:
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        margem = 30

        def draw_text_area(canvas_obj, text, x, y, max_width, line_height=14):
            styles = getSampleStyleSheet()
            style = styles['Normal']
            style.fontSize = 10
            style.leading = line_height
            p = Paragraph(text.replace('\n', '<br/>'), style)
            text_width, text_height = p.wrapOn(canvas_obj, max_width, A4[1])
            actual_y = y - text_height
            p.drawOn(canvas_obj, x, actual_y)
            return actual_y - line_height

        def draw_footer(c, width, margem, y, registro):
            footer_h = 80
            if y < (margem + footer_h + 20):
                c.showPage()
                y = A4[1] - margem
            c.setFont("Helvetica", 9)
            c.setFillColor(darkgrey)
            c.rect(margem, margem, width - 2*margem, 70)
            c.line(margem + 50, margem + 45, margem + 200, margem + 45)
            c.drawCentredString(margem + 125, margem + 30, "Responsável Técnico")
            c.drawCentredString(margem + 125, margem + 15, f"Nome: {registro.get('Responsável Empresa', 'Engenheiro')}")
            c.line(width - margem - 200, margem + 45, width - margem - 50, margem + 45)
            c.drawCentredString(width - margem - 125, margem + 30, "Fiscalização")
            c.drawCentredString(width - margem - 125, margem + 15, f"Nome: {registro.get('Fiscalização', 'Conforme assinatura')}")
            c.setFillColor(black)
            c.drawString(margem + 5, margem + 5, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            return margem

        draw_header(c, width, height, LOGO_PDF_PATH)
        y = height - 100
        y = draw_info_table(c, registro, width, height, y, margem)
        y -= 20
        draw_footer(c, width, margem, y, registro)
        c.save()
        buffer.seek(0)
        return buffer
    except Exception as e:
        print("Erro ao gerar PDF:", e)
        return None

def draw_header(c, width, height, logo_path):
    c.setFillColor(HexColor("#0F2A4D"))
    c.rect(0, height-80, width, 80, fill=True, stroke=False)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height-50, "DIÁRIO DE OBRA")
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, height-70, "RDV ENGENHARIA")
    if os.path.exists(logo_path):
        try:
            logo = ImageReader(logo_path)
            c.drawImage(logo, 30, height-70, width=100, height=50, preserveAspectRatio=True)
        except Exception:
            pass

def draw_info_table(c, registro, width, height, y, margem):
    data = [
        ["OBRA:", registro.get("Obra", "N/A")],
        ["LOCAL:", registro.get("Local", "N/A")],
        ["DATA:", registro.get("Data", "N/A")],
        ["CONTRATO:", registro.get("Contrato", "N/A")]
    ]
    col2_width = width - 100 - (2 * margem)
    table = Table(data, colWidths=[100, col2_width])
    table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6)
    ]))
    table_width, table_height = table.wrapOn(c, width - 2*margem, height)
    table.drawOn(c, margem, y - table_height)
    return y - table_height - 10

def upload_para_drive(pdf_buffer, nome_arquivo, creds):
    try:
        pdf_buffer.seek(0)
        service = build("drive", "v3", credentials=creds, static_discovery=False)
        media = MediaIoBaseUpload(pdf_buffer, mimetype='application/pdf', resumable=True)
        file_metadata = {'name': nome_arquivo, 'parents': [DRIVE_FOLDER_ID]}
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id',
            supportsAllDrives=True
        ).execute()
        return file.get("id")
    except HttpError as error:
        st.error(f"Erro HTTP no Google Drive: {error}")
        return None

def enviar_email(destinatarios, assunto, corpo_html, drive_id=None, email_secrets=None):
    try:
        yag = yagmail.SMTP(
            user=email_secrets["user"],
            password=email_secrets["password"],
            host='smtp.gmail.com',
            port=587,
            smtp_starttls=True,
            smtp_ssl=False,
            timeout=30
        )
        corpo = f"""
        <html>
            <body>
                {corpo_html}
                {f'<p><a href="https://drive.google.com/file/d/{drive_id}/view">Ver no Drive</a></p>' if drive_id else ''}
                <p style="color: #888; font-size: 0.8em;">Enviado automaticamente - Sistema RDV Engenharia</p>
            </body>
        </html>
        """
        yag.send(to=destinatarios, subject=assunto, contents=corpo)
        return True
    except Exception as e:
        st.error(f"Erro no envio de e-mail: {e}")
        return False

def render_diario_obra_page():
    st.title("Relatório Diário de Obra - RDV Engenharia")
    st.subheader("Preenchimento")

    obras_df = pd.read_csv("obras.csv")
    contratos_df = pd.read_csv("contratos.csv")
    colab_df = pd.read_csv("colaboradores.csv")

    obras = [""] + obras_df["Nome"].tolist()
    contratos = [""] + contratos_df["Nome"].tolist()
    colaboradores = [""] + colab_df["Nome"].tolist()

    obra = st.selectbox("Obra", obras)
    local = st.text_input("Local")
    data = st.date_input("Data", datetime.today())
    contrato = st.selectbox("Contrato", contratos)
    clima = st.selectbox("Condições do dia", ["Bom", "Chuva", "Garoa", "Impraticável", "Feriado", "Guarda"])
    maquinas = st.text_area("Máquinas e equipamentos")
    servicos = st.text_area("Serviços executados")
    ocorrencias = st.text_area("Ocorrências")
    responsavel = st.text_input("Responsável pela empresa")
    fiscal = st.text_input("Fiscalização")
    fotos = st.file_uploader("Fotos do serviço", accept_multiple_files=True, type=["png", "jpg", "jpeg"])

    num_colabs = st.number_input("Número de colaboradores", min_value=1, max_value=30, value=5, step=1)
    efetivo = []
    for i in range(int(num_colabs)):
        col1, col2, col3, col4 = st.columns(4)
        nome = col1.selectbox(f"Nome {i+1}", colaboradores, key=f"nome_{i}")
        funcao = ""
        if nome:
            match = colab_df.loc[colab_df["Nome"] == nome]
            if not match.empty:
                funcao = match.iloc[0]["Função"]
        col2.text(f"Função: {funcao}")
        entrada = col3.time_input(f"Entrada {i+1}", value=datetime.strptime("08:00", "%H:%M").time(), key=f"ent_{i}")
        saida = col4.time_input(f"Saída {i+1}", value=datetime.strptime("17:00", "%H:%M").time(), key=f"sai_{i}")
        efetivo.append({
            "Nome": nome,
            "Função": funcao,
            "Entrada": entrada.strftime("%H:%M"),
            "Saída": saida.strftime("%H:%M")
        })

    if st.button("Salvar e Gerar Relatório"):
        registro = {
            "Obra": obra,
            "Local": local,
            "Data": data.strftime("%d/%m/%Y"),
            "Contrato": contrato,
            "Clima": clima,
            "Máquinas": maquinas,
            "Serviços": servicos,
            "Efetivo": json.dumps(efetivo, ensure_ascii=False),
            "Ocorrências": ocorrencias,
            "Responsável Empresa": responsavel,
            "Fiscalização": fiscal
        }

        creds_dict = dict(st.secrets["google_service_account"])
        creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=["https://www.googleapis.com/auth/drive"])

        fotos_processadas = []
        temp_dir = Path(tempfile.mkdtemp())
        for i, foto in enumerate(fotos):
            temp_path = temp_dir / f"foto_{i+1}.jpg"
            with open(temp_path, "wb") as f:
                f.write(foto.getbuffer())
            fotos_processadas.append(str(temp_path))

        pdf_buffer = gerar_pdf(registro, fotos_processadas)
        nome_pdf = f"Diario_{obra.replace(' ', '_')}_{data.strftime('%Y-%m-%d')}.pdf"

        st.download_button("📥 Baixar PDF", data=pdf_buffer, file_name=nome_pdf, mime="application/pdf")

        drive_id = upload_para_drive(pdf_buffer, nome_pdf, creds)
        if drive_id:
            st.success(f"PDF salvo no Drive com sucesso! ID: {drive_id}")

        enviar_email(["administrativo@rdvengenharia.com.br"], f"Diário de Obra - {obra} ({data.strftime('%d/%m/%Y')})", "<p>Relatório Diário enviado.</p>", drive_id, st.secrets["email"])

        shutil.rmtree(temp_dir)
