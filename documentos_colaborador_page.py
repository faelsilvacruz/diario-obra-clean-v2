import streamlit as st
from datetime import datetime
import re
from drive_utils import listar_arquivos_por_usuario
from pytz import timezone

def formatar_nome_arquivo(nome_arquivo):
    nome_sem_extensao = nome_arquivo.replace(".pdf", "")
    nome_formatado = nome_sem_extensao.replace("_", " ")
    return nome_formatado

def extrair_mes_ano(nome_arquivo):
    padrao = r'Holerite_([A-Za-zç]+)_(\d{4})\.pdf'
    match = re.search(padrao, nome_arquivo, re.IGNORECASE)
    if match:
        mes = match.group(1).capitalize()
        ano = match.group(2)
        return mes, int(ano)
    return None, None

def mes_para_numero(mes):
    meses = {
        'Janeiro': 1, 'Fevereiro': 2, 'Março': 3, 'Abril': 4,
        'Maio': 5, 'Junho': 6, 'Julho': 7, 'Agosto': 8,
        'Setembro': 9, 'Outubro': 10, 'Novembro': 11, 'Dezembro': 12
    }
    return meses.get(mes, 0)

def ordenar_holerites(arquivos):
    arquivos_com_data = []
    for arquivo in arquivos:
        nome = arquivo['name']
        mes, ano = extrair_mes_ano(nome)
        if mes and ano:
            num_mes = mes_para_numero(mes)
            if num_mes > 0:
                arquivos_com_data.append({
                    'arquivo': arquivo,
                    'ano': ano,
                    'mes_num': num_mes
                })
    arquivos_ordenados = sorted(
        arquivos_com_data,
        key=lambda x: (x['ano'], x['mes_num']),
        reverse=True
    )
    return [item['arquivo'] for item in arquivos_ordenados]

def render_documentos_colaborador_page():
    st.set_page_config(
        page_title="Central de Documentos - RDV Engenharia",
        page_icon="📂",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown("""
    <style>
        :root {
            --primary-color: #0F2A4D;
            --secondary-color: #446084;
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

    if opcao == "Holerite":
        arquivos = ordenar_holerites(arquivos)
    else:
        def parse_created(arquivo):
            try:
                return datetime.strptime(arquivo['createdTime'], '%Y-%m-%dT%H:%M:%S.%fZ')
            except:
                return datetime.min
        arquivos = sorted(arquivos, key=parse_created, reverse=True)

    if not arquivos:
        st.info("Nenhum documento encontrado.")
        return

    for arquivo in arquivos:
        nome_doc = arquivo['name']
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
            <div class="document-name">📄 {formatar_nome_arquivo(nome_doc)}</div>
            <div style='font-size: 0.85rem; color: #555;'>
                📅 {ultima_mod} | 📦 {tamanho_mb} MB
            </div>
            <a href="{link}" target="_blank">
                <button class="download-btn">Abrir Documento</button>
            </a>
        </div>
        """, unsafe_allow_html=True)
