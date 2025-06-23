import io
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import streamlit as st

# ===== CONFIGURAÇÕES =====
DRIVE_FOLDER_ID = 'SEU_ID_DA_PASTA_NO_DRIVE'  # Substitua pelo ID da pasta onde está o users.db
USERS_DB_FILE_ID = 'SEU_ID_DO_ARQUIVO_USERS_DB'  # Substitua pelo ID atual do users.db no Drive
CREDENTIALS_FILE = 'credentials.json'  # Seu arquivo de credenciais da conta de serviço

def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=['https://www.googleapis.com/auth/drive']
    )
    return build('drive', 'v3', credentials=creds)

def download_users_db_from_drive():
    """Baixa o arquivo users.db do Google Drive"""
    try:
        service = get_drive_service()
        request = service.files().get_media(fileId=USERS_DB_FILE_ID)
        fh = io.FileIO('users.db', 'wb')
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()

        print("✅ users.db baixado com sucesso do Google Drive.")
    except Exception as e:
        print(f"❌ Erro ao baixar users.db: {e}")

def upload_users_db_to_drive():
    """Faz o upload do arquivo users.db para o Google Drive (sobrescrevendo o existente)"""
    try:
        service = get_drive_service()
        media = MediaFileUpload('users.db', mimetype='application/x-sqlite3')

        updated_file = service.files().update(
            fileId=USERS_DB_FILE_ID,
            media_body=media
        ).execute()

        print(f"✅ users.db atualizado no Google Drive. ID do arquivo: {updated_file.get('id')}")
        st.success("✅ Banco de usuários atualizado no Google Drive!")
    except Exception as e:
        print(f"❌ Erro ao fazer upload do users.db: {e}")
        st.error(f"❌ Erro ao fazer upload: {e}")
