import os
import io
import json
import tempfile
import shutil
from datetime import datetime
from pathlib import Path
from PIL import Image as PILImage
from fpdf import FPDF
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.errors import HttpError
import yagmail
import streamlit as st

# ======= CONSTANTES =======
DRIVE_FOLDER_ID = "1BUgZRcBrKksC3eUytoJ5mv_nhMRdAv1d"
LOGO_PDF_PATH = "LOGO_RDV_AZUL.png"
temp_icon_path_for_cleanup = None

# ======= CREDENCIAIS GOOGLE =======
try:
    creds_dict = dict(st.secrets["google_service_account"])
    creds = service_account.Credentials.from_service_account_info(
        creds_dict, scopes=["https://www.googleapis.com/auth/drive"]
    )
except Exception as e:
    creds = None

# ======= CLASSE PDF FINAL =======
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

# ======= GERAÇÃO DE PDF =======
def gerar_pdf(registro, fotos_paths):
    pdf = DiarioObraPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)

    # Dados Gerais da Obra
    pdf.set_font('Arial', 'B', 11)
    pdf.set_text_color(0, 0, 0)
    campos = [
        ("OBRA:", registro.get("Obra", "")),
        ("LOCAL:", registro.get("Local", "")),
        ("DATA:", registro.get("Data", "")),
        ("CONTRATO:", registro.get("Contrato", "")),
        ("CLIMA:", registro.get("Clima", ""))
    ]
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
    pdf.multi_cell(0, 7, registro.get("Serviços", "Nenhum serviço informado.").strip() or "Nenhum serviço informado.", 0, 1)

    # Máquinas
    pdf.ln(2)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 7, 'MÁQUINAS/EQUIPAMENTOS:', 0, 1, 'L', True)
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 7, registro.get("Máquinas", "Nenhuma máquina/equipamento informado.").strip() or "Nenhuma máquina/equipamento informado.", 0, 1)

    # Efetivo de Pessoal
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
    try:
        efetivo_data = json.loads(registro.get("Efetivo", "[]"))
    except Exception:
        efetivo_data = []
    for item in efetivo_data:
        pdf.cell(70, 8, item.get("Nome", ""), 1)
        pdf.cell(40, 8, item.get("Função", ""), 1)
        pdf.cell(30, 8, item.get("Entrada", ""), 1)
        pdf.cell(30, 8, item.get("Saída", ""), 1)
        pdf.ln()
    pdf.ln(2)

    # Intercorrências
    pdf.set_font('Arial', 'B', 11)
    pdf.set_fill_color(220, 230, 242)
    pdf.cell(0, 7, 'INTERCORRÊNCIAS:', 0, 1, 'L', True)
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 7, registro.get("Ocorrências", "Sem intercorrências.").strip() or "Sem intercorrências.", 0, 1)
    pdf.ln(2)

    # Assinaturas
    pdf.set_font('Arial', 'B', 11)
    pdf.set_fill_color(220, 230, 242)
    pdf.cell(0, 7, 'ASSINATURAS:', 0, 1, 'L', True)
    pdf.ln(10)

    largura_linha = 60
    distancia_entre = 45
    largura_total = (2 * largura_linha) + distancia_entre
    x_inicio = (pdf.w - largura_total) / 2
    y_assin = pdf.get_y()
    pdf.set_draw_color(70, 70, 70)
    pdf.line(x_inicio, y_assin, x_inicio + largura_linha, y_assin)
    pdf.line(x_inicio + largura_linha + distancia_entre, y_assin,
             x_inicio + 2 * largura_linha + distancia_entre, y_assin)
    espaco_vertical = 3
    pdf.set_font('Arial', '', 11)
    pdf.set_xy(x_inicio, y_assin + espaco_vertical)
    pdf.cell(largura_linha, 7, "Responsável Técnico:", 0, 2, 'C')
    pdf.cell(largura_linha, 7, f"Nome: {registro.get('Responsável Empresa', '')}", 0, 0, 'C')
    pdf.set_xy(x_inicio + largura_linha + distancia_entre, y_assin + espaco_vertical)
    pdf.cell(largura_linha, 7, "Fiscalização:", 0, 2, 'C')
    pdf.cell(largura_linha, 7, f"Nome: {registro.get('Fiscalização', '')}", 0, 0, 'C')
    pdf.ln(20)

    # Fotos
    for path in fotos_paths:
        if os.path.exists(path):
            pdf.add_page()
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, f'Foto: {os.path.basename(path)}', 0, 1)
            pdf.image(path, x=30, w=150)

    pdf_buffer = io.BytesIO(pdf.output(dest='S').encode('latin1'))
    return pdf_buffer

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
        service = build("drive", "v3", credentials=creds, static_discovery=False, cache_discovery=False)
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
