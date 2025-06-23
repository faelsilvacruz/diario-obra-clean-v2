import os
import streamlit as st
from googleapiclient.discovery import build
from google.oauth2 import service_account

# ======= Configuração Google Drive API =======
SCOPES = ['https://www.googleapis.com/auth/drive']

def listar_arquivos_por_usuario(tipo_documento, username):
    pasta_principal_id = '1gpKHXPdGeSqUbVze5jy40SLGPOXz583Q'  # ID da pasta 'documentos' no Google Drive
    tipo_para_subpasta = {
        'Holerite': 'holerite',
        'Férias': 'ferias',
        'Informe de Rendimentos': 'informe_rendimentos',
        'Documentos Pessoais': 'documentos_pessoais'
    }

    if tipo_documento not in tipo_para_subpasta:
        return []

    subpasta = tipo_para_subpasta[tipo_documento]

    # ======= Ler as credenciais diretamente do Streamlit Secrets =======
    creds = service_account.Credentials.from_service_account_info(
        st.secrets["google_service_account"],
        scopes=SCOPES
    )
    service = build('drive', 'v3', credentials=creds)

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

    # Listar os arquivos dentro da subpasta
    query_arquivos = f"'{subpasta_id}' in parents and trashed = false"
    resultado_arquivos = service.files().list(
        q=query_arquivos,
        fields="files(id, name, webViewLink)"
    ).execute()
    return resultado_arquivos.get('files', [])

def render_documentos_colaborador_page():
    st.title("📄 Central de Documentos - RDV Engenharia")

    username = st.session_state.get('username', '')
    if not username:
        st.error("Erro: Usuário não identificado na sessão.")
        return

    opcao = st.radio(
        "Selecione o tipo de documento:",
        ["Holerite", "Férias", "Informe de Rendimentos", "Documentos Pessoais"]
    )

    st.write(f"📂 Listando documentos tipo **{opcao}** para usuário: `{username}`")

    arquivos = listar_arquivos_por_usuario(opcao, username)

    if not arquivos:
        st.warning("Nenhum documento encontrado.")
    else:
        for arquivo in arquivos:
            st.markdown(f"📥 [{arquivo['name']}]({arquivo['webViewLink']})")
