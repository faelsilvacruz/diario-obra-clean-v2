import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()

# Criar a tabela se ela ainda não existir
c.execute('''
CREATE TABLE IF NOT EXISTS userstable(
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    senha_alterada INTEGER DEFAULT 0
)
''')

conn.commit()
conn.close()

print("Tabela 'userstable' criada com sucesso ou já existente.")
