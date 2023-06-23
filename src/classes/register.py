import os
import sys

diretorio_pai = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
diretorio_classes = os.path.join(diretorio_pai, "classes")
sys.path.append(diretorio_pai)
import json
from classes.db import Database
from classes.grafo import Grafo


class Registro():

    def __init__(self):
        self.db = Database()
        self.usuarios = {}
        self.arquivo_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dados_grafo.json')

    def salvarDadosJson(self):
        with open(self.arquivo_json, "w") as arquivo:
            json.dump({k: list(v) for k, v in self.usuarios.items()}, arquivo)

    def criaNewUser(self, email, nome, dataNasc, telefone, cidade, senha):
        try:
            self.db.cursor.execute("SELECT * FROM usuarios WHERE email=?", (email,))
            if self.db.cursor.fetchone():
                print("Já existe um usuário com esse e-mail!\n")
                return

            self.db.cursor.execute("INSERT INTO usuarios(email, nome, dataNasc, telefone, cidade, senha) VALUES (?, ?, ?, ?, ?, ?)",
                                  (email, nome, dataNasc, telefone, cidade, senha))

            self.usuarios[email] = set()
            Grafo.adicionarUsuario(self, email)
            self.db.conn.commit()
            print("Usuário criado com sucesso !\n")

            return

        except Exception as e:
            print("Erro ao criar novo usuário: ", e)



if __name__ == "__main__":

    User = Registro()
    """conn = sqlite3.connect("RedeSocial.db")
    cursor = conn.cursor()
    for linha in cursor.execute("SELECT * FROM usuarios").fetchall():
        print(linha)"""

    #User.criaNewUser("Lucas@gmail.com", "Lucas", "1990-01-01", "1765766343", "Tapera", "111")
    #User.criaNewUser("Nicolas@gmail", "Nicolas", "2002-04-09", "4323254311", "Passo-Fundo", "222")
    """User.criaNewUser("JaneSmith@gmail.com", "Jane Smith", "1990-02-02", "987654321", "Cidade2", "senha2")
    User.criaNewUser("MichaelJohnson@gmail.com", "Michael Johnson", "1990-03-03", "111222333", "Cidade3", "senha3")
    User.criaNewUser("EmilyDavis@gmail.com", "Emily Davis", "1990-04-04", "444555666", "Cidade4", "senha4")
    User.criaNewUser("DavidWilson@gmail.com", "David Wilson", "1990-05-05", "777888999", "Cidade5", "senha5")"""



