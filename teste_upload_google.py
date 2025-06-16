import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account
import io

# === CONFIGURAÇÕES ===
DRIVE_FOLDER_ID = "1BUgZRcBrKksC3eUytoJ5mv_nhMRdAv1d"  # ✅ Seu ID da pasta
ARQUIVO_NOME = "teste_streamlit_upload.txt"

# === TENTA CARREGAR AS CREDENCIAIS DO secrets.toml ===
try:
    creds_dict = dict(st.secrets["google_service_account"])
    creds = service_account.Credentials.from_service_account_info(
        creds_dict, scopes=["https://www.googleapis.com/auth/drive"]
    )
except Exception as e:
    st.error(f"Erro ao carregar as credenciais: {e}")
    st.stop()

# === TENTA FAZER O UPLOAD ===
def upload_teste():
    try:
        service = build("drive", "v3", credentials=creds, static_discovery=False, cache_discovery=False)

        conteudo = io.BytesIO(b"Arquivo de teste gerado via Streamlit.")
        media = MediaIoBaseUpload(conteudo, mimetype="text/plain", resumable=True)

        file_metadata = {
            "name": ARQUIVO_NOME,
            "parents": [DRIVE_FOLDER_ID]
        }

        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id",
            supportsAllDrives=True
        ).execute()

        file_id = file.get("id")
        if file_id:
            link = f"https://drive.google.com/file/d/{file_id}/view"
            st.success(f"Upload de teste OK! [Abrir no Drive]({link})")
        else:
            st.error("Upload feito, mas sem retorno de ID.")

    except Exception as e:
        st.error(f"Erro durante o upload de teste: {e}")

st.title("Teste simples de Upload para Google Drive")

if st.button("Fazer Upload de Teste"):
    upload_teste()
