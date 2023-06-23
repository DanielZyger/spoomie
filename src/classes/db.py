import sqlite3
import os
import json

#EXCLUIR A TABELA E CRIAR OUTRA SEM AS COLUNAS SEGUINDO E SEGUIDORES

class Database:

    def __init__(self):
        caminho_banco_dados = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'classes', 'RedeSocial.db')
        self.conn = sqlite3.connect(caminho_banco_dados)
        self.cursor = self.conn.cursor()

    # Criar tabela de registros se ainda não existir
    def criaTabelaUsuarios(self):

        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
                                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                email     TEXT UNIQUE NOT NULL,
                                nome      TEXT NOT NULL,
                                dataNasc  DATE,
                                telefone  TEXT,
                                cidade    TEXT NOT NULL,
                                senha     TEXT NOT NULL,  
                                CONSTRAINT unique_email UNIQUE (email))''')

            self.conn.commit()
            print("Tabela de usuários criada com sucesso!")
            self.conn.close()
        except Exception as e:
            print("Erro ao tentar criar tabela de usuários:", e)


    def retornaNome(self, email):
        try:
            for nome in self.cursor.execute('''SELECT nome FROM usuarios WHERE email=?''', (email,)).fetchone():
                return nome

        except Exception as e:
            print("Erro ao retornar nome do usuario:", e)


    def excluirUsuario(self, email):
        try:
            self.cursor.execute('''DELETE FROM usuarios WHERE email=?''', (email,))
            self.conn.commit()
            print("Usuário excluido")

        except Exception as e:
            print("Problema ao excluir usuário: ", e)


    def verificaExistencia(self):
        try:
            Usuarios = set()

            for user in self.cursor.execute('''SELECT email FROM usuarios''').fetchall():
                Usuarios.add(user[0])

            return Usuarios

        except Exception as e:
            print("Problema ao retornar usuarios que estão no banco de dados: ", e)


if __name__ == "__main__":

    #vamo cria todas as tabelas que precisarem nesse arquivo.

    db = Database()
    #db.criaTabelaUsuarios()
    #print( "zezinho123@gmail" in db.verificaExistencia())
    db.excluirUsuario("Daniel@example.com")


    #db.FollowersAndFollowing()
    """Email = str(input())
    db.criaTabelaUsuarios()
    db.excluirUsuario("teste@gmail")
    teste = db.verificaExistencia()
    for i in teste:
        print(i)"""
