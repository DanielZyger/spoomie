
from DataBase import db

class Login:

    def __init__(self):
        self.db = db.Database()

    def Login(self, email, senha):
        try:
            self.db.cursor.execute("SELECT email, senha FROM usuarios WHERE email=? and senha=?", (email, senha,))
            if self.db.cursor.fetchone():
                print("Login realizado !!")
                return True

            else:
                return False

        except Exception as e:
            print("Problema ao realizar login", e)