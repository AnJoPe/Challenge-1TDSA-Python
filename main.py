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

'''
    Informações do paciente, estariam num banco de dados num sistema real
'''
meu_dado_rg = 123456789
meu_dado_cpf = 12345678909
meu_dado_email = ""
meu_dado_senha = ""


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
                #Salva o email e a senha em variáveis, caso venham a ser úteis depois
                meu_dado_email = email_registro
                meu_dado_senha = senha_registro

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
                    meu_dado_senha = senha_login
                    break

                #Checa se o email coincide, mas a senha não.
                    #Isso significa que a conta existe, mas a senha está errada. Fala pro usuário e reseta o loop
                elif conta.get("email") == email_login and conta.get("senha") != senha_login:
                    print("Senha incorreta! \n Tente novamente.")
                    break

                #Se o email não coincidiu com alguma conta, ela não existe.
                else:
                    print("Conta inexistente!")


#Lista que simula o "banco de dados", guarda todos os agendamentos
'''
    EXEMPLO DE AGENDAMENTO CASO QUEIRA DEIXAR ALGUNS DE EXEMPLO
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

#Método que mostra a lista de opções do menu de agendamentos
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
                #Itera sobre cada agendamento na lista de agendamentos e os mostra de forma organizada utilizando o get()
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

                #Looping que ocorrerá até todas as informações serem válidas
                while not informacoes_corretas:
                    print(f"\nNovo agendamento: \n")
                    dia = int(input("Por favor, insira o dia do agendamento (1 a 31): "))
                    mes = int(input("Agora, insira o mês do agendamento (1 a 12): "))
                    ano = int(input("O ano do agendamento (2025-****): "))
                    hora = int(input("A hora em que o agendamento ocorrerá (0 a 23): "))
                    minuto = int(input("Os minutos dessa hora (0 a 59): "))
                    medico = input("O nome do médico responsável pela consulta: ")
                    local = input("E, por fim, o local onde a consulta ocorrerá: ")

                    '''
                        - Não tem como o dia nem o mês serem negativos ou maiores do que o possível
                        - Não tem como agendar num ano que já passou
                        - A hora não pode ser negativa e nem passar de um dia
                        - Os minutos não podem ser negativos e nem passarem de uma hora
                    '''
                    if (dia < 1 or dia > 31
                        or mes < 1 or mes > 12
                        or ano < 2025
                        or hora < 0 or hora > 23
                        or minuto < 0 or minuto > 59):
                            print("\n\nA data do agendamento está fora dos limites, tente novamente!")
                            continue

                    informacoes_corretas = True

                # Dictionary do novo agendamento
                novo_agendamento = {
                    "dia": dia,
                    "mes": mes,
                    "ano": ano,
                    "hora": hora,
                    "minuto": minuto,
                    "medico": medico,
                    "local": local
                }

                # Adicionando o novo agendamento na lista de agendamentos
                lista_agendamentos.append(novo_agendamento)

                print("Agendamento salvo com sucesso!")

            case 3:
                print("\nRemover Agendamento: ")

                #Até um agendamento ser escolhido para ser deletado, o looping se manterá
                agendamento_escolhido = False
                while not agendamento_escolhido:
                    #Se a lista de agendamentos tiver tamanho 0, não dá pra deletar nenhum agendamento
                    if len(lista_agendamentos) == 0:
                        print("Você não possui nenhum agendamento!")
                    else:
                        #O id serve para o usuário escolher o agendamento a ser deletado, começa do 1 apesar das listas
                            #começarem do 0, porque faz mais sentido aos pacientes
                        id_agendamento = 1
                        #Itera sobre cada agendamento na lista de agendamentos, e mostra cada um com um id e suas datas e o médico
                        for agendamento in lista_agendamentos:
                            print(f"--------------------------"
                                  f"\n{id_agendamento} - {converter_itens_em_data_agendamento(agendamento)} — {converter_itens_em_horario_agendamento(agendamento)}"
                                  f"\nMédico: {agendamento.get("medico")}")
                            #Próximo agendamento terá um id diferente, nesse caso, superior
                            id_agendamento += 1

                    print("--------------------------\n\n"
                          "0 - Voltar")

                    selecao_deletar_agendamento = int(input("Insira o número identificador do agendamento que deseja remover: "))

                    #Se for 0, o paciente não quer deletar nenhum, então voltar e quebrar o looping.
                    if selecao_deletar_agendamento == 0:
                        agendamento_escolhido = True
                        continue

                    #Se o seletor for menor que 0, ou maior que o tamanho da lista de agendamentos, ele é inválido
                    elif selecao_deletar_agendamento < 0 or selecao_deletar_agendamento > len(lista_agendamentos):
                        print("Identificador inválido, tente novamente.")
                        continue

                    #Se tudo estiver correto, dar pop no indíce selecionado (subtraindo 1, porque a lista começa do 0)
                    else:
                        lista_agendamentos.pop(selecao_deletar_agendamento - 1)
                        #Quebrar o looping após o apagamento
                        agendamento_escolhido = True

            case 4:
                print("\n Voltando...")
                break

            case _:
                print("\nOpção inválida!")
                continue

#Método que mostra a lista de opções do menu de meus dados
def menu_meus_dados():
    #Essas variáveis são declaradas fora da função, mas são alteradas dentro dela, essa linha é necessária
    global meu_dado_rg, meu_dado_cpf, meu_dado_email, meu_dado_senha

    #O looping ocorrerá até ser manualmente interrompido
    while True:
        print(f"\nMeus Dados:"
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

                #Mínimo de 9 digitos e máximo de 10
                if len(str(novo_rg)) < 9 or len(str(novo_rg)) > 10:
                    print("\nNovo RG é inválido (maior que 10 ou menor que 9 digitos)")
                    continue

                meu_dado_rg = novo_rg
                print("\n Novo RG salvo com sucesso!")

            case 2:
                novo_cpf = int(input("Insira o seu novo CPF (min. 11 digitos): "))

                # Mínimo de 11 digitos
                if len(str(novo_cpf)) < 11:
                    print("\nNovo CPF é inválido (menor que 11 digitos)")
                    continue

                meu_dado_cpf = novo_cpf
                print("\n Novo CPF salvo com sucesso!")

            case 3:
                novo_email = input("Insira o seu novo email: ")

                # É necessário ter um @ no email, para ser considerado um
                if not "@" in novo_email:
                    print("\nNovo email é inválido")
                    continue

                meu_dado_email = novo_email
                print("\n Novo email salvo com sucesso!")

            case 4:
                nova_senha = input("Insira a sua nova senha (Sem espaços, minímo 5 digitos): ")

                # Se, houver espaços ou a senha tiver menos de 5 caracteres, ela é inválida
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


#Lista que simula o "banco de dados", guarda todos os exames
'''
    EXEMPLO DE EXAME CASO QUEIRA DEIXAR ALGUNS DE EXEMPLO
    {
        "tipo_atendimento": tipo_exame (presencial, online, hibrido)
        "nome_exame": nome_exame
    },
