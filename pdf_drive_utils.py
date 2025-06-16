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

import os
import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import black, lightgrey
from PIL import Image as PILImage

LOGO_PDF_PATH = "LOGO_RDV_AZUL-sem fundo.png"

def gerar_pdf(registro, fotos_paths):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    margem = 30
    y = height - margem

    # Função para adicionar uma linha de texto
    def linha(texto, tamanho=10, negrito=False, espaco=15):
        nonlocal y
        if y < 50:
            c.showPage()
            y = height - margem
        if negrito:
            c.setFont("Helvetica-Bold", tamanho)
        else:
            c.setFont("Helvetica", tamanho)
        c.drawString(margem, y, texto)
        y -= espaco

    # LOGO
    try:
        if os.path.exists(LOGO_PDF_PATH):
            logo = ImageReader(LOGO_PDF_PATH)
            c.drawImage(logo, margem, y - 50, width=120, height=40, mask='auto')
    except Exception as e:
        print(f"Erro ao inserir logo: {e}")

    y -= 60
    linha("DIÁRIO DE OBRA", tamanho=14, negrito=True, espaco=20)

    # Cabeçalho geral
    for campo in ["Obra", "Local", "Data", "Contrato", "Clima"]:
        valor = registro.get(campo, "")
        if valor:
            linha(f"{campo.upper()}: {valor}", tamanho=10, negrito=True)

    # Máquinas
    linha("")
    linha("Máquinas e Equipamentos:", negrito=True)
    linha(registro.get("Máquinas", " - "))

    # Serviços Executados
    linha("")
    linha("Serviços Executados:", negrito=True)
    linha(registro.get("Serviços", " - "), tamanho=10, espaco=15)

    # Lista de Colaboradores
    colaboradores = registro.get("Colaboradores", [])
    if colaboradores:
        linha("")
        linha("NOME              FUNÇÃO              ENTRADA   SAÍDA", tamanho=10, negrito=True)
        for colab in colaboradores:
            nome = colab.get("Nome", "")
            funcao = colab.get("Função", "")
            entrada = colab.get("Entrada", "")
            saida = colab.get("Saída", "")
            linha(f"{nome:<20} {funcao:<20} {entrada:<8} {saida:<8}", tamanho=9, espaco=12)

    # Controle de Documentação
    linha("")
    linha("Controle de Documentação de Segurança:", negrito=True)
    linha(f"Hora de Liberação da LT: {registro.get('Hora_LT', '')}")
    linha(f"Hora de Liberação da APR: {registro.get('Hora_APR', '')}")
    linha(f"Data da APR vigente: {registro.get('Data_APR', '')}")
    linha(f"Número/Código da APR: {registro.get('Codigo_APR', '')}")

    # Ocorrências
    linha("")
    linha("Ocorrências:", negrito=True)
    linha(registro.get("Ocorrencias", " - "), tamanho=10, espaco=15)

    # Responsável Técnico
    linha("")
    linha("Responsável Técnico", negrito=True)
    linha(f"Nome: {registro.get('Responsavel', '')}")

    # Fiscalização
    linha("")
    linha("Fiscalização", negrito=True)
    linha(f"Nome: {registro.get('Fiscalizacao', '')}")

    # Rodapé - Data de Geração
    c.setFont("Helvetica-Oblique", 7)
    c.setFillColor(lightgrey)
    c.drawRightString(width - margem, margem, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    # Inserção das Fotos
    if fotos_paths:
        c.showPage()
        y = height - margem
        linha("REGISTRO FOTOGRÁFICO", tamanho=12, negrito=True, espaco=20)

        for foto_path in fotos_paths:
            try:
                img = PILImage.open(foto_path)
                img_width, img_height = img.size
                aspect = img_height / img_width

                max_width = width - 2 * margem
                max_height = 400

                final_width = max_width
                final_height = final_width * aspect

                if final_height > max_height:
                    final_height = max_height
                    final_width = final_height / aspect

                if y - final_height < margem:
                    c.showPage()
                    y = height - margem

                c.drawImage(foto_path, margem, y - final_height, width=final_width, height=final_height)
                y -= final_height + 20
            except Exception as e:
                print(f"Erro ao adicionar foto: {e}")

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
