import io
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

# ===== CONFIGURAÇÕES =====
USERS_DB_FILE_ID = '1_VOW-WwwO6UyM9iDvpj5MmCwUgb6wJ8Q'  # ID real do seu arquivo users.db no Google Drive

def get_drive_service():
    try:
        # Lendo as credenciais diretamente dos secrets (seção [google_service_account])
        service_account_info = st.secrets["google_service_account"]
        creds = service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=["https://www.googleapis.com/auth/drive"]
        )
        return build('drive', 'v3', credentials=creds)
    except Exception as e:
        print(f"❌ Erro ao autenticar no Google Drive: {e}")
        st.error(f"Erro ao conectar ao Google Drive: {e}")
        return None

def download_users_db_from_drive():
    """Baixa o arquivo users.db do Google Drive"""
    try:
        service = get_drive_service()
        if service is None:
            return
        request = service.files().get_media(fileId=USERS_DB_FILE_ID)
        fh = io.FileIO('users.db', 'wb')
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()

        print("✅ users.db baixado com sucesso do Google Drive.")
    except Exception as e:
        print(f"❌ Erro ao baixar users.db: {e}")
        st.error(f"Erro ao baixar users.db: {e}")

def upload_users_db_to_drive():
    """Faz o upload do arquivo users.db para o Google Drive (sobrescrevendo o existente)"""
    try:
        service = get_drive_service()
        if service is None:
            return
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
