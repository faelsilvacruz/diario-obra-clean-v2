import streamlit as st
import sqlite3
import hashlib

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def setup_database():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Criar tabela se não existir
    c.execute('''
    CREATE TABLE IF NOT EXISTS userstable (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        senha_alterada INTEGER DEFAULT 0
    )
    ''')

    # Criar usuário admin inicial, se ainda não existir
    admin_username = 'admin'
    admin_password = make_hashes('1234')  # Senha inicial padrão
    admin_role = 'admin'

    c.execute("SELECT * FROM userstable WHERE username = ?", (admin_username,))
    if not c.fetchone():
        c.execute('INSERT INTO userstable (username, password, role, senha_alterada) VALUES (?,?,?,1)',
                  (admin_username, admin_password, admin_role))
        conn.commit()
        return "Usuário admin criado com sucesso (senha: 1234)."
    else:
        return "Usuário admin já existe. Nenhuma alteração feita."

def main():
    st.title("🛠️ Setup do Banco de Dados - users.db")

    if st.button("Executar Setup"):
        resultado = setup_database()
        st.success(f"✅ Setup concluído: {resultado}")

if __name__ == "__main__":
    main()
