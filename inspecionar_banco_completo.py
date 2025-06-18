import sqlite3

def listar_tabelas():
    conn = sqlite3.connect('diario_obra.db')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelas = c.fetchall()
    conn.close()
    return [t[0] for t in tabelas]

def mostrar_conteudo_tabela(tabela):
    conn = sqlite3.connect('diario_obra.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM {tabela}")
    linhas = c.fetchall()
    colunas = [desc[0] for desc in c.description]
    conn.close()
    return colunas, linhas

if __name__ == "__main__":
    tabelas = listar_tabelas()
    print("\n==== Tabelas no Banco ====")
    for tabela in tabelas:
        print(f"- {tabela}")

    print("\n==========================")

    for tabela in tabelas:
        print(f"\n📋 Conteúdo da Tabela: {tabela}")
        colunas, linhas = mostrar_conteudo_tabela(tabela)
        print(" | ".join(colunas))
        for linha in linhas:
            print(linha)
