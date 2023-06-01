
"""
FAZER FUNCAO DE LOGIN
CONECTAR AO DB
VERIFICAR SE A CONTA EXISTE

"""

from database import db

class Registro():

    def __init__(self):
        self.db = db.Database()

    def criaNewUser(self, nome, data_nascimento, telefone, cidade, email, senha):

        try:
            self.db.cursor.execute("SELECT * FROM usuarios WHERE email=?", (email,))
            if self.db.cursor.fetchone():
                print("Já existe um usuário com esse e-mail!")
                return

            self.db.cursor.execute("INSERT INTO usuarios(nome, data_nascimento, telefone, cidade, email, senha) VALUES(?, ?, ?, ?, ?, ?)",
                                   (nome, data_nascimento, telefone, cidade, email, senha))

            self.db.conn.commit()
            print("Usuário criado com sucesso !")
            return

        except Exception as e:
            print("Erro ao criar novo usuário: ", e)


