import sqlite3

def get_obras():
    conn = sqlite3.connect('diario_obra.db')
    c = conn.cursor()
    c.execute('SELECT id, nome FROM obras')
    obras = c.fetchall()
    conn.close()
    return obras

def get_contratos():
    conn = sqlite3.connect('diario_obra.db')
    c = conn.cursor()
    c.execute('SELECT id, nome FROM contratos')
    contratos = c.fetchall()
    conn.close()
    return contratos

def get_colaboradores():
    conn = sqlite3.connect('diario_obra.db')
    c = conn.cursor()
    c.execute('SELECT id, nome FROM colaboradores')
    colaboradores = c.fetchall()
    conn.close()
    return colaboradores

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

def excluir_obra_por_id(obra_id):
    conn = sqlite3.connect('diario_obra.db')
    c = conn.cursor()
    c.execute('DELETE FROM obras WHERE id = ?', (obra_id,))
    conn.commit()
    conn.close()

def excluir_contrato_por_id(contrato_id):
    conn = sqlite3.connect('diario_obra.db')
    c = conn.cursor()
    c.execute('DELETE FROM contratos WHERE id = ?', (contrato_id,))
    conn.commit()
    conn.close()

def excluir_colaborador_por_id(colaborador_id):
    conn = sqlite3.connect('diario_obra.db')
    c = conn.cursor()
    c.execute('DELETE FROM colaboradores WHERE id = ?', (colaborador_id,))
    conn.commit()
    conn.close()
