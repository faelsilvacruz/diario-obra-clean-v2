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
import yagmail
import streamlit as st

LOGO_PDF_PATH = "LOGO_RDV_AZUL-sem fundo.png"

def gerar_pdf(registro, fotos_paths):
    buffer = io.BytesIO()
    try:
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        margem = 30

        def draw_text_area(c, text, x, y_start, width_max, font_size=10, line_height=14):
            styles = getSampleStyleSheet()
            style = ParagraphStyle(
                'Custom',
                fontName='Helvetica',
                fontSize=font_size,
                leading=line_height
            )
            text = text.replace('\\n', '<br/>')
            p = Paragraph(text, style)
            text_width, text_height = p.wrapOn(c, width_max, A4[1])
            actual_y = y_start - text_height
            p.drawOn(c, x, actual_y)
            return actual_y - line_height

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

        y = draw_text_area(c, f"Máquinas e Equipamentos:\\n{registro.get('Máquinas', '')}", margem, y, width - 2*margem)
        y = draw_text_area(c, f"Serviços Executados:\\n{registro.get('Serviços', '')}", margem, y, width - 2*margem)

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
            ('ALIGN', (0,0), (-1,0), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, lightgrey),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
        ]))
        table_width, table_height = table.wrapOn(c, width - 2*margem, height)
        table.drawOn(c, margem, y - table_height)
        y -= table_height + 10

        y = draw_text_area(c, f"Controle de Documentação de Segurança:\\n"
                              f"Hora de Liberação da LT: {registro.get('Hora LT', '')}\\n"
                              f"Hora de Liberação da APR: {registro.get('Hora APR', '')}\\n"
                              f"Data da APR vigente: {registro.get('Data APR', '')}\\n"
                              f"Número/Código da APR: {registro.get('Numero APR', '')}",
                              margem, y, width - 2*margem)

        y = draw_text_area(c, f"Ocorrências:\\n{registro.get('Ocorrências', '')}", margem, y, width - 2*margem)

        footer_h = 80
        c.setFont("Helvetica", 9)
        c.setFillColor(darkgrey)
        c.rect(margem, margem, width - 2*margem, 70)
        c.line(margem + 50, margem + 45, margem + 200, margem + 45)
        c.drawCentredString(margem + 125, margem + 30, "Responsável Técnico")
        c.drawCentredString(margem + 125, margem + 15, f"Nome: {registro.get('Responsável Empresa', '')}")
        c.line(width - margem - 200, margem + 45, width - margem - 50, margem + 45)
        c.drawCentredString(width - margem - 125, margem + 30, "Fiscalização")
        c.drawCentredString(width - margem - 125, margem + 15, f"Nome: {registro.get('Fiscalização', '')}")

        c.setFillColor(black)
        c.drawString(margem + 5, margem + 5, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

        c.save()
        buffer.seek(0)
        return buffer
    except Exception as e:
        print(f"Erro ao gerar PDF: {e}")
        return None
        def gerar_pdf_holerite(registro):
    buffer = io.BytesIO()
    try:
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        margem = 30

        c.setFillColor(HexColor("#0F2A4D"))
        c.rect(0, height - 80, width, 80, fill=True, stroke=False)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(width / 2, height - 50, "HOLERITE")
        c.setFont("Helvetica", 12)
        c.drawCentredString(width / 2, height - 70, "RDV ENGENHARIA")
        if os.path.exists(LOGO_PDF_PATH):
            try:
                logo = ImageReader(LOGO_PDF_PATH)
                c.drawImage(logo, 30, height - 70, width=100, height=50, preserveAspectRatio=True)
            except Exception:
                pass

        y = height - 100

        info_data = [
            ["Nome:", registro.get("Nome", "N/A")],
            ["Matrícula:", registro.get("Matricula", "N/A")],
            ["Competência:", registro.get("Competencia", "N/A")],
            ["Cargo:", registro.get("Cargo", "N/A")],
            ["Setor:", registro.get("Setor", "N/A")],
            ["Salário Base:", registro.get("Salario Base", "N/A")],
            ["Horas Extras:", registro.get("Horas Extras", "N/A")],
            ["Descontos:", registro.get("Descontos", "N/A")],
            ["Salário Líquido:", registro.get("Salario Liquido", "N/A")]
        ]

        col2_width = width - 100 - (2 * margem)
        table = Table(info_data, colWidths=[150, col2_width])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6)
        ]))
        table_width, table_height = table.wrapOn(c, width - 2 * margem, height)
        table.drawOn(c, margem, y - table_height)
        y -= table_height + 10

        c.setFillColor(black)
        c.drawString(margem + 5, margem + 5, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

        c.save()
        buffer.seek(0)
        return buffer
    except Exception as e:
        print(f"Erro ao gerar PDF do holerite: {e}")
        return None

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

def enviar_email(destinatarios, assunto, corpo_html, pdf_buffer=None, nome_pdf=None):
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

        attachments = []
        if pdf_buffer and nome_pdf:
            temp_pdf_path = f"/tmp/{nome_pdf}"
            with open(temp_pdf_path, "wb") as f:
                f.write(pdf_buffer.read())
            attachments.append(temp_pdf_path)

        corpo = f\"\"\"\
        <html>
            <body>
                {corpo_html}
                <p style="color: #888; font-size: 0.8em;">Enviado automaticamente - Sistema RDV Engenharia</p>
            </body>
        </html>
        \"\"\" 

        yag.send(
            to=destinatarios,
            subject=assunto,
            contents=[corpo] + attachments
        )
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False
        
