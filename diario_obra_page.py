import streamlit as st
from header_component import render_header
from datetime import datetime

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def render_diario_obra_page():
    # ===== Header =====
    render_header()

    # ===== Conteúdo da Página: Diário de Obra =====
    st.title("📓 Diário de Obra - RDV Engenharia")

    st.markdown("""
    Nesta página você pode registrar as atividades diárias da obra, anexar fotos e gerar um resumo.

    ---
    """)

    # ===== Seletor de Data =====
    data_diario = st.date_input("Data do Diário:", datetime.today())

    # ===== Campo de Texto: Atividades =====
    atividades = st.text_area("Descreva as atividades realizadas no dia:")

    # ===== Campo de Texto: Observações Extras =====
    observacoes = st.text_area("Observações adicionais (opcional):")

    # ===== Upload de Fotos =====
    fotos = st.file_uploader("📸 Anexe fotos da obra (JPG, PNG):", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

    # ===== Botão de Salvar =====
    if st.button("✅ Salvar Diário de Obra"):
        st.success(f"Diário de Obra de {data_diario.strftime('%d/%m/%Y')} salvo com sucesso!")

        st.markdown("### ✅ Resumo do que foi preenchido:")
        st.write(f"**Data:** {data_diario.strftime('%d/%m/%Y')}")
        st.write(f"**Atividades:** {atividades}")

        if observacoes:
            st.write(f"**Observações:** {observacoes}")

        if fotos:
            st.write(f"**Fotos Anexadas:** {len(fotos)}")
            for i, foto in enumerate(fotos, 1):
                st.image(foto, caption=f"Foto {i}", width=300)

    st.markdown("---")
    st.info("👉 Em breve: Exportação em PDF e envio automático por e-mail.")
