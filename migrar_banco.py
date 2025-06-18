import sqlite3
import pandas as pd

def migrar_obras_csv_para_banco():
    try:
        obras_df = pd.read_csv("obras.csv")
    except Exception as e:
        print(f"Erro ao ler o arquivo obras.csv: {e}")
        return

    conn = sqlite3.connect('diario_obra.db')
    c = conn.cursor()

    # Cria a tabela de obras se ainda não existir
    c.execute('''
        CREATE TABLE IF NOT EXISTS obras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    ''')

    # Insere as obras
    for index, row in obras_df.iterrows():
        nome_obra = row["Nome"].strip()
        c.execute('INSERT INTO obras (nome) VALUES (?)', (nome_obra,))

    conn.commit()
    conn.close()
    print("Migração das obras concluída com sucesso!")

if __name__ == "__main__":
    migrar_obras_csv_para_banco()
