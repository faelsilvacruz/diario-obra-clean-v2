import os
import io
import tempfile
import shutil
from datetime import datetime
from pathlib import Path
from PIL import Image as PILImage
from fpdf import FPDF
import yagmail
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor, black, lightgrey, white, darkgrey
from reportlab.platypus import Table, TableStyle

# ====================================
# Função: gerar_pdf - DIÁRIO DE OBRA
# ====================================

LOGO_PDF_PATH = "LOGO_RDV_AZUL.png"

class DiarioObraPDF(FPDF):
    def header(self):
        self.set_fill_color(15, 42, 77)
        self.rect(0, 0, self.w, 35, 'F')
        if os.path.exists(LOGO_PDF_PATH):
            self.image(LOGO_PDF_PATH, 12, 8, 19, 13)
        self.set_xy(0, 10)
        self.set_font('Arial', 'B', 17)
        self.set_text_color(255, 255, 255)
        self.cell(self.w, 10, 'DIÁRIO DE OBRA', border=0, ln=2, align='C')
        self.set_font('Arial', 'B', 12)
        self.cell(self.w, 7, 'RDV ENGENHARIA', border=0, ln=1, align='C')
        self.ln(7)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(130, 130, 130)
        self.cell(0, 6, f'Gerado em: {datetime.now().strftime("%d/%m/%Y %H:%M")} - Página {self.page_no()}', 0, 0, 'R')

def gerar_pdf(dados_obra, colaboradores, maquinas, servicos, controle_doc, intercorrencias, responsavel, fiscal, clima, fotos_paths=None):
    pdf = DiarioObraPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)
    # (Aqui entra o conteúdo completo da função gerar_pdf, igual ao layout final com Controle de Documentação de Segurança, colaboradores, fotos, etc.)
    return io.BytesIO(pdf.output(dest='S').encode('latin1'))

# ====================================
# Função: gerar_pdf_holerite
# ====================================
def gerar_pdf_holerite(registro):
    buffer = io.BytesIO()
    try:
        c = canvas.Canvas(buffer, pagesize=A4)
        # Aqui todo o conteúdo de geração de holerite com ReportLab (margens, cabeçalho, dados do colaborador, etc)
        c.save()
        buffer.seek(0)
        return buffer
    except Exception as e:
        print(f"Erro ao gerar PDF do holerite: {e}")
        return None

# ====================================
# Função: processar_fotos
# ====================================
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

# ====================================
# Função: enviar_email
# ====================================
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
        corpo = f"""<html><body>{corpo_html}<p style='color: #888; font-size: 0.8em;'>Enviado automaticamente - Sistema RDV Engenharia</p></body></html>"""
        yag.send(to=destinatarios, subject=assunto, contents=[corpo] + attachments)
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False
