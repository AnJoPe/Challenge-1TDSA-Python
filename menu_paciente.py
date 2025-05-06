#Método que mostra a lista de opções do menu e retorna um input para escolha
def menu_paciente_escolha():
    print("\n\nMenu do Paciente:"
          "\n1 - Agendamentos;"
          "\n2 - Meus Dados;"
          "\n3 - Exames;"
          "\n4 - Prescrições;"
          "\n5 - Documentos Necessários;"
          "\n6 - Ajuda;"
          "\n7 - Desconectar."
          "\n\n")

    return int(input("Insira o número de sua escolha: "))

#Lista que simula o "banco de dados", guarda todos os agendamentos
'''
    EXEMPLO DE AGENDAMENTO CASO QUERIA DEIXAR ALGUNS DE EXEMPLO
    {
        "dia": 12,
        "mes": 12,
        "ano": 2222,
        "hora": 22,
        "minuto": 22,
        "medico": "Pedro",
        "local": "HC"
    },
'''
lista_agendamentos = [

]

'''
    Essas funções são meio complicadas. Cada agendamento tem salvo separadamente cada item de suas informações
    Poderíamos só ter feito diretamente essa conversão na hora que fossemos usar essas informações, mas ficaria muito
    poluído, então fiz uma função a parte que cuida disso.
'''
def converter_itens_em_data_agendamento(agendamento):
    return f"{agendamento.get("dia")}/{agendamento.get("mes")}/{agendamento.get("ano")}"

def converter_itens_em_horario_agendamento(agendamento):
    return f"{agendamento.get("hora")}:{agendamento.get("minuto")}"
'''Fim das funções complicadas'''

#Função de menu dos agendamentos
def menu_agendamentos():
    opcao_agendamento = 0

    print("===================================")
    #Ficará rodando até ser quebrado manualmente com um break
    while True:
        print("\nMenu de Agendamentos:"
              "\n1 - Listar agendamentos;"
              "\n2 - Agendar;"
              "\n3 - Desmarcar agendamento;"
              "\n4 - Voltar"
              "\n")

        opcao_agendamento = int(input("Insira o número de sua escolha: "))
        match opcao_agendamento:
            case 1:
                print("Lista de Agendamentos: \n")
                for agendamento in lista_agendamentos:
                    print(f"--------------------------"
                          f"\nMédico: {agendamento.get("medico")};"
                          f"\nData: {converter_itens_em_data_agendamento(agendamento)};"
                          f"\nHorário: {converter_itens_em_horario_agendamento(agendamento)};"
                          f"\nLocal: {agendamento.get("local")}")
                print("--------------------------")

            case 2:
                informacoes_corretas = False

                dia = 0
                mes = 0
                ano = 0
                hora = 0
                minuto = 0
                medico = ""
                local = ""

                while not informacoes_corretas:
                    print(f"\nNovo agendamento: \n")
                    dia = int(input("Por favor, insira o dia do agendamento (1 a 31): "))
                    mes = int(input("Agora, insira o mês do agendamento (1 a 12): "))
                    ano = int(input("O ano do agendamento (2025-****): "))
                    hora = int(input("A hora em que o agendamento ocorrerá (0 a 23): "))
                    minuto = int(input("Os minutos dessa hora (0 a 59): "))
                    medico = input("O nome do médico responsável pela consulta: ")
                    local = input("E, por fim, o local onde a consulta ocorrerá: ")

                    if (dia < 1 or dia > 31
                        or mes < 1 or mes > 12
                        or ano < 2025
                        or hora < 0 or hora > 23
                        or minuto < 0 or minuto > 59):
                            print("\n\nA data do agendamento está fora dos limites, tente novamente!")
                            continue

                    informacoes_corretas = True

                novo_agendamento = {
                    "dia": dia,
                    "mes": mes,
                    "ano": ano,
                    "hora": hora,
                    "minuto": minuto,
                    "medico": medico,
                    "local": local
                }

                lista_agendamentos.append(novo_agendamento)

                print("Agendamento salvo com sucesso!")

            case 3:
                print("\nRemover Agendamento: ")

                agendamento_escolhido = False
                while not agendamento_escolhido:
                    if len(lista_agendamentos) == 0:
                        print("Você não possui nenhum agendamento!")
                    else:
                        id_agendamento = 1
                        for agendamento in lista_agendamentos:
                            print(f"--------------------------"
                                  f"\n{id_agendamento} - {converter_itens_em_data_agendamento(agendamento)} — {converter_itens_em_horario_agendamento(agendamento)}"
                                  f"\nMédico: {agendamento.get("medico")}")
                            id_agendamento += 1

                    print("--------------------------\n\n"
                          "0 - Voltar")

                    selecao_deletar_agendamento = int(input("Insira o número identificador do agendamento que deseja remover: "))

                    if selecao_deletar_agendamento == 0:
                        agendamento_escolhido = True
                        continue

                    elif selecao_deletar_agendamento < 0 or selecao_deletar_agendamento > len(lista_agendamentos):
                        print("Identificador inválido, tente novamente.")
                        continue

                    else:
                        lista_agendamentos.pop(selecao_deletar_agendamento - 1)
                        agendamento_escolhido = True

            case 4:
                print("\n Voltando...")
                break

            case _:
                print("\nOpção inválida!")
                continue

