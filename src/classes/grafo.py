import json
import os
from spoomie.src.classes.db import Database
from collections import deque
from graphviz import Digraph            #pip install graphviz
from PIL import Image                   #pip install Pillow

class Grafo:
    def __init__(self):
        self.usuarios = {}
        self.arquivo_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dados_grafo.json')

    def salvarDadosJson(self):
        with open(self.arquivo_json, "w") as arquivo:
            json.dump({k: set(v) for k, v in self.usuarios.items()}, arquivo)


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

    def verificar_relacao(self, email1, email2):
        if email1 in self.usuarios and email2 in self.usuarios:
            return email2 in self.usuarios[email1]
        return False

    def mostrarRelacaoUsuarios(self):
        for email in self.usuarios:
            seguidores = self.usuarios[email]
            print(f"Usuário: {email}")

            if seguidores:
                print("Seguidores:")
                for seguidor in seguidores:
                    print(f" -> {seguidor}")

            else:
                print(" Não possui seguidores.")

            print()


    #def consulta_dados(self):

    def mostrarGrafo(self):
        dot = Digraph()

        for email in self.usuarios:
            seguidores = self.usuarios[email]
            if seguidores:
                for seguidor in seguidores:
                    dot.edge(email, seguidor)
            else:
                dot.node(email)

        dot.render(filename='grafo', format='jpeg', directory=os.path.dirname(os.path.abspath(__file__)))
        Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'grafo.jpeg')).show()


    def menor_caminho(self, emailOri, emailDest):
        if emailOri not in self.usuarios or emailDest not in self.usuarios:
            return None

        queue = deque()
        visitados = set()
        predecessores = {}

        queue.append(emailOri)
        visitados.add(emailOri)
        predecessores[emailOri] = None

        while queue:
            emailAtual = queue.popleft()

            if emailAtual == emailDest:
                caminho = [emailAtual]
                emailAntec = predecessores[emailAtual]

                while emailAntec is not None:
                    caminho.insert(0, emailAntec)
                    emailAntec = predecessores[emailAntec]

                return caminho

            for emailVizinho in self.usuarios[emailAtual]:
                if emailVizinho not in visitados:
                    queue.append(emailVizinho)
                    visitados.add(emailVizinho)
                    predecessores[emailVizinho] = emailAtual

        return None


    def excluirUsuario(self, email):
        del self.usuarios[email]

        for usuario in self.usuarios.values():
            if email in usuario:
                usuario.remove(email)

        Database().excluirUsuario(email)
        self.salvarDadosJson()

        return


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

    graph.mostrarGrafo()

    #print('--------------------------------------')

