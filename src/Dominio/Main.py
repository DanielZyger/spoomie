import sys
import os

diretorio_pai = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
diretorio_classes = os.path.join(diretorio_pai, "classes")
sys.path.append(diretorio_pai)

from classes.db import Database
from classes import login
from classes import register
from classes import grafo
from datetime import datetime
from art import *                           #pip install art


if __name__ == '__main__':

    tprint("Spoomie")

    database = Database()
    login_class = login.Entrar()
    register_class = register.Registro()
    Grafo = grafo.Grafo()
    Grafo.puxarDadosJson()

    Logado = False
    OptionLogado = None


    while(True):
        print('Bem-vindo ao Spoomie')
        print('1. Entre\n2. Registre-se\n3. Excluir Conta\n0. Fechar programa')
        option = int(input())

        if (option == 1):

            Email = str(input("E-mail: "))
            senha = input("Senha: ")
            if login_class.login(Email, senha):
                print('--------------------------------------------')
                print(f"Bem vindo de volta { Database().retornaNome(Email) }                   Horario atual - {datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}\n")
                Logado = True

                while Logado:
                    Grafo.puxarDadosJson()
                    print("O que deseja fazer ?\n1. Seguir usuário   2. Deixar de seguir um usuário   3. Listar usuários")
                    print("4. Consultar dados de usuário   5. Ver menor caminho entre dois usuarios   6. Mostrar grafo atual na tela ")
                    print("7. Exibir informações da rede   0. Sair da conta\n")

                    try:                                #caso o usuario digite uma opçao que nao exista, ele vai voltar pro inicio do while e pedir uma opçao valida
                        OptionLogado = int(input())
                    except Exception as e:
                        print("Digite uma opção válida !\n")
                        continue

                    if OptionLogado == 1:
                        UsuarioSeguir = str(input("Digite o email do usuário que você deseja seguir: "))
                        Grafo.seguir(Email, UsuarioSeguir)
                        print()

                    if OptionLogado == 2:
                        Unfollow = str(input("Digite o email do usuário que você deseja deixar de seguir: "))
                        Grafo.unfollow(Email, Unfollow)
                        print()

                    if OptionLogado == 3:
                        Grafo.listaTodosUsuarios()
                        print()

                    if OptionLogado == 4:
                        EmailConsultar = str(input("Digite o email do usuário que você deseja consultar os dados: "))
                        Grafo.consultaDadosUsuario(EmailConsultar)
                        print()

                    if OptionLogado == 5:
                        user1 = str(input("Digite o primeiro email: "))
                        user2 = str(input("Digite o segundo email: "))
                        caminho = Grafo.menorCaminhoEntreUsuarios(user1, user2)
                        if caminho != None:
                            print(f'{caminho}\n')
                        else:
                            print("Não existe nenhum caminho para os dois usuarios informados\n")

                    if OptionLogado == 6:
                        Formato = ["png", "jpeg", "pdf"]
                        escolha = int(input("Escola em qual formato deseja mostrar o grafo\n 1. PNG\n 2. JPEG\n 3. PDF\n"))
                        Grafo.mostrarGrafo(Formato[escolha])
                        print()

                    if OptionLogado == 7:
                        Grafo.informacoesRede()
                        print()

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
            print('--------------------------------------------')

        if (option == 3):
            print("Digite o email da conta que deseja excluir do Spoomie: ")
            emailExcluir = str(input())

            if (emailExcluir in database.verificaExistencia()):
                print("Para excluir esse usuario por favor, digite a senha: ")
                senhaEmail = str(input())

                if login_class.login(emailExcluir, senhaEmail):
                    Grafo.excluirUsuario(emailExcluir)
                    print("Sentiremos sua falta no Spoomie...\n")
            else:
                print("Não existe nenhuma conta com esse email !\n")

        if (option == 0):
            tprint("Ate     mais.")
            break

