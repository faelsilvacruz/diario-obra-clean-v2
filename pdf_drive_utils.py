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
from googleapiclient.errors import HttpError
import yagmail

# ======= CONSTANTES GLOBAIS =======
DRIVE_FOLDER_ID = "1BUgZRcBrKksC3eUytoJ5mv_nhMRdAv1d"
LOGO_PDF_PATH = "LOGO_RDV_AZUL-sem fundo.png"
temp_icon_path_for_cleanup = None

# ======= CREDENCIAIS GOOGLE =======
try:
    creds_dict = dict(st.secrets["google_service_account"])
    creds = service_account.Credentials.from_service_account_info(
        creds_dict, scopes=["https://www.googleapis.com/auth/drive"]
    )
except Exception as e:
    creds = None

# ======= GERAÇÃO DE PDF =======
def gerar_pdf(registro, fotos_paths):
    buffer = io.BytesIO()
    try:
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        margem = 30

        def draw_text_area_with_wrap(canvas_obj, text, x, y_start, max_width, line_height=14, font_size=10):
            styles = getSampleStyleSheet()
            style = styles['Normal']
            style.fontSize = font_size
            style.leading = line_height
            style.fontName = "Helvetica"
            text = text.replace('\n', '<br/>')
            p = Paragraph(text, style)
            text_width, text_height = p.wrapOn(canvas_obj, max_width, A4[1])
            actual_y_start = y_start - text_height
            p.drawOn(canvas_obj, x, actual_y_start)
            return actual_y_start - line_height

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
        # Aqui você pode incluir as chamadas para outras partes do layout (info, clima, máquinas, etc)
        draw_footer(c, width, margem, y, registro)

        c.save()
        buffer.seek(0)
        return buffer
    except Exception as e:
        print("Erro ao gerar PDF:", e)
        return None

# ======= PROCESSAR FOTOS =======
def processar_fotos(fotos_upload, obra_nome, data_relatorio):
    fotos_processadas_paths = []
    temp_dir_path_obj = None
    try:
        temp_dir_path_obj = Path(tempfile.mkdtemp(prefix="diario_obra_"))
        for i, foto_file in enumerate(fotos_upload):
            if foto_file is None:
                continue
            try:
                nome_foto_base = f"{obra_nome.replace(' ', '_')}_{data_relatorio.strftime('%Y-%m-%d')}_foto{i+1}"
                nome_foto_final = f"{nome_foto_base}{Path(foto_file.name).suffix}"
                caminho_foto_temp = temp_dir_path_obj / nome_foto_final
                with open(caminho_foto_temp, "wb") as f:
                    f.write(foto_file.getbuffer())
                if not caminho_foto_temp.exists():
                    raise FileNotFoundError()
                img = PILImage.open(caminho_foto_temp)
                img.thumbnail((1200, 1200), PILImage.Resampling.LANCZOS)
                img.save(caminho_foto_temp, "JPEG", quality=85)
                fotos_processadas_paths.append(str(caminho_foto_temp))
            except Exception:
                continue
        return fotos_processadas_paths
    except Exception:
        if temp_dir_path_obj and temp_dir_path_obj.exists():
            shutil.rmtree(temp_dir_path_obj)
        return []

# ======= UPLOAD PARA GOOGLE DRIVE =======
def upload_para_drive_seguro(pdf_buffer, nome_arquivo):
    try:
        if creds is None:
            raise Exception("Credenciais do Google Drive não carregadas.")
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
    except Exception as e:
        print(f"Erro no upload para o Google Drive: {e}")
        return None

# ======= ENVIO DE E-MAIL =======
def enviar_email(destinatarios, assunto, corpo_html, drive_id=None):
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
        print(f"Erro ao enviar e-mail: {e}")
        return False