'''
lista_exames = [
    {
        "tipo_atendimento": "Presencial",
        "nome_exame": "Eletrocardiograma"
    },
    {
        "tipo_atendimento": "Online",
        "nome_exame": "Avaliação Psicológica"
    },
    {
        "tipo_atendimento": "Híbrido",
        "nome_exame": "Consulta Médica com Teletriagem e Coleta Presencial"
    }
]

lista_exames_feitos = [
    {
        "tipo_atendimento": "Presencial",
        "nome_exame": "Eletrocardiograma",
        "resultado_exame": "Estável"
    },
    {
        "tipo_atendimento": "Online",
        "nome_exame": "Avaliação Psicológica",
        "resultado_exame": "Estável"
    }
]

#Método que mostra a lista de opções do menu de exames
def menu_exames():
    while True:
        print(f"\nMenu exames:"
              f"\n1 - Exames Solicitados;"
              f"\n2 - Solicitar Exame;"
              f"\n3 - Resultados de Exames;"
              f"\n4 - Deletar exame marcado;"
              f"\n5 - Voltar")

        opcao_exames = int(input("Insira o número de sua escolha: "))
        match opcao_exames:
            case 1:
                print("Lista de Exames a serem Agendados: \n")

                #Itera sobre os exames na lista de exames e os mostra de forma organizada
                for exame in lista_exames:
                    print(f"--------------------------"
                          f"\nTipo de Atendimento: {exame.get("tipo_atendimento")};"
                          f"\nNome do Exame: {exame.get("nome_exame")};"
                          )
                print("--------------------------")

            case 2:
                informacoes_corretas = False

                tipo_atendimento = ""
                nome_exame = ""

                #Só sairá do looping quando as informações do novo exame forem válidas
                while not informacoes_corretas:
                    tipo_atendimento = input("Insira o tipo de atendimento (Presencial/Online/Híbrido): ")

                    '''
                        Validação básica e passível a melhoria do tipo de atendimento
                    '''
                    if not "prese" in tipo_atendimento.lower() and not "onli" in tipo_atendimento.lower() and not "hibr" in tipo_atendimento.lower() and not "híbr" in tipo_atendimento.lower():
                        print("Tipo de atendimento inválido")
                        continue

                    nome_exame = input("Insira o nome do exame (Min. 3 caracteres): ")

                    # Se o nome do exame tiver menos de 3 caracteres, ele provavelmente está inválido, então o mínimo é 3
                    if len(nome_exame) < 3:
                        print("Nome do exame deve ter no mínimo 3 caracteres!")
                        continue

                    informacoes_corretas = True

                    #Salva o novo exame num dictionary
                    novo_exame = {
                        "tipo_atendimento": tipo_atendimento,
                        "nome_exame": nome_exame
                    }

                    #Adiciona o novo exame à lista de exames
                    lista_exames.append(novo_exame)

                    print("Exame adicionado a lista com sucesso!")

            case 3:
                print("Lista de Exames Feitos: \n")

                #Itera sobre a lista de exames feitos e os mostra de forma organizada
                for exame_feito in lista_exames_feitos:
                    print(f"--------------------------"
                          f"\nTipo de Atendimento: {exame_feito.get("tipo_atendimento")};"
                          f"\nNome do Exame: {exame_feito.get("nome_exame")};"
                          f"\nResultado do Exame: {exame_feito.get("resultado_exame")}"
                          )
                    print("--------------------------")

            case 4:
                print("\nRemover Exame Marcado: ")

                exame_escolhido = False

                #Enquanto um exame não for escolhido para deletar, o loop continuará
                while not exame_escolhido:
                    #Se a lista de exames tiver tamanho 0, não é possível deletar nenhum visto que não há nenhum
                    if len(lista_exames) == 0:
                        print("Você não possui nenhum exame a ser agendado!")
                    else:
                        #Id para seleção por parte do paciente, começa no 1 por convenções sociais, mas a lista começa com 0
                        id_exame = 1

                        #Itera sobre a lista de exames, e mostra cada um com um id para ser selecionado
                        for exame in lista_exames:
                            print(f"--------------------------"
                                  f"\n{id_exame} - Nome do exame: {exame.get("nome_exame")}"
                                  f"\nTipo de Atendimento: {exame.get("tipo_atendimento")}")

                            #O próximo exame a ser mostrado terá um id diferente, nesse caso maior
                            id_exame += 1

                    print("--------------------------\n\n"
                          "0 - Voltar")

                    selecao_deletar_exame = int(
                        input("Insira o número identificador do exame a ser agendado que deseja remover: "))

                    #Paciente desisitu de deletar um exame, voltar e quebrar o loop
                    if selecao_deletar_exame == 0:
                        exame_escolhido = True
                        continue

                    #Se o id selecionado pelo usuário for negativo ou maior que a quantidade de exames, é inválido
                    elif selecao_deletar_exame < 0 or selecao_deletar_exame > len(lista_exames):
                        print("Identificador inválido, tente novamente.")
                        continue

                    else:
                        #Remover o exame na posição selecionada pelo usuário (subtrai 1, porque a lista começa no indíce 0)
                        lista_exames.pop(selecao_deletar_exame - 1)
                        exame_escolhido = True

            case 5:
                print("\n\nVoltando.")
                break

            case _:
                print("\nOpção inválida.")
                continue

#Lista que simula o "banco de dados", guarda todos as prescrições ativas
'''
    EXEMPLO DE PRESCRIÇÃO CASO QUEIRA DEIXAR ALGUMAS DE EXEMPLO
    {
        "medicamento": "Dipirona 5ml",
        "data_inicio": "06/05/2025",
        "data_validade": "11/05/2025",
    },
