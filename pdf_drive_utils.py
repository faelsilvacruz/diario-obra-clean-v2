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

# ======= CONSTANTES =======
LOGO_PDF_PATH = "LOGO_RDV_AZUL-sem fundo.png"

# ======= PDF DIÁRIO DE OBRA =======
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

        # Informações gerais
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

        # Máquinas
        maquinas_txt = registro.get('Máquinas', '').strip() or 'Nenhuma máquina/equipamento informado.'
        y = draw_text_area(c, f"Máquinas e Equipamentos:\n{maquinas_txt}", margem, y, width - 2*margem)

        # Serviços
        servicos_txt = registro.get('Serviços', '').strip() or 'Nenhum serviço executado informado.'
        y = draw_text_area(c, f"Serviços Executados:\n{servicos_txt}", margem, y, width - 2*margem)

        # Efetivo
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

        # Ocorrências
        ocorrencias_txt = registro.get('Ocorrências', '').strip() or 'Nenhuma ocorrência informada.'
        y = draw_text_area(c, f"Ocorrências:\n{ocorrencias_txt}", margem, y, width - 2*margem)

        # Rodapé
        c.setFont("Helvetica", 8)
        c.drawString(margem, 40, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
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

# ======= ENVIO DE E-MAIL =======
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
        corpo = f"""
        <html>
            <body>
                {corpo_html}
                <p style="color: #888; font-size: 0.8em;">Enviado automaticamente - Sistema RDV Engenharia</p>
            </body>
        </html>
        """
        yag.send(
            to=destinatarios,
            subject=assunto,
            contents=[corpo] + attachments
        )
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False

# ======= GERAR PDF HOLERITE =======
def gerar_pdf_holerite(dados_colaborador):
    try:
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        largura, altura = A4
        margem = 30

        if os.path.exists(LOGO_PDF_PATH):
            try:
                logo = ImageReader(LOGO_PDF_PATH)
                c.drawImage(logo, margem, altura - 70, width=100, height=40, preserveAspectRatio=True)
            except Exception as e:
                print(f"Erro ao carregar logo: {e}")

        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(HexColor("#0F2A4D"))
        c.drawString(150, altura - 50, "HOLERITE - RDV Engenharia")
        c.setFillColor(black)

        y = altura - 100
        linha_espaco = 18
        campos = [
            ("Colaborador", dados_colaborador["Nome"]),
            ("Salário Base", f"R$ {dados_colaborador['Salario Base']:.2f}"),
            ("Horas Extras", f"R$ {dados_colaborador['Horas Extras']:.2f}"),
            ("Vale Alimentação", f"R$ {dados_colaborador['Vale Alimentacao']:.2f}"),
            ("Descontos", f"R$ {dados_colaborador['Descontos']:.2f}"),
            ("Salário Líquido", f"R$ {dados_colaborador['Liquido']:.2f}"),
        ]

        for label, valor in campos:
            c.setFont("Helvetica-Bold", 10)
            c.drawString(margem, y, f"{label}:")
            c.setFont("Helvetica", 10)
            c.drawString(150, y, valor)
            y -= linha_espaco

        c.setFont("Helvetica", 8)
        c.drawString(margem, 40, f"Gerado automaticamente em {datetime.now().strftime('%d/%m/%Y %H:%M')} - RDV Engenharia")
        c.save()
        buffer.seek(0)
        return buffer
    except Exception as e:
        print(f"Erro ao gerar PDF do holerite: {e}")
        return None
