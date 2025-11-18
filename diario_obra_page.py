# diario_obra_page.py
import os
import unicodedata
from datetime import datetime
import pandas as pd
import streamlit as st
from pdf_drive_utils import gerar_pdf, processar_fotos, enviar_email

# =========================
# Helpers de dados (cache)
# =========================

def _norm(s: str) -> str:
    """minúsculas, sem acentos e sem espaços extras (para cabeçalhos)"""
    s = str(s)
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
    return s.strip().lower()

@st.cache_data(ttl=3600)
def carregar_arquivo_csv(caminho: str) -> pd.DataFrame:
    """
    Lê CSV com autodetecção de separador e normaliza cabeçalhos.
    Se houver apenas 1 coluna, ela vira 'nome'.
    """
    if not os.path.exists(caminho):
        return pd.DataFrame()

    try:
        df = pd.read_csv(caminho, sep=None, engine="python", encoding="utf-8", header=0)
    except Exception:
        # fallback simples
        df = pd.read_csv(caminho, encoding="utf-8", header=0)

    # normaliza nomes de colunas
    df.columns = [_norm(c) for c in df.columns]

    # se só tem 1 coluna, padroniza como 'nome'
    if "nome" not in df.columns and len(df.columns) > 0:
        df = df.rename(columns={df.columns[0]: "nome"})

    # limpa strings
    for c in df.columns:
        if df[c].dtype == object:
            df[c] = df[c].astype(str).str.strip()

    return df

@st.cache_data(ttl=3600)
def load_obras() -> pd.DataFrame:
    df = carregar_arquivo_csv("obras.csv")
    if not df.empty and "nome" in df.columns:
        df = df[df["nome"] != ""].copy()
        df = df.sort_values("nome", key=lambda s: s.str.normalize("NFKD"))
    return df

@st.cache_data(ttl=3600)
def load_contratos() -> pd.DataFrame:
    # tenta raiz e /assets/
    for caminho in ["contratos.csv", os.path.join("assets", "contratos.csv")]:
        df = carregar_arquivo_csv(caminho)
        if not df.empty:
            if "nome" in df.columns:
                df = df[df["nome"] != ""].copy()
                df = df.sort_values("nome", key=lambda s: s.str.normalize("NFKD"))
            return df
    return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_colaboradores() -> pd.DataFrame:
    df = carregar_arquivo_csv("colaboradores.csv")
    if df.empty:
        return df

    # aceita 'funcao'/'função'
    if "funcao" not in df.columns and "funcao" in [ _norm(c) for c in df.columns ]:
        pass  # já normalizado
    elif "funcao" not in df.columns and "funcao" not in df.columns and "funcaO" not in df.columns:
        # tenta mapear possíveis variações
        for c in list(df.columns):
            if _norm(c) == "funcao":
                df = df.rename(columns={c: "funcao"})
                break

    # filtra ativos se houver coluna 'status'
    if "status" in df.columns:
        df["status"] = df["status"].str.lower().str.strip()
        df = df[df["status"] == "ativo"]

    # normalização para busca
    if "nome" in df.columns:
        df["nome_normalizado"] = df["nome"].str.lower().str.strip()

    # ordenação
    if "nome" in df.columns:
        df = df[df["nome"] != ""]
        df = df.sort_values("nome", key=lambda s: s.str.normalize("NFKD"))

    return df

# ================
# Página principal
# ================

