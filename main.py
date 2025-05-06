print("Seja bem-vindo(a) ao painel de pacientes da HC!")
print("Espero que tenha uma ótima experiência.")

print("\n Antes de efetuarmos o seu acesso, responda:")

# Estado inicial o paciente não está logado
esta_logado = False

# Lista que guarda o registro de todos os pacientes
    # Um registro seria da seguinte forma:
        # "email": email_do_paciente,
        # "senha": senha_do_paciente
lista_contas_pacientes = []

meu_dado_email = ""


# Função para checar se um input é sim. É para evitar colocar ifs gigantes por todo o código.
def checarInputSim(inputString):
    if (
        inputString.lower() == "sim"
        or inputString.lower() == "s"
        or inputString.lower() == "si"
        or inputString.lower() == "yes"
        or inputString.lower() == "ye"
        or inputString.lower() == "y"
    ):
        return True
    else:
        return False

# Função para checar se um input é não. É para evitar colocar ifs gigantes por todo o código.
def checarInputNao(inputString):
    if (
        inputString.lower() == "nao"
        or inputString.lower() == "não"
        or inputString.lower() == "na"
        or inputString.lower() == "nã"
        or inputString.lower() == "n"
        or inputString.lower() == "no"
    ):
        return True
    else:
        return False

# Loop de logar/registrar, roda enquanto não estiver logado
while not esta_logado:
    possui_registro = input("Você já possui um cadastro? (Sim/Não): ")
    #Checa as variações mais comuns de "não", só por via das dúvidas
    if checarInputNao(possui_registro):
        print("Certo, prosseguiremos com o processo de registro.\n")

        #Variável de controle do while de registro
        salvo = False

        #WHILE DE REGISTRO - SUPER IMPORTANTE!!!
        while not salvo:
            email_registro = input("Insira o seu email: ")
            senha_registro = input("Insira a sua senha: ")

            # Perfumaria
            confirmar_senha = input(f"Seu email será: {email_registro} \nSua senha será: {senha_registro}\n\n Está "
                                    f"correto? (Sim/Não): ")

            if checarInputSim(confirmar_senha):
                lista_contas_pacientes.append({
                    "email": email_registro,
                    "senha": senha_registro
                })

                print("Registro realizado com sucesso \n\n")
                #Salva o email logado numa variável, caso venha a ser útil depois
                meu_dado_email= email_registro

                salvo = True
                esta_logado = True

                break

            else:
                print("Entendido, tentaremos novamente.")
                continue

    elif checarInputSim(possui_registro):
        print("Certo, efetuaremos a sua autenticação a seguir. \n")

        #Variável de controle do while de login
        conseguiu_logar = False

        #WHILE DE LOGIN - SUPER IMPORTANTE!!!
        while not conseguiu_logar:
            email_login = input("Insira o seu email: ")
            senha_login = input("Insira a sua senha: ")

            #Se o tamanho da lista de contas for 0, a conta não existe (nenhuma existe)
            if len(lista_contas_pacientes) == 0:
                print("Conta inexistente!")

            #Itera sobre cada conta na lista de contas
            for conta in lista_contas_pacientes:
                #Checa se o email e a senha da conta da iteração atual coincidem com as informações informadas pelo usuário
                if conta.get("email") == email_login and conta.get("senha") == senha_login:
                    print("Login realizado com sucesso! \n\n")

                    conseguiu_logar = True
                    esta_logado = True
                    meu_dado_email = email_login
                    break

                #Checa se o email coincide, mas a senha não.
                    #Isso significa que a conta existe, mas a senha está errada. Fala pro usuário e reseta o loop
                elif conta.get("email") == email_login and conta.get("senha") != senha_login:
                    print("Senha incorreta! \n Tente novamente.")
                    break

                #Se o email não coincidiu com alguma conta, ela não existe.
                else:
                    print("Conta inexistente!")


def menuPacienteEscolha():
    print("\n\nMenu do Paciente:"
          "\n1 - Agendamentos;"
          "\n2 - Meus Dados;"
          "\n3 - Exames;"
          "\n4 - Prescrições;"
          "\n5 - Documentos Necessários;"
          "\n6 - Ajuda;"
          "\n7 - Desconectar.")

    return int(input("Insira o número de sua escolha: "))

#Loop será infinito até o usuário voluntariamente sair
while True:
    opcao_menu = menuPacienteEscolha()