import os
import sqlite3
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import shutil

# ====== CONFIGURAÇÕES ======
CAMINHO_CREDENCIAL = r"C:\RDV_Automacoes\credenciais\service_account.json"
PASTA_ORIGEM = r"C:\RDV_Automacoes\saida"
PASTA_ENVIADOS = r"C:\RDV_Automacoes\enviado_google_drive"
CAMINHO_DB = r"C:\RDV_Automacoes\holerites.db"
GOOGLE_DRIVE_FOLDER_ID = "1VgWk-7lHIGgEOZli9dvU4eVUNYD_bUgq"

# ====== CONEXÃO COM GOOGLE DRIVE ======
creds = service_account.Credentials.from_service_account_file(
    CAMINHO_CREDENCIAL,
    scopes=['https://www.googleapis.com/auth/drive']
)
service = build('drive', 'v3', credentials=creds)

# ====== CONEXÃO COM BANCO DE DADOS ======
conn = sqlite3.connect(CAMINHO_DB)
cursor = conn.cursor()

# Criar tabela caso não exista
cursor.execute('''
    CREATE TABLE IF NOT EXISTS holerites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_colaborador TEXT,
        mes TEXT,
        ano TEXT,
        link_google_drive TEXT
    )
''')
conn.commit()

# ====== FUNÇÃO DE UPLOAD ======
def upload_para_drive(caminho_arquivo, nome_arquivo):
    file_metadata = {
        'name': nome_arquivo,
        'parents': [GOOGLE_DRIVE_FOLDER_ID]
    }
    media = MediaFileUpload(caminho_arquivo, mimetype='application/pdf')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    file_id = file.get('id')
    link = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"
    return link

# ====== PROCESSAMENTO DE UPLOAD ======
for nome_arquivo in os.listdir(PASTA_ORIGEM):
    if nome_arquivo.endswith('.pdf'):
        caminho_arquivo = os.path.join(PASTA_ORIGEM, nome_arquivo)
        print(f"Enviando: {nome_arquivo}")

        # Upload para o Drive
        link = upload_para_drive(caminho_arquivo, nome_arquivo)

        # Extrair nome, mês, ano
        partes = nome_arquivo.replace('.pdf', '').split('_')
        try:
            nome_colaborador = "_".join(partes[1:-2]).replace("_", " ")
            mes = partes[-2]
            ano = partes[-1]
        except:
            nome_colaborador = "Desconhecido"
            mes = "Mês"
            ano = "Ano"

        # Gravar no banco
        cursor.execute('''
            INSERT INTO holerites (nome_colaborador, mes, ano, link_google_drive)
            VALUES (?, ?, ?, ?)
        ''', (nome_colaborador, mes, ano, link))
        conn.commit()

        # Mover o arquivo
        shutil.move(caminho_arquivo, os.path.join(PASTA_ENVIADOS, nome_arquivo))

print("Upload finalizado com sucesso!")

conn.close()
