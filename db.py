import sqlite3


def conectar():
    return sqlite3.connect("bd.db")

def criar_tabelas():
        tabela = """
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            categoria TEXT NOT NULL,
            descricao TEXT,
            valor REAL NOT NULL
        );
        """

        con = conectar()
        con.execute(tabela)
        con.commit()
        con.close()

if __name__ == '__main__':
      criar_tabelas()
      print("Tabela criada (ou ja existia). Arquivo bd.db pronto")
