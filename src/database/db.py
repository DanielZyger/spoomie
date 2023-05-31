import sqlite3


class Database:

    def __init__(self):
        self.conn = sqlite3.connect("BancoDados")
        self.cursor = self.conn.cursor()

    # Criar tabela de registros se ainda não existir
    def criaTabelaUsuarios(self):

        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome TEXT NOT NULL,
                            sobrenome TEXT NOT NULL,
                            email TEXT UNIQUE NOT NULL)''')

            self.conn.commit()
            print("Tabela de usuários criada com sucesso!")

        except Exception as e:
            print("Erro ao tentar criar tabela de usuários:", e)

    def fecharConexao(self):
        self.conn.close()