'''
lista_prescricoes_ativas = [
    {
        "nome_medicamento": "Dipirona 5ml",
        "data_inicio": "06/05/2025",
        "data_validade": "11/05/2025",
    },
    {
        "nome_medicamento": "Amoxicilina 500mg",
        "data_inicio": "04/05/2025",
        "data_validade": "10/05/2025"
    },
    {
        "nome_medicamento": "Ibuprofeno 200mg",
        "data_inicio": "05/05/2025",
        "data_validade": "09/05/2025"
    }
]

lista_prescricoes_inativas = [
    {
        "nome_medicamento": "Dramin 10ml",
        "data_vencimento": "11/05/2025"
    },
    {
        "nome_medicamento": "Vitamina D 50mg",
        "data_vencimento": "10/05/2025"
    },
]

#Método que mostra a lista de opções do menu de prescrições
def menu_prescricoes():
    while True:
        print(f"\nMenu prescrições:"
              f"\n1 - Prescrições Ativas;"
              f"\n2 - Prescrições Vencidas;"
              f"\n3 - Voltar")

        opcao_prescricoes = int(input("Insira o número de sua escolha: "))
        match opcao_prescricoes:
            case 1:
                print("Lista de Prescrições Ativas: \n")
                #Itera sobre a lista de prescrições ativas e mostra cada uma de forma organizada
                for prescricao_ativa in lista_prescricoes_ativas:
                    print(f"--------------------------"
                          f"\nNome do medicamento: {prescricao_ativa.get("nome_medicamento")};"
                          f"\nData de início de uso: {prescricao_ativa.get("data_inicio")};"
                          f"\nData de validade: {prescricao_ativa.get("data_validade")}"
                          )
                print("--------------------------")

            #Itera sobre a lista de prescrições inativas e mostra cada uma de forma organizada
            case 2:
                print("Lista de Prescrições Inativas: \n")
                for prescricao_inativa in lista_prescricoes_inativas:
                    print(f"--------------------------"
                          f"\nNome do medicamento: {prescricao_inativa.get("nome_medicamento")};"
                          f"\nData de vencimento: {prescricao_inativa.get("data_vencimento")}"
                          )
                print("--------------------------")

            case 3:
                print("\n\nVoltando.")
                break

            case _:
                print("Opção inválida.")
                continue



#Lista que simula o "banco de dados", guarda todos as vacinações feitas
'''
    EXEMPLO DE VACINAÇÃO CASO QUEIRA DEIXAR ALGUMAS DE EXEMPLO
    {
        "vacina": "Hepatite B",
        "data_aplicacao": "10/03/2025",
        "validade": "10/03/2035"
    },
