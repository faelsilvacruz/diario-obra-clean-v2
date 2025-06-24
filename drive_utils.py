import streamlit as st
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/drive']

def get_drive_service():
    try:
        service_account_info = st.secrets["google_service_account"]
        creds = service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=SCOPES
        )
        return build('drive', 'v3', credentials=creds)
    except Exception as e:
        print(f"Erro ao autenticar no Google Drive: {e}")
        st.error(f"Erro ao conectar ao Google Drive: {e}")
        return None

def listar_arquivos_por_usuario(tipo_documento, username):
    pasta_principal_id = '1gpKHXPdGeSqUbVze5jy40SLGPOXz583Q'  # ID da pasta 'documentos'
    tipo_para_subpasta = {
        'Holerite': 'holerite',
        'Férias': 'ferias',
        'Informe de Rendimentos': 'informe_rendimentos',
        'Documentos Pessoais': 'documentos_pessoais'
    }

    if tipo_documento not in tipo_para_subpasta:
        return []

    subpasta = tipo_para_subpasta[tipo_documento]
    service = get_drive_service()
    if service is None:
        return []

    # Buscar a pasta do usuário
    query_pasta_usuario = (
        f"'{pasta_principal_id}' in parents and name = '{username}' "
        f"and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    )
    resultado_pasta = service.files().list(q=query_pasta_usuario, fields="files(id, name)").execute()
    pastas_usuario = resultado_pasta.get('files', [])

    if not pastas_usuario:
        return []

    pasta_usuario_id = pastas_usuario[0]['id']

    # Buscar a subpasta (tipo de documento)
    query_subpasta = (
        f"'{pasta_usuario_id}' in parents and name = '{subpasta}' "
        f"and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    )
    resultado_subpasta = service.files().list(q=query_subpasta, fields="files(id, name)").execute()
    subpastas = resultado_subpasta.get('files', [])

    if not subpastas:
        return []

    subpasta_id = subpastas[0]['id']

    # Listar os arquivos dentro da subpasta com os campos completos
    query_arquivos = f"'{subpasta_id}' in parents and trashed = false"
    resultado_arquivos = service.files().list(
        q=query_arquivos,
        fields="files(id, name, webViewLink, createdTime, size)"
    ).execute()

    return resultado_arquivos.get('files', [])
