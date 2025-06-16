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
import streamlit as st

# ======= CONSTANTES =======
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

        styles = getSampleStyleSheet()

        def draw_text_area(c, text, x, y_start, width_max, font_size=10, line_height=14):
            style = ParagraphStyle(
                'Custom',
                fontName='Helvetica',
                fontSize=font_size,
                leading=line_height
            )
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

        # Dados Gerais
        info_data = [
            ["OBRA:", registro.get("Obra", "N/A")],
            ["LOCAL:", registro.get("Local", "N/A")],
            ["DATA:", registro.get("Data", "N/A")],
            ["CONTRATO:", registro.get("Contrato", "N/A")]
        ]
        table = Table(info_data, colWidths=[100, width - 100 - 2*margem])
        table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6)
        ]))
        table.wrapOn(c, width - 2*margem, height)
        table.drawOn(c, margem, y - table._height)
        y -= table._height + 10

        # Clima
        box_clima_h = 25
        c.rect(margem, y - box_clima_h, width - 2*margem, box_clima_h)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(margem + 5, y - 15, "Condições do dia:")
        c.setFont("Helvetica", 11)
        c.drawString(margem + 120, y - 15, registro.get('Clima', 'N/A'))
        y -= (box_clima_h + 8)

        # Máquinas
        maquinas_txt = registro.get('Máquinas', '').strip() or 'Nenhuma máquina/equipamento informado.'
        y = draw_text_area(c, f"Máquinas e Equipamentos:\n{maquinas_txt}", margem, y, width - 2*margem)

        # Serviços
        servicos_txt = registro.get('Serviços', '').strip() or 'Nenhum serviço executado informado.'
        y = draw_text_area(c, f"Serviços Executados:\n{servicos_txt}", margem, y, width - 2*margem)

        # Efetivo
        c.setFont("Helvetica-Bold", 10)
        c.drawString(margem, y - 10, "Efetivo de Pessoal:")
        y -= 18
        try:
            efetivo_data = json.loads(registro.get("Efetivo", "[]"))
        except Exception:
            efetivo_data = []
        data_efetivo = [["NOME", "FUNÇÃO", "ENTRADA", "SAÍDA"]]
        for item in efetivo_data:
            data_efetivo.append([
                item.get("Nome", ""),
                item.get("Função", ""),
                item.get("Entrada", ""),
                item.get("Saída", "")
            ])
        while len(data_efetivo) < 7:
            data_efetivo.append(["", "", "", ""])
        table = Table(data_efetivo, colWidths=[150, 100, 65, 65])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), HexColor("#0F2A4D")),
            ('TEXTCOLOR', (0,0), (-1,0), white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 9),
            ('FONTSIZE', (0,1), (-1,-1), 8),
            ('GRID', (0,0), (-1,-1), 0.5, lightgrey),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
        ]))
        table.wrapOn(c, width - 2*margem, height)
        table.drawOn(c, margem, y - table._height)
        y -= table._height + 10

        # Ocorrências
        ocorrencias_txt = registro.get('Ocorrências', '').strip() or 'Nenhuma ocorrência informada.'
        y = draw_text_area(c, f"Ocorrências:\n{ocorrencias_txt}", margem, y, width - 2*margem)

        # Fiscalização
        fiscal_txt = registro.get('Fiscalização', '').strip() or 'N/A'
        y = draw_text_area(c, f"Fiscalização:\n{fiscal_txt}", margem, y, width - 2*margem)

        # Rodapé
        c.setFont("Helvetica", 9)
        c.setFillColor(darkgrey)
        c.rect(margem, margem, width - 2*margem, 70)
        c.setFillColor(black)
        c.drawString(margem + 5, margem + 5, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

        # Fotos
        for i, foto_path in enumerate(fotos_paths):
            try:
                if not Path(foto_path).exists():
                    continue
                c.showPage()
                y_foto = height - margem
                c.setFont("Helvetica-Bold", 12)
                c.drawString(margem, y_foto, f"📷 Foto {i+1}: {Path(foto_path).name}")
                img = PILImage.open(foto_path)
                img_width, img_height = img.size
                max_img_width = width - 2*margem
                max_img_height = height - 2*margem
                aspect_ratio = img_width / img_height
                if img_width > max_img_width or img_height > max_img_height:
                    if (max_img_width / aspect_ratio) <= max_img_height:
                        new_width = max_img_width
                        new_height = max_img_width / aspect_ratio
                    else:
                        new_height = max_img_height
                        new_width = max_img_height * aspect_ratio
                    img = img.resize((int(new_width), int(new_height)), PILImage.Resampling.LANCZOS)
                x_pos = margem + (max_img_width - new_width) / 2
                y_pos = y_foto - new_height - 10
                c.drawImage(ImageReader(img), x_pos, y_pos, width=new_width, height=new_height)
            except Exception:
                continue

        c.save()
        buffer.seek(0)
        return buffer
    except Exception as e:
        print(f"Erro ao gerar PDF: {e}")
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

# ======= UPLOAD GOOGLE DRIVE =======
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

# ======= ENVIO DE EMAIL =======
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