meu_dado_rg = 123456789
meu_dado_cpf = 12345678909
meu_dado_email = "email@gmail.com"
meu_dado_senha = "senha123"

def menu_meus_dados():
    global meu_dado_rg, meu_dado_cpf, meu_dado_email, meu_dado_senha
    while True:
        print(f"\n Meus Dados:"
              f"\nRG: {meu_dado_rg};"
              f"\nCPF: {meu_dado_cpf};"
              f"\nEmail: {meu_dado_email};"
              f"\nSenha: {meu_dado_senha};"
              f"\n\n"
              f"1 - Editar RG;"
              f"\n2 - Editar CPF;"
              f"\n3 - Editar email;"
              f"\n4 - Editar senha;"
              f"\n5 - Voltar")

        opcao_meus_dados = int(input("Insira o número de sua escolha: "))
        match opcao_meus_dados:
            case 1:
                novo_rg = int(input("Insira o seu novo RG (min. 9 digitos, máx. 10): "))
                if len(str(novo_rg)) < 9 or len(str(novo_rg)) > 10:
                    print("\nNovo RG é inválido (maior que 10 ou menor que 9 digitos)")
                    continue

                meu_dado_rg = novo_rg
                print("\n Novo RG salvo com sucesso!")

            case 2:
                novo_cpf = int(input("Insira o seu novo CPF (min. 11 digitos): "))
                if len(str(novo_cpf)) < 11:
                    print("\nNovo CPF é inválido (menor que 11 digitos)")
                    continue

                meu_dado_cpf = novo_cpf
                print("\n Novo CPF salvo com sucesso!")

            case 3:
                novo_email = input("Insira o seu novo email: ")
                if not "@" in novo_email:
                    print("\nNovo email é inválido")
                    continue

                meu_dado_email = novo_email
                print("\n Novo email salvo com sucesso!")

            case 4:
                nova_senha = input("Insira a sua nova senha (Sem espaços, minímo 5 digitos): ")
                if " " in nova_senha or len(nova_senha) < 5:
                    print("\nNova senha é inválida, verifique se você utilizou um espaço ou se ela tem no mínimo 5 digitos")
                    continue

                meu_dado_senha = nova_senha
                print("\n Nova senha salva com sucesso!")

            case 5:
                print("\n\nVoltando.")
                break

            case _:
                print("Escolha inválida")
                continue

#Loop será infinito até o usuário voluntariamente sair
while True:
    '''Usa o input retornado do método que demonstra o menu de escolhas do paciente e guarda numa variavel, é relativamente
    grande, logo coloquei num método a parte para não poluir o flow principal'''
    opcao_menu = menu_paciente_escolha()

    match(opcao_menu):
        case 1:
            menu_agendamentos()

        case 2:
            menu_meus_dados()