'''
lista_vacinacoes_anteriores = [
    {
        "vacina": "Hepatite B",
        "data_aplicacao": "10/03/2025",
        "validade": "10/03/2035"
    },
    {
        "vacina": "Febre Amarela",
        "data_aplicacao": "15/02/2020",
        "validade": "15/02/2030"
    },
    {
        "vacina": "Influenza (Gripe)",
        "data_aplicacao": "01/04/2025",
        "validade": "01/04/2026"
    }
]

#Lista que simula o "banco de dados", guarda todos os convênios médicos
'''
    EXEMPLO DE CONVÊNIO CASO QUEIRA DEIXAR ALGUM DE EXEMPLO
    {
        "operadora": "Unimed",
        "numero_carteirinha": "1234567890",
        "inicio_vigencia": "01/01/2023",
        "validade": "31/12/2025"
    },
'''
lista_convenios_medicos = [
    {
        "operadora": "Unimed",
        "numero_carteirinha": "1234567890",
        "inicio_vigencia": "01/01/2023",
        "validade": "31/12/2025"
    },
    {
        "operadora": "Bradesco Saúde",
        "numero_carteirinha": "BRD987654321",
        "inicio_vigencia": "15/06/2022",
        "validade": "14/06/2024"
    },
    {
        "operadora": "Amil",
        "numero_carteirinha": "AML11223344",
        "inicio_vigencia": "20/09/2024",
        "validade": "19/09/2026"
    }
]



#Lista que simula o "banco de dados", guarda todos os relatórios médicos
'''
    EXEMPLO DE RELATÓRIO CASO QUEIRA DEIXAR ALGUM DE EXEMPLO
    {
        "medico": "Dra. Ana Paula Ribeiro",
        "data_relatorio": "12/03/2024",
        "descricao": "Relato de dor abdominal persistente. Solicitado ultrassom e exames laboratoriais."
    },
