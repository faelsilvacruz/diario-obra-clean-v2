import sqlite3
from login_page import make_hashes

def init_db():
    # Criar users.db
    conn_users = sqlite3.connect('users.db')
    c_users = conn_users.cursor()
    c_users.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT, role TEXT)')

    # Inserir usuário admin com senha hash de 'abc123'
    hashed_password = make_hashes("abc123")
    c_users.execute('INSERT INTO userstable VALUES (?, ?, ?)', ("admin", hashed_password, "admin"))

    conn_users.commit()
    conn_users.close()

    # Criar holerites.db
    conn_holerite = sqlite3.connect('holerites.db')
    c_holerite = conn_holerite.cursor()
    c_holerite.execute('''
        CREATE TABLE IF NOT EXISTS holerites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_colaborador TEXT,
            mes TEXT,
            ano TEXT,
            link_google_drive TEXT
        )
    ''')
    conn_holerite.commit()
    conn_holerite.close()

    print("Bancos criados com sucesso!")
