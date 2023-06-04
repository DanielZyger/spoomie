
from spoomie.src.classes.db import Database

class Registro():

    def __init__(self):
        self.db = Database()

    def criaNewUser(self, email, nome, dataNasc, telefone, cidade, senha):

        try:
            self.db.cursor.execute("SELECT * FROM usuarios WHERE email=?", (email,))
            if self.db.cursor.fetchone():
                print("Já existe um usuário com esse e-mail!")
                return

            self.db.cursor.execute("INSERT INTO usuarios(email, nome, dataNasc, telefone, cidade, senha) VALUES (?, ?, ?, ?, ?, ?)",
                                  (email, nome, dataNasc, telefone, cidade, senha))

            self.db.conn.commit()
            print("Usuário criado com sucesso !")
            #self.db.conn.close()

            return

        except Exception as e:
            print("Erro ao criar novo usuário: ", e)



if __name__ == "__main__":

    User = Registro()
    """conn = sqlite3.connect("RedeSocial.db")
    cursor = conn.cursor()
    for linha in cursor.execute("SELECT * FROM usuarios").fetchall():
        print(linha)"""


