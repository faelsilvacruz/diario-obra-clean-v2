def render_holerite_page():
    st.title("📄 Holerites")

    if "username" not in st.session_state or not st.session_state["username"]:
        st.warning("Por favor, faça login para visualizar seus holerites.")
        return

    nome_colaborador = st.session_state["username"]

    conn = sqlite3.connect("holerites.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT mes, ano, link_google_drive
        FROM holerites
        WHERE nome_colaborador LIKE ?
        ORDER BY ano DESC, mes DESC
    """, (f"%{nome_colaborador}%",))

    resultados = cursor.fetchall()
    conn.close()

    if resultados:
        st.success(f"Holorites disponíveis para: **{nome_colaborador}**")
        for mes, ano, link in resultados:
            st.markdown(f"📅 **{mes}/{ano}** – [🔗 Abrir Holerite]({link})")
    else:
        st.info("Nenhum holerite disponível para você no momento.")
