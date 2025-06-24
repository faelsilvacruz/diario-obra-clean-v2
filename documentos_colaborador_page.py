import streamlit as st
from datetime import datetime
import re
from drive_utils import listar_arquivos_por_usuario
from pytz import timezone
from header_component import render_header  # Chamada do header final aprovado

def formatar_nome_arquivo(nome_arquivo):
    nome_sem_extensao = nome_arquivo.replace(".pdf", "")
    nome_formatado = nome_sem_extensao.replace("_", " ")
    return nome_formatado

def render_documentos_colaborador_page():
    # ===== Render Header RDV =====
    render_header()

    # ===== Conteúdo da página começa aqui =====
    st.markdown("""
    <style>
    :root {
        --primary-color: #0F2A4D;
    }
    .document-card {
        border-left: 5px solid var(--primary-color);
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.08);
    }
    .document-name {
        font-weight: 600;
        color: var(--primary-color);
    }
    .download-btn {
        background-color: var(--primary-color) !important;
        color: white !important;
        border-radius: 6px !important;
        padding: 8px 16px !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

    from pytz import timezone

    with st.sidebar:
        opcao = st.radio(
            "Selecione o tipo de documento:",
            ["Holerite", "Férias", "Informe de Rendimentos", "Documentos Pessoais"]
        )

        st.markdown(f"👤 Usuário: **{st.session_state.get('username', 'não identificado')}**")

        fuso_brasilia = timezone('America/Sao_Paulo')
        hora_local = datetime.now(fuso_brasilia).strftime('%d/%m/%Y %H:%M')
        st.markdown(f"📅 {hora_local}")

    termo_busca = st.text_input("🔎 Buscar por nome do documento:")

    username = st.session_state.get('username', '')
    if not username:
        st.error("Erro: Usuário não identificado na sessão.")
        return

    with st.spinner(f"Carregando {opcao.lower()}..."):
        arquivos = listar_arquivos_por_usuario(opcao, username)

    if termo_busca:
        arquivos = [a for a in arquivos if termo_busca.lower() in a['name'].lower()]

    if not arquivos:
        st.info("Nenhum documento encontrado.")
        return

    for arquivo in arquivos:
        nome_doc = formatar_nome_arquivo(arquivo['name'])
        link = arquivo['webViewLink']
        tamanho_mb = round(int(arquivo.get('size', 0)) / 1024 / 1024, 2) if 'size' in arquivo else "-"
        ultima_mod = ""
        if 'createdTime' in arquivo:
            try:
                ultima_mod = datetime.strptime(arquivo['createdTime'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%d/%m/%Y')
            except:
                pass

        st.markdown(f"""
        <div class="document-card">
            <div class="document-name">📄 {nome_doc}</div>
            <div style='font-size: 0.85rem; color: #555;'>
                📅 {ultima_mod} | 📦 {tamanho_mb} MB
            </div>
            <a href="{link}" target="_blank">
                <button class="download-btn">Abrir Documento</button>
            </a>
        </div>
        """, unsafe_allow_html=True)
