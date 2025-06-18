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
    # Criar diario_obra.db
conn_diario = sqlite3.connect('diario_obra.db')
c_diario = conn_diario.cursor()

# Tabela de Obras
c_diario.execute('''
    CREATE TABLE IF NOT EXISTS obras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
''')

# Tabela de Contratos
c_diario.execute('''
    CREATE TABLE IF NOT EXISTS contratos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        obra_id INTEGER,
        nome TEXT NOT NULL,
        FOREIGN KEY (obra_id) REFERENCES obras(id)
    )
''')

# Tabela de Colaboradores
c_diario.execute('''
    CREATE TABLE IF NOT EXISTS colaboradores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        funcao TEXT
    )
''')

# Tabela de Diário de Obra
c_diario.execute('''
    CREATE TABLE IF NOT EXISTS diario_obra (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL,
        obra_id INTEGER,
        contrato_id INTEGER,
        frente_servico TEXT,
        atividades TEXT,
        observacoes TEXT,
        responsavel_empresa TEXT,
        fiscalizacao TEXT,
        FOREIGN KEY (obra_id) REFERENCES obras(id),
        FOREIGN KEY (contrato_id) REFERENCES contratos(id)
    )
''')

conn_diario.commit()
conn_diario.close()

print("Banco do Diário de Obra criado com sucesso!")
