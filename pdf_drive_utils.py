
import os
import io
import json
import tempfile
import shutil
from datetime import datetime
from pathlib import Path
from PIL import Image as PILImage
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor, black, lightgrey, white, darkgrey
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import yagmail
import streamlit as st

DRIVE_FOLDER_ID = "1BUgZRcBrKksC3eUytoJ5mv_nhMRdAv1d"
LOGO_PDF_PATH = "LOGO_RDV_AZUL-sem fundo.png"

try:
    creds_dict = dict(st.secrets["google_service_account"])
    creds = service_account.Credentials.from_service_account_info(
        creds_dict, scopes=["https://www.googleapis.com/auth/drive"]
    )
except Exception as e:
    creds = None

def gerar_pdf(registro, fotos_paths):
    buffer = io.BytesIO()
    try:
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        margem = 30

        def draw_text_area(c, text, x, y_start, width_max, font_size=10, line_height=14):
            styles = getSampleStyleSheet()
            style = ParagraphStyle('Custom', fontName='Helvetica', fontSize=font_size, leading=line_height)
            text = text.replace('\n', '<br/>')
            p = Paragraph(text, style)
            text_width, text_height = p.wrapOn(c, width_max, A4[1])
            actual_y = y_start - text_height
            p.drawOn(c, x, actual_y)
            return actual_y - line_height

        # Cabeçalho
        c.setFillColor(HexColor("#0F2A4D"))
        c.rect(0, height-80, width, 80, fill=True, stroke=False)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(width/2, height-50, "DIÁRIO DE OBRA")
        c.setFont("Helvetica", 12)
        c.drawCentredString(width/2, height-70, "RDV ENGENHARIA")
        if os.path.exists(LOGO_PDF_PATH):
            try:
                logo = ImageReader(LOGO_PDF_PATH)
                c.drawImage(logo, 30, height-70, width=100, height=50, preserveAspectRatio=True)
            except Exception:
                pass

        y = height - 100

        # Informações da Obra
        info_data = [
            ["OBRA:", registro.get("Obra", "N/A")],
            ["LOCAL:", registro.get("Local", "N/A")],
            ["DATA:", registro.get("Data", "N/A")],
            ["CONTRATO:", registro.get("Contrato", "N/A")],
            ["CLIMA:", registro.get("Clima", "N/A")]
        ]
        col2_width = width - 100 - (2 * margem)
        table = Table(info_data, colWidths=[100, col2_width])
        table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6)
        ]))
        table_width, table_height = table.wrapOn(c, width - 2*margem, height)
        table.drawOn(c, margem, y - table_height)
        y -= table_height + 10

        # Ocorrências
        ocorrencias_txt = registro.get('Ocorrências', '').strip() or 'Nenhuma ocorrência informada.'
        c.setFont("Helvetica-Bold", 10)
        c.drawString(margem, y - 10, "Ocorrências:")
        y -= 18
        y = draw_text_area(c, ocorrencias_txt, margem + 10, y, width - 2*margem - 20)

        c.save()
        buffer.seek(0)
        return buffer
    except Exception as e:
        print(f"Erro ao gerar PDF: {e}")
        return None

def processar_fotos(fotos_upload, obra_nome, data_relatorio):
    fotos_processadas_paths = []
    temp_dir_path_obj = None
    try:
        temp_dir_path_obj = Path(tempfile.mkdtemp(prefix="diario_obra_"))
        for i, foto_file in enumerate(fotos_upload):
            if foto_file is None:
                continue
            nome_foto_base = f"{obra_nome.replace(' ', '_')}_{data_relatorio.strftime('%Y-%m-%d')}_foto{i+1}"
            nome_foto_final = f"{nome_foto_base}{Path(foto_file.name).suffix}"
            caminho_foto_temp = temp_dir_path_obj / nome_foto_final
            with open(caminho_foto_temp, "wb") as f:
                f.write(foto_file.getbuffer())
            fotos_processadas_paths.append(str(caminho_foto_temp))
        return fotos_processadas_paths
    except Exception as e:
        print(f"Erro ao processar fotos: {e}")
        return []

def enviar_email(destinatarios, assunto, corpo_html, attachment=None, attachment_name="Relatorio.pdf"):
    try:
        yag = yagmail.SMTP(
            user=st.secrets["email"]["user"],
            password=st.secrets["email"]["password"],
            host='smtp.gmail.com',
            port=587,
            smtp_starttls=True,
            smtp_ssl=False,
            timeout=30
        )
        contents = [yagmail.inline(corpo_html)]
        if attachment is not None:
            attachment.seek(0)
            contents.append(attachment.read())
        yag.send(
            to=destinatarios,
            subject=assunto,
            contents=contents,
            attachments={attachment_name: attachment} if attachment else None
        )
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False
