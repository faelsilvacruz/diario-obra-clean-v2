import streamlit as st
from header_component import render_header
from datetime import datetime

def render_diario_obra_page():
    # ===== Header =====
    render_header()

    # ===== Estilo Local da Página =====
    st.markdown("""
        <style>
        .diario-card {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }

        .diario-title {
            font-size: 1.6rem;
            color: #0F2A4D;
            font-weight: bold;
            margin-bottom: 10px;
        }

        .stTextArea, .stDateInput, .stFileUploader {
            margin-bottom: 20px;
        }

        .stButton>button {
            background-color: #0F2A4D;
            color: white;
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: 600;
            border: none;
        }

        .stButton>button:hover {
            background-color: #14406d;
        }
        </style>
    """, unsafe_allow_html=True)

    # ===== Conteúdo =====
    st.markdown("<div class='diario-card'>", unsafe_allow_html=True)
    st.markdown("<div class='diario-title'>📓 Diário de Obra - Registro do Dia</div>", unsafe_allow_html=True)

    # Seletor de Data
    data_diario = st.date_input("Data do Diário:", datetime.today())

    # Campo de Texto: Atividades
    atividades = st.text_area("Atividades Realizadas:")

    # Campo de Texto: Observações
    observacoes = st.text_area("Observações Adicionais (opcional):")

    # Upload de Fotos
    fotos = st.file_uploader("📸 Anexar Fotos da Obra (JPG, PNG):", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    # Botão Salvar
    if st.button("✅ Salvar Diário de Obra"):
        st.success(f"Diário de Obra de {data_diario.strftime('%d/%m/%Y')} salvo com sucesso!")

        # Resumo
        st.markdown("---")
        st.markdown("### ✅ Resumo do Registro:")
        st.write(f"**Data:** {data_diario.strftime('%d/%m/%Y')}")
        st.write(f"**Atividades:** {atividades}")

        if observacoes:
            st.write(f"**Observações:** {observacoes}")

        if fotos:
            st.write(f"**Total de fotos anexadas:** {len(fotos)}")
            for i, foto in enumerate(fotos, 1):
                st.image(foto, caption=f"Foto {i}", width=300)

    st.markdown("</div>", unsafe_allow_html=True)
