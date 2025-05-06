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

email_atual_logado = ""

# Loop de logar/registrar, roda enquanto não estiver logado
while not esta_logado:
    possui_registro = input("Você já possui um cadastro? (Sim/Não): ")
    #Checa as variações mais comuns de "não", só por via das dúvidas
    if (
            possui_registro.lower() == "nao"
            or possui_registro.lower() == "não"
            or possui_registro.lower() == "na"
            or possui_registro.lower() == "nã"
            or possui_registro.lower() == "n"
            or possui_registro.lower() == "no"
    ):
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

            if (
                    confirmar_senha.lower() == "sim"
                    or confirmar_senha.lower() == "s"
                    or confirmar_senha.lower() == "si"
                    or confirmar_senha.lower() == "yes"
                    or confirmar_senha.lower() == "ye"
                    or confirmar_senha.lower() == "y"
            ):
                lista_contas_pacientes.append({
                    "email": email_registro,
                    "senha": senha_registro
                })

                print("Registro realizado com sucesso \n\n")
                #Salva o email logado numa variável, caso venha a ser útil depois
                email_atual_logado = email_registro

                salvo = True
                esta_logado = True

                break

            else:
                print("Entendido, tentaremos novamente.")
                continue

    elif (
            possui_registro.lower() == "sim"
            or possui_registro.lower() == "s"
            or possui_registro.lower() == "si"
            or possui_registro.lower() == "yes"
            or possui_registro.lower() == "ye"
            or possui_registro.lower() == "y"
    ):
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
                    email_atual_logado = email_login
                    break

                #Checa se o email coincide, mas a senha não.
                    #Isso significa que a conta existe, mas a senha está errada. Fala pro usuário e reseta o loop
                elif conta.get("email") == email_login and conta.get("senha") != senha_login:
                    print("Senha incorreta! \n Tente novamente.")
                    break

                #Se o email não coincidiu com alguma conta, ela não existe.
                else:
                    print("Conta inexistente!")

print("Sai do loop!")