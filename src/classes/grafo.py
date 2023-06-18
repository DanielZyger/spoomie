import os
import sys
sys.path.append(os.path.join(os.getcwd()))

import json
from db import Database
from collections import deque
from graphviz import Digraph            #pip install graphviz
from PIL import Image                   #pip install Pillow


class Grafo:
    def __init__(self):
        self.usuarios = {}
        self.arquivo_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dados_grafo.json')

    def salvarDadosJson(self):
        with open(self.arquivo_json, "w") as arquivo:
            json.dump({k: list(v) for k, v in self.usuarios.items()}, arquivo, indent=2)

    def puxarDadosJson(self):
        with open(self.arquivo_json, "r") as arquivo:
            data = json.load(arquivo)
            self.usuarios = {emails: set(seguidores) for emails, seguidores in data.items()}

    def adicionarUsuario(self, email):
        if email not in self.usuarios:
            self.usuarios[email] = set()
            self.salvarDadosJson()

    def seguir(self, email1, email2):
        if email1 in self.usuarios and email2 in self.usuarios:
            if email1 in self.usuarios[email2]:
                print(f"Você já segue {Database().retornaNome(email2)}\n")
            else:
                self.usuarios[email2].add(email1)
                self.salvarDadosJson()
                print(f"Agora você está seguindo {Database().retornaNome(email2)}\n")

        else:
            print(f"O email {email2} não tem uma conta no Spoomie")

    def unfollow(self, email1, email2):
        if email1 in self.usuarios and email2 in self.usuarios:

            if email1 in self.usuarios[email2]:
                self.usuarios[email2].remove(email1)
                self.salvarDadosJson()
                print(f"Você deixou de seguir {Database().retornaNome(email2)}\n")
            else:
                print(f"Você não segue {Database().retornaNome(email2)}\n")

        else:
            print(f"O email {email2} não tem uma conta no Spoomie")

    def verificarFollow(self, email1, email2):
        if email1 in self.usuarios and email2 in self.usuarios:
            return email2 in self.usuarios[email1]
        return False

    def countSeguindo(self, userEmail):
        seguindo = 0
        for email in self.usuarios:
            if userEmail in self.usuarios[email]:
                seguindo += 1

        return seguindo

    def listaTodosUsuarios(self):
        for email in self.usuarios:
            seguidores = self.usuarios[email]
            print(f"Usuário: {Database().retornaNome(email)}, email: {email}")

            if seguidores:
                print(f"Total de seguidores: {len(seguidores)}")
                print("Seguidores:")
                for seguidor in seguidores:
                    print(f" -> {seguidor}")
            else:
                print(" Não possui seguidores.")

            print(f"{Database().retornaNome(email)} segue {self.countSeguindo(email)} pessoas\n")

    def consultaDadosUsuario(self, email):
        for data in Database().cursor.execute('''SELECT dataNasc FROM usuarios WHERE email=?''', (email,)).fetchone():
            DataNascimento = data

        for telefone in Database().cursor.execute('''SELECT telefone FROM usuarios WHERE email=?''', (email,)).fetchone():
            NumTelefone = telefone

        for cidade in Database().cursor.execute('''SELECT cidade FROM usuarios WHERE email=?''', (email,)).fetchone():
            Cidade = cidade

        Seguindo = self.countSeguindo(email)
        print(f"Nome: {Database().retornaNome(email)}\nEmail: {email}\nNascimento: {DataNascimento}\nTelefone: {NumTelefone}\nCidade: {Cidade}\nSeguindo: {Seguindo}")

        if Seguindo:
            print(f"Pessoas que {Database().retornaNome(email)} segue:")
            for usuario in self.usuarios:
                if email in self.usuarios[usuario]:
                    print(f" -{usuario}")

    def mostrarGrafo(self, formato):
        dot = Digraph()

        for email in self.usuarios:
            seguidores = self.usuarios[email]
            if seguidores:
                for seguidor in seguidores:
                    dot.edge(email, seguidor)
            else:
                dot.node(email)

        dot.render(filename='grafo', format=formato, directory=os.path.dirname(os.path.abspath(__file__)))
        if formato != "pdf":
            Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f'grafo.{formato}')).show()

    def menorCaminhoEntreUsuarios(self, emailOrigem, emailDestino):
        if emailOrigem not in self.usuarios or emailDestino not in self.usuarios:
            return None

        queue = deque()
        visitados = set()
        antecedentes = {}

        queue.append(emailOrigem)
        visitados.add(emailOrigem)
        antecedentes[emailOrigem] = None

        while queue:
            emailAtual = queue.popleft()

            if emailAtual == emailDest:
                caminho = [emailAtual]
                emailAntec = antecedentes[emailAtual]

                while emailAntec is not None:
                    caminho.insert(0, emailAntec)
                    emailAntec = antecedentes[emailAntec]

                return caminho

            for emailVizinho in self.usuarios[emailAtual]:
                if emailVizinho not in visitados:
                    queue.append(emailVizinho)
                    visitados.add(emailVizinho)
                    antecedentes[emailVizinho] = emailAtual

        return None

    def excluirUsuario(self, email):
        del self.usuarios[email]

        for usuario in self.usuarios.values():
            if email in usuario:
                usuario.remove(email)

        Database().excluirUsuario(email)
        self.salvarDadosJson()

        return

    def grauMedioEntrada(self):
        TotalEntrada = 0

        if not len(self.usuarios):
            return TotalEntrada

        for seguidores in self.usuarios.values():
            TotalEntrada += len(seguidores)                                 #soma com o tamanho da lista de seguidores de cada usuario

        return TotalEntrada / len(self.usuarios)

    def grauMedioSaida(self):
        TotalSaida = 0
        if not len(self.usuarios):
            return TotalSaida

        for usuario in self.usuarios:
            TotalSaida += self.countSeguindo(usuario)

        return TotalSaida / len(self.usuarios)

    def BFS(self, origem):
        visited = set()
        distance = {usuario: float() for usuario in self.usuarios.keys()}
        fila = deque()
        fila.append((origem, 0))
        distance[origem] = 0

        while fila:
            usuario, distancia = fila.popleft()
            if usuario not in visited:
                visited.add(usuario)

                for vizinho in self.usuarios[usuario]:
                    distance[vizinho] = distancia + 1
                    fila.append((vizinho, distancia + 1))

        return distance

    def grafoDiametro(self):
        if not len(self.usuarios):
            return 0

        MaiorDistancia = 0
        for ori in self.usuarios.keys():
            Distancia = self.BFS(ori)
            MaiorDistancia = max( MaiorDistancia, max(Distancia.values()) )

        return MaiorDistancia

    def UserMaisSeguido(self):
        Seguidores = 0
        UsuarioMaisSeguido = None
        for user, followers in self.usuarios.items():
            if len(followers) > Seguidores:
                Seguidores = len(followers)
                UsuarioMaisSeguido = user

        return UsuarioMaisSeguido if Seguidores > 0 else "Nenhum usuário da rede possui seguidores.\n"

    def informacoesRede(self):
        print(f"Usuários cadastrados: {len(self.usuarios)}\nGrau médio de entrada: {self.grauMedioEntrada()}")
        print(f"Grau médio de saída: {self.grauMedioSaida()}\nDiâmetro do grafo: {self.grafoDiametro()}")
        print(f"Usuário com mais seguidores: {self.UserMaisSeguido()}")



if __name__ == '__main__':
    graph = Grafo()
    graph.puxarDadosJson()
    """graph.exibir_usuarios_e_seguidores()
    print()
    graph.adicionar_relacao("rogerio@gmail", "bernardo@gmail")
    graph.adicionar_relacao("isadora@gmail", "pamela@gmail")
    print()
    graph.exibir_usuarios_e_seguidores()
    print(f'Rogerio segue bernardo ? {graph.verificar_relacao("bernardo@gmail", "rogerio@gmail")}')"""
    #graph.excluirUsuario("pamela@gmail")
    #graph.exibir_usuarios_e_seguidores()
    #graph.mostrarGrafo()

    graph.unfollow("pamela@gmail", "bernardo@gmail")
    #graph.mostrarGrafo("pdf")
    #graph.listaTodosUsuarios()

    #graph.consultaDadosUsuario("pamela@gmail")
    #print(graph.UserMaisSeguido())
    #graph.informacoesRede()
