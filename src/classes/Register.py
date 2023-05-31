
"""
FAZER FUNCAO DE LOGIN
CONECTAR AO DB
VERIFICAR SE A CONTA EXISTE

"""

from DataBase import db

class Registro():

    def __init__(self):
        self.db = db.Database()

    def criaNewUser(self, nome, sobrenome, email):

        try:
            self.db.cursor.execute("SELECT * FROM usuarios WHERE email=?", (email,))
            if self.db.cursor.fetchone():
                print("Usuário ja existe !")
                return

            self.db.cursor.execute("INSERT INTO usuarios(nome, sobrenome, email) VALUES(?, ?, ?)",
                                   (nome, sobrenome, email))

            self.db.conn.commit()
            print("Usuário criado com sucesso !")
            return

        except Exception as e:
            print("Erro ao criar novo usuário: ", e)


