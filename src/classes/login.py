
from spoomie.src.classes.db import Database                         #precisa ter o caminho completo



class Entrar:
    def __init__(self):
        self.database = Database()

    def login(self, email, senha):
        try:
            self.database.cursor.execute("SELECT email, senha FROM usuarios WHERE email=? and senha=?", (email, senha,))
            if self.database.cursor.fetchone():
                return True

            else:
                print("Credenciais incorretas !")
                return False

        except Exception as e:
            print("Problema ao realizar login", e)



"""if __name__ == '__main__':
    teste = Entrar()
    teste.login("teste@gmail.com", "123")"""