'''
lista_relatorios_medicos = [
    {
        "medico": "Dra. Ana Paula Ribeiro",
        "data_relatorio": "12/03/2024",
        "descricao": "Relato de dor abdominal persistente. Solicitado ultrassom e exames laboratoriais."
    },
    {
        "medico": "Dr. Carlos Henrique Silva",
        "data_relatorio": "05/11/2023",
        "descricao": "Acompanhamento pós-operatório de apendicectomia. Evolução dentro do esperado."
    },
    {
        "medico": "Dra. Juliana Mendes",
        "data_relatorio": "20/07/2022",
        "descricao": "Crise de enxaqueca frequente. Iniciada medicação preventiva e encaminhamento para neurologista."
    }
]

#Método que mostra a lista de opções do menu de documentos necessários
def menu_documentos_necessarios():
    while True:
        print(f"\nMenu Documentos Necessários:"
              f"\n1 - Carteirinha de Vacinação"
              f"\n2 - Convênio Médico;"
              f"\n3 - Relatórios Médicos Anteriores"
              f"\n4 - Voltar")

        opcao_documentos_necessarios = int(input("Insira o número de sua escolha: "))

        match opcao_documentos_necessarios:
            case 1:
                print(f"\n\nCarteirinha de Vacinação:"
                      f"\n1 - Listar vacinações anteriores;"
                      f"\n2 - Adicionar vacinação;"
                      f"\n3 - Voltar")

                opcao_carteirinha_vacinacao = int(input("Insira o número de sua escolha: "))
                match opcao_carteirinha_vacinacao:
                    case 1:
                        print("Lista de Vacinações feitas: \n")
                        #Itera sobre a lista de vacinações feitas anteriormente e mostra cada uma de forma organizada
                        for vacinacao in lista_vacinacoes_anteriores:
                            print(f"--------------------------"
                                  f"\nVacina: {vacinacao.get("vacina")};"
                                  f"\nData de Aplicação: {vacinacao.get("data_aplicacao")};"
                                  f"\nData de Validade: {vacinacao.get("validade")}"
                                  )
                        print("--------------------------")

                    case 2:
                        informacoes_corretas = False

                        nome_vacina = ""
                        data_aplicacao = ""
                        data_validade = ""

                        #Loop ocorrerá enquanto as informações para uma nova vacinação forem inválidas
                        while not informacoes_corretas:
                            nome_vacina = input("Insira o nome da Vacina: ")

                            #Se, tirando todos os espaçoes, o nome da vacina tiver 0 caracteres, ele é inválido
                            if len(nome_vacina.strip(" ")) < 1:
                                print("Nome inválido")
                                continue

                            data_aplicacao = input("Insira a data de aplicação da vacina (dd/mm/aaaa): ")

                            #A data, por ser uma string, precisa conter 8 caracteres no minimo (barras incluidas)
                            if len(data_aplicacao) < 8:
                                print("Data de aplicação inválida")
                                continue

                            data_validade = input("Insira a data de validade da vacina (dd/mm/aaaa): ")

                            # A data, por ser uma string, precisa conter 8 caracteres no minimo (barras incluidas)
                            if len(data_aplicacao) < 8:
                                print("Data de validade inválida")
                                continue

                            informacoes_corretas = True

                            # Salva a nova vacinação num dictionary
                            nova_vacinacao = {
                                "vacina": nome_vacina,
                                "data_aplicacao": data_aplicacao,
                                "validade": data_validade
                            }

                            # Adiciona o dictionary da nova vacinação na lista de vacinações
                            lista_vacinacoes_anteriores.append(nova_vacinacao)

                            print("Vacina adicionada à lista com sucesso!")

                    case 3:
                        print("\n\nVoltando.")
                        break

                    case _:
                        print("Opção inválida.")
                        continue

            case 2:
                print(f"\n\nConvênios Médicos:"
                      f"\n1 - Listar convênios médicos;"
                      f"\n2 - Adicionar convênio médico;"
                      f"\n3 - Voltar")

                opcao_convenio_medico = int(input("Insira o número de sua escolha: "))
                match opcao_convenio_medico:
                    case 1:
                        print("Lista de Convênios Médicos: \n")
                        #Itera sobre a lista de convênios médicos e mostra cada um de forma organizada
                        for convenio in lista_convenios_medicos:
                            print(f"--------------------------"
                                  f"\nOperadora: {convenio.get("operadora")};"
                                  f"\nNúmero da Carteirinha: {convenio.get("numero_carteirinha")};"
                                  f"\nInício da Vigência: {convenio.get("inicio_vigencia")};"
                                  f"\nData de Validade: {convenio.get("validade")}"
                                  )
                        print("--------------------------")

                    case 2:
                        informacoes_corretas = False

                        nome_operadora = ""
                        numero_carteirinha = ""
                        inicio_vigencia = ""
                        data_validade = ""

                        #Enquanto as informações não forem válidas, o loop continuará acontecendo
                        while not informacoes_corretas:
                            nome_operadora = input("Insira o nome da Operadora: ")

                            #Se, sem espaços, o nome da operadora tiver 0 caracteres, ele é inválido
                            if len(nome_operadora.strip(" ")) < 1:
                                print("Nome inválido")
                                continue

                            numero_carteirinha = input("Insira o número da carteirinha: ")

                            #Se o número da carteirinha tiver menos que 3 caracteres, ele é inválido
                            if len(numero_carteirinha) < 3:
                                print("Número da carteirinha inválido")
                                continue

                            inicio_vigencia = input("Insira a data de início da vigência de carteirinha (dd/mm/aaaa): ")

                            #Se o ano de inicio tiver menos que 8 caracteres, ele é invalido (deve incluir as barras)
                            if len(inicio_vigencia) < 8:
                                print("Data de validade inválida")
                                continue

                            data_validade = input(
                                "Insira a data de validade da carteirinha (dd/mm/aaaa): ")

                            # Se o ano de validade tiver menos que 8 caracteres, ele é invalido (deve incluir as barras)
                            if len(data_validade) < 8:
                                print("Data de validade inválida")
                                continue

                            informacoes_corretas = True

                            #Salva o novo convênio num dictionary
                            novo_convenio = {
                                "operadora": nome_operadora,
                                "numero_carteirinha": numero_carteirinha,
                                "inicio_vigencia": inicio_vigencia,
                                "validade": data_validade
                            }

                            #Adiciona o dictionary do novo convênio na lista de convênios
                            lista_convenios_medicos.append(novo_convenio)

                            print("Convênio adicionado à lista com sucesso!")

                    case 3:
                        print("\n\nVoltando.")
                        break

                    case _:
                        print("Opção inválida.")
                        continue

            case 3:
                print(f"\n\nRelatórios Médicos:"
                      f"\n1 - Listar relatórios médicos;"
                      f"\n2 - Adicionar relatório médico;"
                      f"\n3 - Voltar")

                opcao_relatorio_medico = int(input("Insira o número de sua escolha: "))
                match opcao_relatorio_medico:
                    case 1:
                        print("Lista de Relatórios Médicos: \n")
                        #Itera sobre os relatórios na lista de relatórios médicos e mostra-os de forma organizada
                        for relatorio in lista_relatorios_medicos:
                            print(f"--------------------------"
                                  f"\nNome do(a) Médico(a): {relatorio.get("medico")};"
                                  f"\nData de Emissão do Relatório: {relatorio.get("data_relatorio")};"
                                  f"\nDescrição: {relatorio.get("descricao")}"
                                  )
                        print("--------------------------")

                    case 2:
                        informacoes_corretas = False

                        nome_medico = ""
                        data_emissao = ""
                        descricao = ""

                        #O loop ocorrerá enquanto as informações não forem válidas
                        while not informacoes_corretas:
                            nome_medico = input("Insira o nome do(a) Médico(a): ")

                            #Se, removendo os espaços, o nome tiver 0 caracteres, ele é inválido
                            if len(nome_medico.strip(" ")) < 1:
                                print("Nome inválido")
                                continue

                            data_emissao = input("Insira a Data de Emissão do Relatório (dd/mm/aaaa): ")

                            # Se a data de emissão tiver menos que 8 caracteres, ela é invalida (deve incluir as barras)
                            if len(data_emissao) < 8:
                                print("Data de validade inválida")
                                continue

                            descricao = input("Insira uma breve descrição do relatório: ")

                            #Se a descrição tiver menos que 2 caracteres, ela é inválida
                            if len(descricao) < 2:
                                print("Relatório inválido, muito breve.")
                                continue

                            informacoes_corretas = True

                            #Salva o novo relatório num dictionary
                            novo_relatorio = {
                                "medico": nome_medico,
                                "data_relatorio": data_emissao,
                                "descricao": descricao
                            }

                            #Salva o dictionary na lista de relatórios
                            lista_relatorios_medicos.append(novo_relatorio)

                            print("Relatório Médico adicionado à lista com sucesso!")

                    case 3:
                        print("\n\nVoltando.")
                        break

                    case _:
                        print("Opção inválida.")
                        continue

            case 4:
                print("\n\nVoltando.")
                break

            case _:
                print("Opção inválida.")
                continue

#Método que mostra o menu de ajuda
def menu_ajuda():
    while True:
        print(f"Menu de Ajuda:"
              f"\n\nSe o sistema não estiver carregando corretamente, tente atualizar a página, "
              f"utilizar outro navegador ou verificar sua conexão com a internet."
              f"\n\nPara ajuda personalizada, entre em contato com o suporte"
              f"\nTelefone: (11) 2661-1048"
              f"\nTelefone: (11) 2661-1561"
              f"\nE-mail: ouvidoria.geral@hc.fm.usp.br")

        voltar_para_menu = input("\nVoltar para o menu? (Sim/Não): ")
        if checarInputSim(voltar_para_menu):
            print("\n\nVoltando.")
            break
        else:
            #Se o paciente não quiser voltar para o menu principal, ele verá o menu de ajuda novamente
            continue

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

#Loop será infinito até o usuário voluntariamente sair
while True:
    '''Usa o input retornado do método que demonstra o menu de escolhas do paciente e guarda numa variavel, é relativamente
    grande, logo coloquei num método a parte para não poluir o flow principal'''
    opcao_menu = menu_paciente_escolha()

    match opcao_menu:
        case 1:
            menu_agendamentos()

        case 2:
            menu_meus_dados()

        case 3:
            menu_exames()

        case 4:
            menu_prescricoes()

        case 5:
            menu_documentos_necessarios()

        case 6:
            menu_ajuda()

        case 7:
            print("Muito obrigado por utilizar o sistema de pacientes da HC, desenvolvido por estudantes da FIAP!")
            print("Saindo...")
            break

        case _:
            print("Opção inválida!")
            continue