import os
import io
from datetime import datetime
from pathlib import Path
from PIL import Image as PILImage
from fpdf import FPDF
import tempfile
import shutil
import yagmail
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor, black, lightgrey, white, darkgrey
from reportlab.platypus import Table, TableStyle

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

    # Dados da Obra
    pdf.set_font('Arial', 'B', 11)
    campos = [("OBRA:", dados_obra.get("obra", "")),
              ("LOCAL:", dados_obra.get("local", "")),
              ("DATA:", dados_obra.get("data", "")),
              ("CONTRATO:", dados_obra.get("contrato", "")),
              ("CLIMA:", clima)]
    for rotulo, valor in campos:
        pdf.cell(25, 8, rotulo, 0, 0)
        pdf.set_font('Arial', '', 11)
        pdf.cell(80, 8, valor, 0, 1)
        pdf.set_font('Arial', 'B', 11)

    # Serviços Executados
    pdf.ln(3)
    pdf.set_fill_color(220, 230, 242)
    pdf.cell(0, 7, 'SERVIÇOS EXECUTADOS:', 0, 1, 'L', True)
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 7, servicos.strip() if servicos.strip() else "Nenhum serviço informado.", 0, 1)

    # Máquinas
    pdf.ln(2)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 7, 'MÁQUINAS/EQUIPAMENTOS:', 0, 1, 'L', True)
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 7, maquinas.strip() if maquinas.strip() else "Nenhuma máquina/equipamento informado.", 0, 1)

    # Efetivo
    pdf.ln(2)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 7, 'EFETIVO DE PESSOAL', 0, 1, 'L', True)
    pdf.set_fill_color(15, 42, 77)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(70, 8, 'NOME', 1, 0, 'C', True)
    pdf.cell(40, 8, 'FUNÇÃO', 1, 0, 'C', True)
    pdf.cell(30, 8, 'ENTRADA', 1, 0, 'C', True)
    pdf.cell(30, 8, 'SAÍDA', 1, 1, 'C', True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', '', 9)
    for row in colaboradores:
        pdf.cell(70, 8, row[0], 1)
        pdf.cell(40, 8, row[1], 1)
        pdf.cell(30, 8, row[2], 1)
        pdf.cell(30, 8, row[3], 1)
        pdf.ln()
    pdf.ln(2)

    # Controle de Documentação
    pdf.set_font('Arial', 'B', 11)
    pdf.set_fill_color(220, 230, 242)
    pdf.cell(0, 7, 'CONTROLE DE DOCUMENTAÇÃO DE SEGURANÇA:', 0, 1, 'L', True)
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 7, controle_doc.strip() if controle_doc.strip() else "Não informado.", 0, 1)
    pdf.ln(2)

    # Intercorrências
    pdf.set_font('Arial', 'B', 11)
    pdf.set_fill_color(220, 230, 242)
    pdf.cell(0, 7, 'INTERCORRÊNCIAS:', 0, 1, 'L', True)
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 7, intercorrencias.strip() if intercorrencias.strip() else "Sem intercorrências.", 0, 1)
    pdf.ln(2)

    # Assinaturas
    pdf.set_font('Arial', 'B', 11)
    pdf.set_fill_color(220, 230, 242)
    pdf.cell(0, 7, 'ASSINATURAS:', 0, 1, 'L', True)
    pdf.ln(10)
    largura_linha = 60
    distancia_entre = 45
    x_inicio = (pdf.w - (2 * largura_linha + distancia_entre)) / 2
    y_assin = pdf.get_y()
    pdf.set_draw_color(70, 70, 70)
    pdf.line(x_inicio, y_assin, x_inicio + largura_linha, y_assin)
    pdf.line(x_inicio + largura_linha + distancia_entre, y_assin, x_inicio + 2 * largura_linha + distancia_entre, y_assin)
    pdf.set_font('Arial', '', 11)
    pdf.set_xy(x_inicio, y_assin + 3)
    pdf.cell(largura_linha, 7, "Responsável Técnico:", 0, 2, 'C')
    pdf.cell(largura_linha, 7, f"Nome: {responsavel}", 0, 0, 'C')
    pdf.set_xy(x_inicio + largura_linha + distancia_entre, y_assin + 3)
    pdf.cell(largura_linha, 7, "Fiscalização:", 0, 2, 'C')
    pdf.cell(largura_linha, 7, f"Nome: {fiscal}", 0, 0, 'C')
    pdf.ln(20)

    # Fotos
    if fotos_paths:
        for path in fotos_paths:
            if os.path.exists(path):
                pdf.add_page()
                pdf.set_font('Arial', 'B', 12)
                pdf.cell(0, 10, f'Foto: {os.path.basename(path)}', 0, 1)
                pdf.image(path, x=30, w=150)

    return io.BytesIO(pdf.output(dest='S').encode('latin1'))

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
