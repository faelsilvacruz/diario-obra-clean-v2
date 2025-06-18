import sqlite3

def get_obras():
    conn = sqlite3.connect('diario_obra.db')
    c = conn.cursor()
    c.execute('SELECT id, nome FROM obras')
    obras = c.fetchall()
    conn.close()
    return obras
