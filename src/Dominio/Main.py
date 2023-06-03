from spoomie.src.classes import login
from spoomie.src.classes import register
from spoomie.src.classes import grafo
from spoomie.src.classes.db import Database
from datetime import datetime
from art import *   #colocar no readme que precisa usar o pip install art


if __name__ == '__main__':

    tprint("Spoomie")

    login_class = login.Entrar()
    register_class = register.Registro()
    Grafo = grafo.Grafo()
    Logado = False

    Grafo.retornaEmailsDB()

    while(True):
        print('Bem-vindo ao Spoomie')
        print('1. Entre\n2. Registre-se\n0. Fechar programa')
        option = int(input())

        if (option == 1):

            Email = str(input("E-mail: "))
            senha = input("Senha: ")
            login_class.login(Email, senha)
            print('--------------------------------------------')
            print(f"Bem vindo de volta { Database().retornaNome(Email) }                   Horario atual - {datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}\n")
            Logado = True

            while Logado:
                print("O que deseja fazer ?\n1. Seguir usuário\n2. Deixar de seguir um usuário\n3. Listar usuários\n4. Consultar dados de usuário\n0. Sair da conta")
                OptionLogado = int(input())

                if OptionLogado == 1:
                    print("Digite o email do usuário que você deseja seguir: ")
                    UsuarioSeguir = str(input())
                    Grafo.adicionar_relacao(Email, UsuarioSeguir)
                    print()
                    Grafo.exibir_usuarios_e_seguidores()            #coloquei aqui so pra testar

                if OptionLogado == 0:
                    break

        if (option == 2):

            print('Crie sua conta no Spoomie')

            email = input("E-mail: ")
            nome = input("Nome: ")
            data_nascimento = input("Data de Nascimento: ")
            telefone = input("Telefone: ")
            cidade = input("Cidade: ")
            senha = input("Senha: ")

            register_class.criaNewUser(email, nome, data_nascimento, telefone, cidade, senha)
            Grafo.adicionar_usuario(email)
            print('--------------------------------------------')

        if (option == 0):
            tprint("Ate     mais.")
            break

