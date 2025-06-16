import streamlit as st
import sqlite3

def run_migration():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    try:
        c.execute('ALTER TABLE userstable ADD COLUMN senha_alterada INTEGER DEFAULT 0;')
        conn.commit()
        st.success("✅ Campo 'senha_alterada' adicionado com sucesso ao banco de dados!")
    except Exception as e:
        if "duplicate column name" in str(e).lower():
            st.info("⚠️ O campo 'senha_alterada' já existe no banco.")
        else:
            st.error(f"❌ Erro ao alterar a tabela: {e}")
    finally:
        conn.close()

def main():
    st.title("🛠️ Migração do Banco de Dados - users.db")
    if st.button("Executar Migração"):
        run_migration()

if __name__ == "__main__":
    main()