def render_diario_obra_page():
    st.warning("VERSÃO DEBUG 18/NOV – GitHub sincronizado")

    st.markdown("## 📓 Diário de Obra")

    # Botão para limpar cache e recarregar dados
    if st.button("🔄 Atualizar dados (limpar cache)"):
        st.cache_data.clear()
        st.success("Cache limpo. Recarregando…")
        st.rerun()

    # ===== Carregamento dos dados =====
    obras_df = load_obras()
    contratos_df = load_contratos()
    colab_df = load_colaboradores()

    if obras_df.empty or "nome" not in obras_df.columns:
        st.error("Arquivo **obras.csv** não encontrado ou sem coluna 'nome'.")
        st.stop()
    if contratos_df.empty or "nome" not in contratos_df.columns:
        st.error("Arquivo **contratos.csv** não encontrado ou sem coluna 'nome'.")
        st.stop()
    if colab_df.empty or "nome" not in colab_df.columns:
        st.warning("Arquivo **colaboradores.csv** vazio/sem coluna 'nome'. Você ainda pode preencher manualmente, mas os selects ficarão limitados.")

    obras_lista = [""] + obras_df["nome"].dropna().tolist()
    contratos_lista = [""] + contratos_df["nome"].dropna().tolist()
    colaboradores_lista = colab_df["nome"].dropna().tolist() if not colab_df.empty else []
    max_colabs = max(1, len(colaboradores_lista)) if colaboradores_lista else 8

    # ===== Dados da Obra =====
    st.markdown("### 📋 Dados da Obra")
    c1, c2, c3 = st.columns([0.45, 0.25, 0.30])
    with c1:
        obra = st.selectbox("Obra", obras_lista, index=0, placeholder="Selecione…")
        local = st.text_input("Local")
    with c2:
        data = st.date_input("Data", datetime.today())
    with c3:
        contrato = st.selectbox("Contrato", contratos_lista, index=0, placeholder="Selecione…")
        clima = st.selectbox("Condições do dia", ["Bom", "Chuva", "Garoa", "Impraticável", "Feriado", "Guarda"])

    # ===== Máquinas e Serviços =====
    st.markdown("### 🛠️ Máquinas e Serviços")
    maquinas = st.text_area("Máquinas e equipamentos utilizados", placeholder="Ex.: betoneira, martelete, caminhão pipa…")
    servicos = st.text_area("Serviços executados no dia", placeholder="Descreva objetivamente o que foi executado.")

    # ===== Efetivo =====
    st.markdown("### 👷‍♂️ Efetivo de Pessoal")
    qtd_colaboradores = st.number_input(
        "Quantos colaboradores hoje?",
        min_value=1, max_value=max_colabs, value=1, step=1
    )
    efetivo_lista = []

    for i in range(int(qtd_colaboradores)):
        with st.expander(f"Colaborador {i+1}", expanded=True):
            if colaboradores_lista:
                nome = st.selectbox("Nome", [""] + colaboradores_lista, key=f"colab_nome_{i}", index=0)
            else:
                nome = st.text_input("Nome", key=f"colab_nome_{i}")

            funcao = ""
            if nome and not colab_df.empty and "nome_normalizado" in colab_df.columns:
                nome_norm = nome.strip().lower()
                match = colab_df[colab_df["nome_normalizado"] == nome_norm]
                if not match.empty:
                    funcao = str(match.iloc[0].get("funcao", "")).strip()

            st.markdown(f"**Função:** {funcao if funcao else 'Selecione o colaborador ou informe manualmente'}")

            col1, col2 = st.columns(2)
            entrada = col1.time_input("Entrada", value=datetime.strptime("08:00", "%H:%M").time(), key=f"entrada_{i}")
            saida   = col2.time_input("Saída",   value=datetime.strptime("17:00", "%H:%M").time(), key=f"saida_{i}")

            efetivo_lista.append([
                nome, funcao,
                entrada.strftime("%H:%M"),
                saida.strftime("%H:%M")
            ])

    # ===== Documentação de Segurança =====
    st.markdown("### 🔐 Controle de Documentação de Segurança")
    d1, d2 = st.columns(2)
    hora_lt  = d1.time_input("Hora de Liberação da LT",  value=datetime.strptime("07:00", "%H:%M").time())
    hora_apr = d2.time_input("Hora de Liberação da APR", value=datetime.strptime("07:00", "%H:%M").time())
    data_apr   = st.date_input("Data da APR", value=datetime.today())
    numero_apr = st.text_input("Número/Código da APR")

    # ===== Informações adicionais =====
    st.markdown("### 📝 Informações Adicionais")
    ocorrencias   = st.text_area("Intercorrências / Ocorrências", placeholder="Registre atrasos, clima que impactou, paralisações, etc.")
    nome_empresa  = st.text_input("Responsável Técnico")
    nome_fiscal   = st.text_input("Fiscalização")

    # ===== Fotos =====
    st.markdown("### 📸 Fotos do Serviço")
    fotos = st.file_uploader(
        "Anexe as fotos (JPG, PNG)",
        accept_multiple_files=True,
        type=["png", "jpg", "jpeg"]
    )

    # ===== Ações finais =====
    st.write("---")
    if st.button("✅ Salvar e Gerar Relatório", type="primary"):
        # validações mínimas
        if not obra:
            st.error("Por favor, selecione a **Obra**.")
            st.stop()
        if not contrato:
            st.error("Por favor, selecione o **Contrato**.")
            st.stop()
        if not nome_empresa:
            st.error("Preencha o campo **Responsável Técnico**.")
            st.stop()

        # monta bloco de controle de documentação
        controle_doc_texto = (
            f"Hora de Liberação da LT: {hora_lt.strftime('%H:%M')}\n"
            f"Hora de Liberação da APR: {hora_apr.strftime('%H:%M')}\n"
            f"Data da APR: {data_apr.strftime('%d/%m/%Y')}\n"
            f"Número/Código da APR: {numero_apr}"
        )

        # processa fotos
        fotos_processed_paths = processar_fotos(fotos, obra, data) if fotos else []

        # dicionário de dados
        registro = {
            "dados_obra": {
                "obra": obra,
                "local": local,
                "data": data.strftime("%d/%m/%Y"),
                "contrato": contrato
            },
            "colaboradores": efetivo_lista,
            "maquinas": maquinas,
            "servicos": servicos,
            "controle_doc": controle_doc_texto,
            "intercorrencias": ocorrencias,
            "responsavel": nome_empresa,
            "fiscal": nome_fiscal,
            "clima": clima
        }

        # gera PDF (buffer)
        pdf_buffer = gerar_pdf(
            registro["dados_obra"],
            registro["colaboradores"],
            registro["maquinas"],
            registro["servicos"],
            registro["controle_doc"],
            registro["intercorrencias"],
            registro["responsavel"],
            registro["fiscal"],
            registro["clima"],
            fotos_processed_paths
        )

        nome_pdf = f"Diario_{obra.replace(' ', '_')}_{data.strftime('%Y-%m-%d')}.pdf"

        st.download_button(
            label="📥 Baixar Relatório PDF",
            data=pdf_buffer,
            file_name=nome_pdf,
            mime="application/pdf",
            type="primary"
        )

        # e-mail (em homologação: somente administrativo@rdvengenharia.com.br)
        assunto = f"Diário de Obra - {obra} ({data.strftime('%d/%m/%Y')})"
        corpo = f"""
        <p>Relatório diário gerado:</p>
        <ul>
            <li><b>Obra:</b> {obra}</li>
            <li><b>Data:</b> {data.strftime('%d/%m/%Y')}</li>
            <li><b>Responsável:</b> {nome_empresa}</li>
        </ul>
        """

        pdf_buffer.seek(0)
        ok = enviar_email(
            ["administrativo@rdvengenharia.com.br"],  # ambiente de homologação
            assunto,
            corpo,
            pdf_buffer,
            nome_pdf
        )
        if ok:
            st.success("E-mail enviado com sucesso!")
        else:
            st.warning("PDF gerado, mas não foi possível enviar o e-mail agora.")
