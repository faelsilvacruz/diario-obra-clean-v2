import sqlite3

def get_obras():
    conn = sqlite3.connect('diario_obra.db')
    c = conn.cursor()
    c.execute('SELECT id, nome FROM obras')
    obras = c.fetchall()
    conn.close()
    return obras

def add_obra(nome_obra):
    conn = sqlite3.connect('diario_obra.db')
    c = conn.cursor()
    c.execute('INSERT INTO obras (nome) VALUES (?)', (nome_obra,))
    conn.commit()
    conn.close()

def add_contrato(obra_id, nome_contrato):
    conn = sqlite3.connect('diario_obra.db')
    c = conn.cursor()
    c.execute('INSERT INTO contratos (obra_id, nome) VALUES (?, ?)', (obra_id, nome_contrato))
    conn.commit()
    conn.close()

def add_colaborador(nome_colaborador, funcao):
    conn = sqlite3.connect('diario_obra.db')
    c = conn.cursor()
    c.execute('INSERT INTO colaboradores (nome, funcao) VALUES (?, ?)', (nome_colaborador, funcao))
    conn.commit()
    conn.close()
