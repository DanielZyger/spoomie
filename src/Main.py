from classes import login;
from classes import register;


if __name__ == '__main__':
    login_class = login.Entrar()
    register_class = register.Registro()
    
    while(True):  
        print('Bem-vindo ao Spoomie')
        print('1. Entre')
        print('2. Registre-se')
        num2 = int(input()) 
        if(num2 == 1):
            email = input("E-mail:")
            senha = input("Senha:")
            login_class.login(email, senha)
        else:
            print('Crie sua conta no Spoomie')
            nome = input("Nome:")
            data_nascimento = input("Data de Nascimento:")
            telefone = input("Telefone:")
            cidade = input("Cidade:")
            email = input("E-mail:")
            senha = input("Senha:")
            register_class.criaNewUser(nome, data_nascimento, telefone, cidade, email, senha)
        print('FIM')


        

    


    
    
    