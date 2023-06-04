
from spoomie.src.classes.db import Database
from collections import deque


class Grafo:
    def __init__(self):
        self.usuarios = {}

    def adicionar_usuario(self, email):
        if email not in self.usuarios:
            self.usuarios[email] = set()


    def retornaEmailsDB(self):
        usuariosdb = Database().verificaExistencia()
        for emailDB in usuariosdb:                      # loop que vai puxar todos os usuarios que estao no BD para o programa atual
            if emailDB not in self.usuarios:            # tem que implementar depois uma forma de puxar tambem quem ele segue.
                self.usuarios[emailDB] = set()


    def adicionar_relacao(self, email1, email2):
        if email1 in self.usuarios and email2 in self.usuarios:
            if email1 in self.usuarios[email2]:                             #se a pessoa JA seguir a outra pessoa.
                print(f"Você já segue {Database().retornaNome(email2)}\n")
            else:
                self.usuarios[email2].add(email1)
                print(f"Agora você está seguindo {Database().retornaNome(email2)}\n")

        else:
            print(f"O email {email2} não tem uma conta no Spoomie")


    def verificar_relacao(self, email1, email2):
        if email1 in self.usuarios and email2 in self.usuarios:
            return email2 in self.usuarios[email1]
        return False

    def exibir_usuarios_e_seguidores(self):
        for email in self.usuarios:
            seguidores = self.usuarios[email]
            print(f"Usuário: {email}")

            if seguidores:
                print("Seguidores:")
                for seguidor in seguidores:
                    print(f"  - {seguidor}")

            else:
                print("Não possui seguidores.")

            print()

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