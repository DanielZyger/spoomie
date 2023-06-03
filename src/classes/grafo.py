
from spoomie.src.classes.db import Database



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