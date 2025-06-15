
import sqlite3

# Criar users.db
conn_users = sqlite3.connect('users.db')
c_users = conn_users.cursor()
c_users.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT, role TEXT)')
c_users.execute('INSERT INTO userstable VALUES ("admin", "e99a18c428cb38d5f260853678922e03", "admin")')  # senha: abc123
conn_users.commit()
conn_users.close()

# Criar holerites.db
conn_holerite = sqlite3.connect('holerites.db')
c_holerite = conn_holerite.cursor()
c_holerite.execute('CREATE TABLE IF NOT EXISTS holerites (id INTEGER PRIMARY KEY AUTOINCREMENT, nome_colaborador TEXT, mes TEXT, ano TEXT, link_google_drive TEXT)')
c_holerite.execute('INSERT INTO holerites (nome_colaborador, mes, ano, link_google_drive) VALUES ("admin", "Maio", "2025", "https://google.com")')
conn_holerite.commit()
conn_holerite.close()

print("Bancos criados com sucesso!")
