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

                while not informacoes_corretas:
                    tipo_atendimento = input("Insira o tipo de atendimento (Presencial/Online/Híbrido): ")

                    if not "prese" in tipo_atendimento.lower() and not "onli" in tipo_atendimento.lower() and not "hibr" in tipo_atendimento.lower() and not "híbr" in tipo_atendimento.lower():
                        print("Tipo de atendimento inválido")
                        continue

                    nome_exame = input("Insira o nome do exame (Min. 3 caracteres): ")

                    if len(nome_exame) < 3:
                        print("Nome do exame deve ter no mínimo 3 caracteres!")
                        continue

                    informacoes_corretas = True
                    novo_exame = {
                        "tipo_atendimento": tipo_atendimento,
                        "nome_exame": nome_exame
                    }

                    lista_exames.append(novo_exame)

                    print("Exame adicionado a lista com sucesso!")

            case 3:
                print("Lista de Exames Feitos: \n")
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
                while not exame_escolhido:
                    if len(lista_exames) == 0:
                        print("Você não possui nenhum exame a ser agendado!")
                    else:
                        id_exame = 1
                        for exame in lista_exames:
                            print(f"--------------------------"
                                  f"\n{id_exame} - Nome do exame: {exame.get("nome_exame")}"
                                  f"\nTipo de Atendimento: {exame.get("tipo_atendimento")}")
                            id_exame += 1

                    print("--------------------------\n\n"
                          "0 - Voltar")

                    selecao_deletar_exame = int(
                        input("Insira o número identificador do exame a ser agendado que deseja remover: "))

                    if selecao_deletar_exame == 0:
                        exame_escolhido = True
                        continue

                    elif selecao_deletar_exame < 0 or selecao_deletar_exame > len(lista_exames):
                        print("Identificador inválido, tente novamente.")
                        continue

                    else:
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
                for prescricao_ativa in lista_prescricoes_ativas:
                    print(f"--------------------------"
                          f"\nNome do medicamento: {prescricao_ativa.get("nome_medicamento")};"
                          f"\nData de início de uso: {prescricao_ativa.get("data_inicio")};"
                          f"\nData de validade: {prescricao_ativa.get("data_validade")}"
                          )
                print("--------------------------")

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

                        while not informacoes_corretas:
                            nome_vacina = input("Insira o nome da Vacina: ")

                            if len(nome_vacina.strip(" ")) < 1:
                                print("Nome inválido")
                                continue

                            data_aplicacao = input("Insira a data de aplicação da vacina (dd/mm/aaaa): ")

                            if len(data_aplicacao) < 8:
                                print("Data de aplicação inválida")
                                continue

                            data_validade = input("Insira a data de validade da vacina (dd/mm/aaaa): ")

                            if len(data_aplicacao) < 8:
                                print("Data de validade inválida")
                                continue

                            informacoes_corretas = True
                            nova_vacinacao = {
                                "vacina": nome_vacina,
                                "data_aplicacao": data_aplicacao,
                                "validade": data_validade
                            }

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

                        while not informacoes_corretas:
                            nome_operadora = input("Insira o nome da Operadora: ")

                            if len(nome_operadora.strip(" ")) < 1:
                                print("Nome inválido")
                                continue

                            numero_carteirinha = input("Insira o número da carteirinha: ")

                            if len(numero_carteirinha) < 3:
                                print("Número da carteirinha inválido")
                                continue

                            inicio_vigencia = input("Insira a data de início da vigência de carteirinha (dd/mm/aaaa): ")

                            if len(inicio_vigencia) < 8:
                                print("Data de validade inválida")
                                continue

                            data_validade = input(
                                "Insira a data de validade da carteirinha (dd/mm/aaaa): ")

                            if len(data_validade) < 8:
                                print("Data de validade inválida")
                                continue

                            informacoes_corretas = True
                            novo_convenio = {
                                "operadora": nome_operadora,
                                "numero_carteirinha": numero_carteirinha,
                                "inicio_vigencia": inicio_vigencia,
                                "validade": data_validade
                            }

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

                        while not informacoes_corretas:
                            nome_medico = input("Insira o nome do(a) Médico(a): ")

                            if len(nome_medico.strip(" ")) < 1:
                                print("Nome inválido")
                                continue

                            data_emissao = input("Insira a Data de Emissão do Relatório (dd/mm/aaaa): ")

                            if len(data_emissao) < 8:
                                print("Data de validade inválida")
                                continue

                            descricao = input("Insira uma breve descrição do relatório: ")

                            if len(descricao) < 2:
                                print("Relatório inválido, muito breve.")
                                continue

                            informacoes_corretas = True
                            novo_relatorio = {
                                "medico": nome_medico,
                                "data_relatorio": data_emissao,
                                "descricao": descricao
                            }

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
            continue


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