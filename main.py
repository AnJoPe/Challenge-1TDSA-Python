import random
import time
from datetime import datetime

import re as regex
import requests
import json

api_url = "https://api-sistema-hc.onrender.com"


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



#Função que cadastra o convênio médico do paciente no banco de dados
def criarConvenioMedico(convenio, id_paciente):
    try:
        response_api = requests.post(f"{api_url}/convenio_medico", json={
            "operadora": convenio["operadora"],
            "numeroCarteirinha": convenio["codigo"],
            "idPaciente":id_paciente
        })

        return response_api.json()
    except requests.exceptions.RequestException as erro:
        print(f'Erro na requisição: {erro}')
        return None
    except Exception as e:
        print(f'Erro: {e}')
        return None

#Função que cadastra o perfil médico do paciente no banco de dados
def criarPerfilPaciente(perfil_paciente):
    try:
        response_api = requests.post(f"{api_url}/paciente", json={
            "nomePaciente": perfil_paciente["nome_completo"],
            "idade": perfil_paciente["idade"],
            "altura": perfil_paciente["altura"],
            "peso": perfil_paciente["peso"],
            "rg": perfil_paciente["rg"],
            "cpf": perfil_paciente["cpf"],
            "telefone": perfil_paciente["telefone"],
            "endereco": {
                "logradouro": perfil_paciente["endereco"]["logradouro"],
                "numero": perfil_paciente["endereco"]["numero"],
                "bairro": perfil_paciente["endereco"]["bairro"],
                "cidade": perfil_paciente["endereco"]["cidade"],
                "cep": perfil_paciente["endereco"]["cep"]
            },
            "sexo": perfil_paciente["sexo"]
        })

        print(f'Paciente cadastrado com sucesso!')

        perfil_paciente["id_paciente"] = response_api.json()

        return perfil_paciente
    except requests.exceptions.RequestException as erro:
        print(f'Erro na requisição: {erro}')
        return None
    except Exception as e:
        print(f'Erro: {e}')
        return None


#Função que cadastra a conta do paciente no banco de dados
def criarContaPaciente(dadosPaciente):
    try:
        response_api = requests.post(f"{api_url}/conta_paciente", json={
            "email": dadosPaciente["email"],
            "senha": dadosPaciente["senha"],
            "paciente": {
                "id": dadosPaciente["id_paciente"]
            },
            "convenioMedico": {
                "id": dadosPaciente["id_convenio"]
            }
        })

        print(f'Conta cadastrada com sucesso!')
        dadosPaciente["id_conta_paciente"] = response_api.json()

        return dadosPaciente
    except requests.exceptions.RequestException as erro:
        print(f'Erro na requisição: {erro}')
        return None

    except Exception as e:
        print(f'Erro: {e}')
        return None

#Função que retorna a conta do paciente no banco de dados procurada pelo email
def selectContaPacientePorEmail(email):
    try:
        response_api = requests.get(f"{api_url}/conta_paciente/email/{email}")

        if not response_api.json():
            return None
        else:
            conta = {
                "id_conta_paciente": response_api.json()["id"],
                "email": response_api.json()["email"],
                "senha": response_api.json()["senha"],
                "fk_id_paciente": response_api.json()["paciente"]["id"],
                "fk_id_convenio": response_api.json()["convenioMedico"]["id"]
            }

            return conta

    except requests.exceptions.RequestException as erro:
        print(f'Erro na requisição: {erro}')
        return None

    except Exception as e:
        print(f'Erro: {e}')
        return None

#Função que retorna a conta do paciente no banco de dados procurada pelo ID
def selectContaPacientePorId(id):
    try:
        response_api = requests.get(f"{api_url}/conta_paciente/{id}")

        if not response_api.json():
            return None
        else:
            conta = {
                "id_conta_paciente": response_api.json()["id"],
                "email": response_api.json()["email"],
                "senha": response_api.json()["senha"],
                "fk_id_paciente": response_api.json()["paciente"]["id"],
                "fk_id_convenio": response_api.json()["convenioMedico"]["id"]
            }

            return conta

    except requests.exceptions.RequestException as erro:
        print(f'Erro na requisição: {erro}')
        return None

    except Exception as e:
        print(f'Erro: {e}')
        return None

#Função que retorna o id do perfil médico do paciente no banco de dados, procurado pelo RG
def selectIdPerfilPacientePorRg(rg):
    try:
        response_api = requests.get(f"{api_url}/paciente/rg/{rg}")

        if not response_api.json():
            return None
        else:

            return response_api.json()

    except requests.exceptions.RequestException as erro:
        print(f'Erro na requisição: {erro}')
        return None

    except Exception as e:
        print(f'Erro: {e}')
        return None

#Função que retorna o paciente no banco de dados procurada pelo ID
def selectPacientePorId(id):
    try:
        response_api = requests.get(f"{api_url}/paciente/{id}")

        if not response_api.json():
            return None
        else:
            paciente = {
                'id_paciente': response_api.json()["id"],
                'num_tel': response_api.json()["telefone"],
                'ds_endereco': response_api.json()["endereco"],
                'nm_paciente': response_api.json()["nomePaciente"],
                'num_idade': response_api.json()["idade"],
                'ds_sexo_paciente': response_api.json()["sexo"],
                'num_altura': response_api.json()["altura"],
                'num_peso': response_api.json()["peso"],
                'ds_rg': response_api.json()["rg"],
                'ds_cpf': response_api.json()["cpf"]
            }

            return paciente

    except requests.exceptions.RequestException as erro:
        print(f'Erro na requisição: {erro}')
        return None

    except Exception as e:
        print(f'Erro: {e}')
        return None

#Método que loga ou registra o usuário no sistema
def loginERegistro():
    esta_logado = False

    conta_paciente = {}
    info_paciente = {}

    # Loop de logar/registrar, roda enquanto não estiver logado
    while not esta_logado:
        time.sleep(.2)
        possui_registro = input("Você já possui um cadastro? (Sim/Não): ")
        time.sleep(.4)
        # Checa as variações mais comuns de "não", só por via das dúvidas
        if checarInputNao(possui_registro):
            print("Certo, prosseguiremos com o processo de registro.\n")
            time.sleep(.35)

            # WHILE DE REGISTRO - SUPER IMPORTANTE!!!
            while not esta_logado:
                email_registro = input("Insira o seu email: ")
                time.sleep(.45)

                padrao_email = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
                if not regex.match(padrao_email, email_registro):
                    print("\nEmail inválido, tente novamente.")
                    continue

                senha_registro = input("Insira a sua senha (mínimo 5 caracteres, sem espaço): ")
                time.sleep(.45)

                if len(senha_registro) < 5 or " " in senha_registro:
                    print("Senha inválida, não use espaços e use no mínimo 5 caracteres.")
                    continue

                print("\nRegistro de conta realizado com sucesso, agora cadastraremos os seus dados de paciente.\n\n")

                cadastrado = False
                while not cadastrado:
                    perfil_paciente = {
                        "nome_completo": "",
                        "telefone": "",
                        "idade": -1,
                        "sexo": "",
                        "altura": -1,
                        "peso": -1,
                        "rg": "",
                        "cpf": "",
                        "endereco": {}
                    }

                    time.sleep(.5)
                    while True:
                        nome_completo = input("Insira o seu nome completo, por favor: ")
                        if len(nome_completo.replace(" ", "")) == 0:
                            print("Nome inválido, tente novamente.")
                            continue

                        else:
                            perfil_paciente["nome_completo"] = nome_completo
                            break

                    time.sleep(.5)
                    while True:
                        telefone = input("Insira o seu telefone completo, por favor (Sem () e/ou -): ")
                        telefone = telefone.replace("-", "")
                        telefone = telefone.replace("(", "")
                        telefone = telefone.replace(")", "")
                        telefone = telefone.replace(" ", "")
                        if len(telefone) == 0:
                            print("Telefone inválido, tente novamente.")
                            continue

                        else:
                            perfil_paciente["telefone"] = telefone
                            break

                    time.sleep(.5)
                    while True:
                        try:
                            idade = int(input("Insira a sua idade, por favor: "))
                            if idade < 0 or idade > 130:
                                print("Idade inválida, tente novamente.")
                                continue
                            else:
                                perfil_paciente["idade"] = idade
                                break
                        except:
                            print("Por favor, insira um número válido.")
                            continue

                    time.sleep(.5)
                    while True:
                        sexo = input("Insira o seu sexo, por favor: ")
                        if len(sexo.replace(" ", "")) == 0:
                            print("Sexo inválido, tente novamente.")
                            continue
                        else:
                            perfil_paciente["sexo"] = sexo
                            break

                    time.sleep(.5)
                    while True:
                        try:
                            altura = float(input("Insira a sua altura, por favor: "))
                            if altura < 0:
                                print("Altura inválida, tente novamente.")
                                continue

                            # De Centímetros para Metros
                            if altura >= 100:
                                altura /= 100

                            perfil_paciente["altura"] = altura
                            break
                        except:
                            print("Por favor, insira uma altura válida.")
                            continue

                    time.sleep(.5)
                    while True:
                        try:
                            peso = float(input("Insira o sua peso, por favor: "))
                            if peso < 0:
                                print("Peso inválido, tente novamente.")
                                continue

                            perfil_paciente["peso"] = peso
                            break
                        except:
                            print("Por favor, insira um peso válido.")
                            continue

                    time.sleep(.5)
                    while True:
                        registro_geral = input("Insira o seu RG, por favor (sem . ou -): ")
                        registro_geral = registro_geral.replace(" ", "")
                        if len(registro_geral) == 0 or len(registro_geral) < 5 or len(registro_geral) > 15:
                            print("RG inválido, tente novamente.")
                            continue

                        else:
                            perfil_paciente["rg"] = registro_geral
                            break

                    time.sleep(.5)
                    while True:
                        cadastro_pessoa_fisica = input("Insira o seu CPF, por favor (sem . ou -): ")
                        cadastro_pessoa_fisica = cadastro_pessoa_fisica.replace(" ", "")
                        if len(cadastro_pessoa_fisica) == 0 or len(cadastro_pessoa_fisica) < 5 or len(
                                cadastro_pessoa_fisica) > 15:
                            print("CPF inválido, tente novamente.")
                            continue

                        else:
                            perfil_paciente["cpf"] = cadastro_pessoa_fisica
                            break

                    time.sleep(.55)
                    print("\nPerfil de paciente criado com sucesso, resta apenas alguns ajustes finais...\n\n")
                    time.sleep(.35)
                    print(
                        "Registraremos o seu endereço ao seu perfil de paciente. Protegemos suas informações com o máximo de cuidado!\n\n")

                    endereco = {
                        "logradouro": "",
                        "numero": -1,
                        "bairro": "",
                        "cidade": "",
                        "cep": ""
                    }

                    time.sleep(.5)
                    while True:
                        logradouro = input("Insira o logradouro, por favor: ")
                        if len(logradouro.replace(" ", "")) == 0:
                            print("Logradouro inválido, tente novamente.")
                            continue

                        else:
                            endereco["logradouro"] = logradouro
                            break

                    time.sleep(.5)
                    while True:
                        try:
                            numero = int(input("Insira o número, por favor: "))
                            if numero < 0:
                                print("Número inválido, tente novamente.")
                                continue
                            else:
                                endereco["numero"] = numero
                                break
                        except:
                            print("Por favor, insira um número válido.")
                            continue

                    time.sleep(.5)
                    while True:
                        bairro = input("Insira o bairro, por favor: ")
                        if len(bairro.replace(" ", "")) == 0:
                            print("Bairro inválido, tente novamente.")
                            continue

                        else:
                            endereco["bairro"] = bairro
                            break

                    time.sleep(.5)
                    while True:
                        cidade = input("Insira a cidade, por favor: ")
                        if len(cidade.replace(" ", "")) == 0:
                            print("Cidade inválida, tente novamente.")
                            continue

                        else:
                            endereco["cidade"] = cidade
                            break

                    time.sleep(.5)
                    while True:
                        cep = input("Insira o CEP, por favor (sem -): ")
                        cep = cep.replace("-", "")

                        if len(cep.replace(" ", "")) == 0:
                            print("CEP inválido, tente novamente.")
                            continue

                        else:
                            endereco["cep"] = cep
                            break

                    perfil_paciente["endereco"] = endereco

                    time.sleep(.55)
                    print("\nAgradecemos pela colaboração...\n\n")

                    info_paciente = criarPerfilPaciente(perfil_paciente)

                    if not info_paciente:
                        print("Falha na criação. Finalizando o programa.")

                    time.sleep(.35)
                    print("Registraremos agora o seu Convênio Médico")

                    convenio_medico = {
                        "operadora": "",
                        "codigo": ""
                    }

                    time.sleep(.5)
                    while True:
                        operadora = input("Insira a operadora, por favor: ")
                        if len(operadora.replace(" ", "")) == 0:
                            print("Operadora inválida, tente novamente.")
                            continue

                        else:
                            convenio_medico["operadora"] = operadora
                            break

                    time.sleep(.5)
                    while True:
                        codigo = input("Insira o código da carteirinha, por favor: ")
                        if len(codigo.replace(" ", "")) == 0:
                            print("Código inválido, tente novamente.")
                            continue

                        else:
                            convenio_medico["codigo"] = codigo
                            break

                    id_perfil_paciente = selectIdPerfilPacientePorRg(perfil_paciente["rg"])

                    id_convenio = criarConvenioMedico(convenio_medico, id_perfil_paciente)

                    perfil_conta_paciente = {
                        "email": email_registro,
                        "senha": senha_registro,
                        "id_paciente": id_perfil_paciente,
                        "id_convenio": id_convenio
                    }

                    conta_paciente = criarContaPaciente(perfil_conta_paciente)

                    cadastrado = True
                    print("\n\nAgradecemos pela colaboração!\n\n")

                esta_logado = True

                break

        elif checarInputSim(possui_registro):
            print("Certo, efetuaremos a sua autenticação a seguir.\n")
            time.sleep(.35)

            # WHILE DE LOGIN - SUPER IMPORTANTE!!!
            while not esta_logado:
                email_login = input("Insira o seu email: ")
                time.sleep(.45)

                padrao_email = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
                if not regex.match(padrao_email, email_login):
                    print("Email inválido, tente novamente.")
                    continue

                senha_login = input("Insira a sua senha: ")
                time.sleep(.45)

                if len(senha_login) < 5 or " " in senha_login:
                    print("Senha inválida, não use espaços e use no mínimo 5 caracteres.")
                    continue

                # Tenta encontrar os dados da conta através do email
                conta_logada = selectContaPacientePorEmail(email_login)

                time.sleep(.5)
                # Verifica se existe uma conta com esse registro
                if conta_logada is None or not conta_logada:
                    print("\nConta inexistente!\n\n")
                    time.sleep(.4)

                    tentar_novamente = input("Deseja tentar novamente? (Sim/Não): ")
                    if checarInputSim(tentar_novamente):
                        continue
                    else:
                        break

                # Itera sobre cada conta na lista de contas
                # Checa se o email e a senha da conta encontra coincidem com as informações inseridas pelo usuário
                if conta_logada.get('email') == email_login and conta_logada.get('senha') == senha_login:
                    print("\nLogin realizado com sucesso!\n\n")
                    time.sleep(.5)

                    conta_paciente = conta_logada

                    info_paciente = selectPacientePorId(conta_logada["fk_id_paciente"])

                    esta_logado = True
                    break

                # Checa se o email coincide, mas a senha não.
                # Isso significa que a conta existe, mas a senha está errada. Fala pro usuário e reseta o loop
                elif conta_logada.get('email') == email_login and conta_logada.get('senha') != senha_login:
                    print("\nSenha incorreta! \n Tente novamente.\n\n")
                    time.sleep(.3)
                    continue

    return conta_paciente, info_paciente



#Função que retorna todos os agendamentos que têm o id do paciente no banco de dados
def selectAgendamentosPorIdPaciente(id_paciente):
    lista_agendamentos = []

    try:
        response_api = requests.get(f"{api_url}/agendamento/{id_paciente}")

        for agendamento in response_api.json():
            novo_agendamento = {
                "id_agendamento": agendamento["id"],
                "dt_consulta": agendamento["data"],
                "hr_consulta": agendamento["horario"],
                "fk_id_medico": agendamento["medicoResponsavel"]["id"],
                "fk_id_instituicao": agendamento["local"]["id"],
                "fk_id_paciente": agendamento["paciente"]["id"]
            }
            lista_agendamentos.append(novo_agendamento)

    except requests.exceptions.RequestException as erro:
        print(f'Erro na requisição: {erro}')

    except Exception as e:
        print(f'Erro: {e}')

    return lista_agendamentos

#Função que cadastra um novo agendamento no banco de dados
def criarAgendamento(agendamento, id_paciente, id_medico, id_instituicao):
    try:
        dataAgendamento = agendamento["dt_consulta"].strftime("%Y-%m-%d")
        response_api = requests.post(f"{api_url}/agendamento", json={
            "horario": agendamento["hr_consulta"],
            "data": dataAgendamento,
            "paciente": {
                "id": id_paciente
            },
            "local": {
                "id": id_instituicao
            },
            "medicoResponsavel": {
                "id": id_medico
            }
        })

        print(f'Agendamento cadastrado com sucesso!')

        id_agendamento = response_api.json()

        return id_agendamento

    except requests.exceptions.RequestException as erro:
        print(f'Erro na requisição: {erro}')
        return None

    except Exception as e:
        print(f'Erro: {e}')
        return None


#Função que deleta um agendamento do banco de dados
def deleteAgendamentoPorId(id):
    try:
        response_api = requests.delete(f"{api_url}/agendamento/{id}")

        if response_api.status_code == 200:
            print(f'O Agendamento foi excluído com sucesso!')
        else:
            print(f'Nenhum Agendamento com id: {id} foi encontrado!')

    except requests.exceptions.RequestException as erro:
        print(f'Erro na requisição: {erro}')
        return None

    except Exception as e:
        print(f'Erro: {e}')
        return None


#Método que mostra o menu de agendamentos
def menu_agendamentos(id_paciente):
    print("===================================")
    #Ficará rodando até ser quebrado manualmente com um break
    while True:
        lista_agendamentos = selectAgendamentosPorIdPaciente(id_paciente)

        print("\nMenu de Agendamentos:"
              "\n1 - Listar agendamentos;"
              "\n2 - Agendar;"
              "\n3 - Desmarcar agendamento;"
              "\n4 - Voltar;"
              "\n5 - Exportar todos os Agendamentos para JSON."
              "\n")

        opcao_agendamento = int(input("\nInsira o número de sua escolha: "))
        time.sleep(.65)

        match opcao_agendamento:
            case 1:
                print("\nLista de Agendamentos:\n")
                time.sleep(.3)
                #Itera sobre cada agendamento na lista de agendamentos e os mostra de forma organizada utilizando o get()
                for agendamento in lista_agendamentos:
                    medico = selectMedicoPorId(agendamento.get('fk_id_medico'))
                    instituicao = selectInstituicaoPorId(agendamento.get('fk_id_instituicao'))

                    data_formatada = agendamento["dt_consulta"]
                    time.sleep(.5)
                    print(f"--------------------------"
                          f"\nMédico: {medico['nm_medico']};"
                          f"\nData: {data_formatada};"
                          f"\nHorário: {agendamento["hr_consulta"]};"
                          f"\nLocal: {instituicao["nm_razao_social"]}")
                print("--------------------------")

            case 2:
                informacoes_corretas = False

                horario = ""
                data = ""
                medico_responsavel = ""
                instituicao = ""
                paciente = None

                while not informacoes_corretas:
                    print(f"\nNovo agendamento:\n")
                    time.sleep(.3)
                    data_str = input("Por favor, insira a data do agendamento (DD/MM/AAAA): ")
                    time.sleep(.35)
                    horario_str = input("Agora insira o horário no qual o agendamento ocorrerá (HH:MM): ")
                    time.sleep(.5)

                    # Lista de médicos disponíveis
                    lista_medicos = selectMedicos()
                    if not lista_medicos:
                        print("Nenhum médico disponível no momento.")
                        return

                    print("\n=== Lista de Médicos Disponíveis ===")
                    id_agendamento = 1
                    for medico in lista_medicos:
                        print(f"{id_agendamento}. {medico['nm_medico']} — Setor: {medico['ds_setor_medico']}")
                        id_agendamento += 1

                    while True:
                        try:
                            escolha_medico = int(input("\nEscolha o número do médico desejado: "))
                            if 1 <= escolha_medico <= len(lista_medicos):
                                medico = lista_medicos[escolha_medico - 1]
                                break
                            else:
                                print("Opção inválida! Escolha um número válido.")
                        except ValueError:
                            print("Entrada inválida! Digite apenas o número da opção.")

                    # Lista de instituições disponíveis
                    lista_locais = selectInstituicao()
                    if not lista_locais:
                        print("Nenhuma instituição disponível no momento.")
                        return

                    print("\n=== Lista de Instituições ===")
                    id_agendamento = 1
                    for instituicao in lista_locais:
                        endereco = instituicao['ds_endereco']
                        print(f"{id_agendamento}. {instituicao['nm_fantasia']} — {endereco['logradouro']}, {endereco['numero']} - {endereco['bairro']} ({endereco['cidade']} - {endereco['cep']})")
                        id_agendamento += 1

                    while True:
                        try:
                            escolha_local = int(input("\nEscolha o número da instituição desejada: "))
                            if 1 <= escolha_local <= len(lista_locais):
                                local = lista_locais[escolha_local - 1]
                                break
                            else:
                                print("Opção inválida! Escolha um número válido.")
                        except ValueError:
                            print("Entrada inválida! Digite apenas o número da opção.")

                    try:
                        data_agendamento = datetime.strptime(data_str, "%d/%m/%Y")
                        hora, minuto = map(int, horario_str.split(":"))
                        data_hoje = datetime.now()

                        if data_agendamento.year < data_hoje.year:
                            print("O ano não pode ser menor que o atual!")
                            time.sleep(.35)
                            continue

                        if hora < 0 or hora > 23:
                            print("Hora inválida, precisa estar entre 0 e 23.")
                            time.sleep(.35)
                            continue

                        if minuto < 0 or minuto > 59:
                            print("Minutos inválidos, precisam estar entre 0 e 59.")
                            time.sleep(.35)
                            continue

                        novo_agendamento = {
                            "dt_consulta": data_agendamento,
                            "hr_consulta": f"{hora}:{minuto}"
                        }

                        criarAgendamento(
                            novo_agendamento,
                            id_paciente,
                            medico["id_medico"],
                            local["id_instituicao"]
                        )
                        time.sleep(.5)

                    except ValueError:
                        print("Formato inválido! Use DD/MM/AAAA para a data e HH:MM para o horário.")
                        continue

                    informacoes_corretas = True

            case 3:
                print("\nRemover Agendamento:\n")
                time.sleep(.3)

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
                        #Itera sobre cada agendamento na lista de agendamentos, e mostra cada um com um id e suas datas, o local e o médico
                        for agendamento in lista_agendamentos:
                            medico = selectMedicoPorId(agendamento.get('fk_id_medico'))
                            data_formatada = agendamento["dt_consulta"]
                            time.sleep(.5)
                            print(f"--------------------------"
                                  f"\n{id_agendamento} - {agendamento["hr_consulta"]} — {data_formatada}"
                                  f"\nMédico: {medico["nm_medico"]}")
                            #Próximo agendamento terá um id diferente, nesse caso, superior
                            id_agendamento += 1

                    print("--------------------------\n\n"
                          "0 - Voltar")

                    time.sleep(.25)
                    selecao_deletar_agendamento = int(input("\nInsira o número identificador do agendamento que deseja remover: "))
                    time.sleep(.35)

                    #Se for 0, o paciente não quer deletar nenhum, então voltar e quebrar o looping.
                    if selecao_deletar_agendamento == 0:
                        agendamento_escolhido = True
                        continue

                    #Se o seletor for menor que 0, ou maior que o tamanho da lista de agendamentos, ele é inválido
                    elif selecao_deletar_agendamento < 0 or selecao_deletar_agendamento > len(lista_agendamentos):
                        print("Identificador inválido, tente novamente.")
                        time.sleep(.5)
                        continue

                    #Se tudo estiver correto, dar delete no indíce selecionado (subtraindo 1, porque a lista começa do 0)
                    else:
                        id_agendamento_selecionado = lista_agendamentos[selecao_deletar_agendamento - 1]["id_agendamento"]
                        deleteAgendamentoPorId(id_agendamento_selecionado)
                        #Quebrar o looping após o apagamento
                        agendamento_escolhido = True

            case 4:
                print("\nVoltando...")
                time.sleep(.5)
                break

            case 5:
                try:
                    with open("agendamentos.json", "w", encoding="utf-8") as arquivo:
                        json.dump(lista_agendamentos, arquivo, indent=4, ensure_ascii=False)
                    print("Dados exportados com sucesso para 'agendamentos.json'.")
                except Exception as e:
                    print(f"Erro ao exportar dados: {e}")
                break

            case _:
                print("\nOpção inválida!")
                time.sleep(.5)
                continue


#Função que atualiza o telefone do perfil médico do paciente no banco de dados através do ID
def updateTelefonePacientePorId(id, telefone):
    try:
        response_api = requests.put(f"{api_url}/paciente/telefone", json={
            "id": id,
            "telefone": telefone
        })

        print(f'Telefone atualizado com sucesso!')
    except requests.exceptions.RequestException as erro:
        print(f'Erro na requisição: {erro}')
        return None

    except Exception as e:
        print(f'Erro: {e}')
        return None

#Função que atualiza a altura do perfil médico do paciente no banco de dados através do ID
def updateAlturaPacientePorId(id, altura):
    try:
        response_api = requests.put(f"{api_url}/paciente/altura", json={
            "id": id,
            "altura": altura
        })

        print(f'Altura atualizada com sucesso!')
    except requests.exceptions.RequestException as erro:
        print(f'Erro na requisição: {erro}')
        return None

    except Exception as e:
        print(f'Erro: {e}')
        return None

#Função que atualiza o peso do perfil médico do paciente no banco de dados através do ID
def updatePesoPacientePorId(id, peso):
    try:
        response_api = requests.put(f"{api_url}/paciente/peso", json={
            "id": id,
            "peso": peso
        })

        print(f'Peso atualizado com sucesso!')
    except requests.exceptions.RequestException as erro:
        print(f'Erro na requisição: {erro}')
        return None

    except Exception as e:
        print(f'Erro: {e}')
        return None

#Método que mostra o menu de minha conta
def menu_minha_conta(minha_conta):
    # O looping ocorrerá até ser manualmente interrompido
    while True:
        time.sleep(.25)
        print(f"\nMinha Conta:"
              f"\nEmail: {minha_conta["email"]};"
              f"\nSenha: {minha_conta["senha"]};"
              f"\n\n"
              f"1 - Editar email;"
              f"\n2 - Editar senha;"
              f"\n3 - Voltar")

        time.sleep(.25)

        opcao_meus_dados = int(input("\nInsira o número de sua escolha: "))
        time.sleep(.35)
        match opcao_meus_dados:
            case 1:
                novo_email = input("Insira o seu novo email: ")
                time.sleep(.5)

                # É necessário ter um @ no email, para ser considerado um
                if not "@" in novo_email:
                    print("\nNovo email é inválido")
                    continue

                updateEmailContaPacientePorId(minha_conta["id_conta_paciente"], novo_email)
                time.sleep(.6)
                break

            case 2:
                nova_senha = input("Insira a sua nova senha (Sem espaços, minímo 5 digitos): ")
                time.sleep(.5)

                # Se, houver espaços ou a senha tiver menos de 5 caracteres, ela é inválida
                if " " in nova_senha or len(nova_senha) < 5:
                    print(
                        "\nNova senha é inválida, verifique se você utilizou um espaço ou se ela tem no mínimo 5 digitos")
                    continue

                updateSenhaContaPacientePorId(minha_conta["id_conta_paciente"], nova_senha)
                time.sleep(.6)

                print("\nNova senha salva com sucesso!")

                break

            case 3:
                time.sleep(.45)
                print("\n\nVoltando.")
                break

            case _:
                time.sleep(.45)
                print("Escolha inválida")
                continue



#Função que atualiza o email da conta do paciente no banco de dados através do ID
def updateEmailContaPacientePorId(id, email):
    try:
        response_api = requests.put(f"{api_url}/conta_paciente/email", json={
            "id": id,
            "email": email
        })

        print(f'Email atualizado com sucesso!')
    except requests.exceptions.RequestException as erro:
        print(f'Erro na requisição: {erro}')
        return None

    except Exception as e:
        print(f'Erro: {e}')
        return None

#Função que atualiza a senha da conta do paciente no banco de dados através do ID
def updateSenhaContaPacientePorId(id, senha):
    try:
        response_api = requests.put(f"{api_url}/conta_paciente/senha", json={
            "id": id,
            "senha": senha
        })

        print(f'Senha atualizada com sucesso!')
    except requests.exceptions.RequestException as erro:
        print(f'Erro na requisição: {erro}')
        return None

    except Exception as e:
        print(f'Erro: {e}')
        return None

#Método que mostra o menu de meus dados
def menu_meus_dados(meus_dados):
    #O looping ocorrerá até ser manualmente interrompido
    while True:
        print(f"\nMeus Dados:"
              f"\nRG: {meus_dados["ds_rg"]};"
              f"\nCPF: {meus_dados["ds_cpf"]};"
              f"\nTelefone: {meus_dados["num_tel"]};"
              f"\nNome: {meus_dados["nm_paciente"]};"
              f"\nIdade: {meus_dados["num_idade"]};"
              f"\nSexo Biológico: {meus_dados["ds_sexo_paciente"]};"
              f"\nAltura (m): {meus_dados["num_altura"]}m;"
              f"\nPeso (kg): {meus_dados["num_peso"]}kg;"
              f"\n\n"
              f"1 - Editar Telefone;"
              f"\n2 - Editar Altura (m);"
              f"\n3 - Editar Peso (kg);"
              f"\n4 - Voltar;"
              f"\n5 - Exportar para JSON.")

        opcao_meus_dados = int(input("\nInsira o número de sua escolha: "))
        time.sleep(.65)

        match opcao_meus_dados:
            case 1:
                novo_telefone = input("\nInsira o seu novo número de telefone: ")
                novo_telefone = novo_telefone.replace("-", "")
                novo_telefone = novo_telefone.replace("(", "")
                novo_telefone = novo_telefone.replace(")", "")
                novo_telefone = novo_telefone.replace(" ", "")

                time.sleep(.5)
                if len(novo_telefone) == 0:
                    print("Telefone inválido.")
                    continue

                updateTelefonePacientePorId(meus_dados["id_paciente"], novo_telefone)
                time.sleep(.25)

                print("\nNovo telefone salvo!")
                break

            case 2:
                nova_altura = float(input("Insira a sua altura (m): "))

                time.sleep(.5)
                if nova_altura > 100:
                    nova_altura /= 100
                elif nova_altura < 10:
                    print("Altura inválida.")
                    continue

                updateAlturaPacientePorId(meus_dados["id_paciente"], nova_altura)
                time.sleep(.25)

                print("\nNova altura salva!")
                break

            case 3:
                novo_peso = float(input("Insira o seu peso (kg): "))

                time.sleep(.5)
                if novo_peso < 0:
                    print("Peso inválido.")
                    continue

                updatePesoPacientePorId(meus_dados["id_paciente"], novo_peso)

                time.sleep(.25)
                print("\nNovo peso salvo!")
                break

            case 4:
                print("\n\nVoltando.")
                time.sleep(.5)
                break

            case 5:
                try:
                    with open("meus_dados.json", "w", encoding="utf-8") as arquivo:
                        json.dump(meus_dados, arquivo, indent=4, ensure_ascii=False)
                    print("Dados exportados com sucesso para 'meus_dados.json'.")
                except Exception as e:
                    print(f"Erro ao exportar dados: {e}")
                break

            case _:
                print("Escolha inválida")
                time.sleep(.5)
                continue


#Função que retorna o convênio médico do paciente no banco de dados, procurado com o ID do mesmo
def selectConvenioMedicoPorIdPaciente(id_paciente):
    try:
        response_api = requests.get(f"{api_url}/convenio_medico/paciente/{id_paciente}")

        if not response_api.json():
            return None
        else:
            convenio_medico = {
                "id_convenio": response_api.json()["id"],
                "nm_operadora": response_api.json()["operadora"],
                "num_carteirinha": response_api.json()["numeroCarteirinha"],
                "dt_inicio": response_api.json()["dataInicio"],
                "dt_validade": response_api.json()["dataValidade"],
                "fk_id_paciente": response_api.json()["idPaciente"]
            }

            return convenio_medico

    except requests.exceptions.RequestException as erro:
        print(f'Erro na requisição: {erro}')
        return None

    except Exception as e:
        print(f'Erro: {e}')
        return None


#Método que mostra o menu de convênio médico
def menu_convenio_medico(id_paciente):
    while True:
        convenio_medico = selectConvenioMedicoPorIdPaciente(id_paciente)

        emissao_formatada = convenio_medico["dt_inicio"]  # pega só dia/mês/ano
        validade_formatada = convenio_medico["dt_validade"]  # pega só dia/mês/ano

        time.sleep(.35)
        print(f"\nInformações do meu Convênio Médico:"
              f"\nOperadora: {convenio_medico["nm_operadora"]};"
              f"\nNúmero da Carteirinha: {convenio_medico["num_carteirinha"]};"
              f"\nEmissão: {emissao_formatada};"
              f"\nValidade: {validade_formatada};"
              f"\n"
              f"\n1 - Exportar dados para JSON;"
              f"\n0 - Voltar")

        time.sleep(.25)
        try:
            opcao_meus_dados = int(input("\nInsira o número de sua escolha: "))
            time.sleep(.3)
            match opcao_meus_dados:
                case 1:
                    try:
                        with open("convenio_medico.json", "w", encoding="utf-8") as arquivo:
                            json.dump(convenio_medico, arquivo, indent=4, ensure_ascii=False)
                        print("Dados exportados com sucesso para 'convenio_medico.json'.")
                    except Exception as e:
                        print(f"Erro ao exportar dados: {e}")
                    break

                case 0:
                    print("\nVoltando.")
                    time.sleep(.5)
                    break

                case _:
                    print("\nEscolha inválida!")
                    time.sleep(.5)
                    continue

        except ValueError:
            time.sleep(.5)
            print("Insira um número, por favor.")


#Função que cadastra um novo relatório médico no banco de dados
def criarRelatorio(relatorio, id_paciente, id_medico):
    try:
        response_api = requests.post(f"{api_url}/relatorio_medico", json={
            "descricaoRelatorio": relatorio["ds_relatorio"],
            "paciente": {
                "id": id_paciente
            },
            "dataRelatorio": relatorio["dt_relatorio"],
            "medicoRelator": {
                "id": id_medico
            }
        })

        id_relatorio = response_api.text

        print(f'Relatório emitido com sucesso!')

        return id_relatorio

    except requests.exceptions.RequestException as erro:
        print(f'Erro na requisição: {erro}')
        return None

    except Exception as e:
        print(f'Erro: {e}')
        return None

#Função que deleta um relatório médico do banco de dados através do ID
def deleteRelatorioPorId(id):
    try:
        response_api = requests.delete(f"{api_url}/relatorio_medico/{id}")

        if response_api.status_code == 200:
            print(f'O relatório médico foi excluído com sucesso!')
        else:
            print(f'Nenhum relatório médico com id: {id} foi encontrado!')

    except requests.exceptions.RequestException as erro:
        print(f'Erro na requisição: {erro}')
        return None

    except Exception as e:
        print(f'Erro: {e}')
        return None

#Função que retorna todos os relatórios médicos no banco de dados que têm o ID do paciente
def selectRelatoriosPorIdPaciente(id_paciente):
    lista_relatorios = []

    try:
        response_api = requests.get(f"{api_url}/relatorio_medico/paciente/{id_paciente}")

        for relatorio in response_api.json():
            novo_relatorio = {
                "id_relatorio_medico": relatorio["id"],
                "dt_relatorio": relatorio["dataRelatorio"],
                "ds_relatorio": relatorio["descricaoRelatorio"],
                "fk_id_medico": relatorio["medicoRelator"]["id"],
                "fk_id_paciente": relatorio["paciente"]["id"]
            }
            lista_relatorios.append(novo_relatorio)

    except requests.exceptions.RequestException as erro:
        print(f'Erro na requisição: {erro}')

    except Exception as e:
        print(f'Erro: {e}')

    return lista_relatorios


#Método que mostra o menu de relatórios médicos
def menu_relatorios_medicos(id_paciente):
    print("===================================")
    #Ficará rodando até ser quebrado manualmente com um break
    while True:
        lista_relatorios = selectRelatoriosPorIdPaciente(id_paciente)

        print("\nMenu de Relatórios Médicos:"
              "\n1 - Listar relatórios;"
              "\n2 - Emitir novo relatório;"
              "\n3 - Deletar relatório;"
              "\n4 - Voltar."
              "\n5 - Exportar todos os Relatórios para JSON."
              "\n")

        time.sleep(.25)
        opcao_relatorio = int(input("Insira o número de sua escolha: "))
        time.sleep(.35)

        match opcao_relatorio:
            case 1:
                print("\nLista de Relatórios Médicos:\n")
                time.sleep(.35)
                #Itera sobre cada agendamento na lista de agendamentos e os mostra de forma organizada utilizando o get()
                for relatorio in lista_relatorios:
                    medico = selectMedicoPorId(relatorio['fk_id_medico'])

                    data_obj = datetime.strptime(relatorio["dt_relatorio"], "%Y-%m-%d")
                    data_formatada = data_obj.strftime("%d/%m/%Y") # pega só dia/mês/ano
                    time.sleep(.35)
                    print(f"--------------------------"
                          f"\nMédico Relator: {medico['nm_medico']};"
                          f"\nData de Emissão: {data_formatada};"
                          f"\nRelatório: {relatorio["ds_relatorio"]}")
                print("--------------------------")
                time.sleep(.5)
            case 2:
                informacoes_corretas = False

                data = ""
                medico_responsavel = ""
                relatorio = ""

                #Looping que ocorrerá até todas as informações serem válidas
                while not informacoes_corretas:
                    print(f"\nNovo Relatório Médico:\n")
                    time.sleep(.35)
                    data_str = input("Por favor, insira a data de emissão do relatório (DD/MM/AAAA): ")
                    time.sleep(.3)
                    relatorio = input("Insira o conteúdo do relatório:\n ")
                    time.sleep(.3)

                    #Escolhe um médico aleatório, visto que teria acesso a todos os possíveis na situação real
                    lista_medicos = selectMedicos()
                    if not lista_medicos:
                        print("Nenhum médico disponível no momento.")
                        return

                    print("\n=== Lista de Médicos Disponíveis ===")
                    id_medico = 1
                    for medico in lista_medicos:
                        print(f"{id_medico}. {medico['nm_medico']} — Setor: {medico['ds_setor_medico']}")
                        id_medico += 1

                    while True:
                        try:
                            escolha_medico = int(input("\nEscolha o número do médico relator: "))
                            if 1 <= escolha_medico <= len(lista_medicos):
                                medico = lista_medicos[escolha_medico - 1]
                                break
                            else:
                                print("Opção inválida! Escolha um número válido.")
                        except ValueError:
                            print("Entrada inválida! Digite apenas o número da opção.")

                    novo_relatorio = {}

                    try:
                        data_relatorio = datetime.strptime(data_str, "%d/%m/%Y")
                        data_relatorio = data_relatorio.strftime("%Y-%m-%d")
                        # Dictionary do novo agendamento
                        novo_relatorio = {
                            "dt_relatorio": data_relatorio,
                            "ds_relatorio": relatorio,
                        }


                        criarRelatorio(novo_relatorio, id_paciente, medico["id_medico"])

                    except ValueError as e:
                        time.sleep(.5)
                        print(e)
                        print("Formato inválido! Use DD/MM/AAAA para a data e HH:MM para o horário.")


                    informacoes_corretas = True


            case 3:
                print("\nRemover Relatório Médico:\n")
                time.sleep(.3)
                #Até um relatório ser escolhido para ser deletado, o looping se manterá
                relatorio_escolhido = False
                while not relatorio_escolhido:
                    #Se a lista de relatórios médicos tiver tamanho 0, não dá pra deletar nenhum relatório
                    time.sleep(.5)
                    if len(lista_relatorios) == 0:
                        print("Você não possui nenhum relatório médico!")
                    else:
                        #O id serve para o usuário escolher o relatório a ser deletado, começa do 1 apesar das listas
                            #começarem do 0, porque faz mais sentido aos pacientes
                        id_relatorio = 1
                        #Itera sobre cada relatório na lista de relatórios, e mostra cada um com um id, sua data de emissão, o médico relator e o conteúdo
                        for relatorio in lista_relatorios:
                            medico = selectMedicoPorId(relatorio['fk_id_medico'])
                            data_obj = datetime.strptime(relatorio["dt_relatorio"], "%Y-%m-%d")
                            data_formatada = data_obj.strftime("%d/%m/%Y")  # pega só dia/mês/ano
                            time.sleep(.35)
                            print(f"--------------------------"
                                  f"\n{id_relatorio} - {data_formatada}"
                                  f"\nConteúdo: {relatorio["ds_relatorio"]}"
                                  f"\nMédico Relator: {medico["nm_medico"]}")
                            #Próximo relatório terá um id diferente, nesse caso, superior
                            id_relatorio += 1

                    print("--------------------------\n\n"
                          "0 - Voltar")

                    time.sleep(.5)


                    try:
                        selecao_deletar_relatorio = int(input("\nInsira o número identificador do relatório que deseja remover: "))
                        time.sleep(.35)

                        #Se for 0, o paciente não quer deletar nenhum, então voltar e quebrar o looping.
                        if selecao_deletar_relatorio == 0:
                            relatorio_escolhido = True
                            continue

                        #Se o seletor for menor que 0, ou maior que o tamanho da lista de relatórios, ele é inválido
                        elif selecao_deletar_relatorio < 0 or selecao_deletar_relatorio > len(lista_relatorios):
                            print("Identificador inválido, tente novamente.")
                            time.sleep(.5)
                            continue

                        #Se tudo estiver correto, dar delete no indíce selecionado (subtraindo 1, porque a lista começa do 0)
                        else:
                            id_relatorio_selecionado = lista_relatorios[selecao_deletar_relatorio - 1]["id_relatorio_medico"]
                            deleteRelatorioPorId(id_relatorio_selecionado)
                            #Quebrar o looping após o apagamento
                            relatorio_escolhido = True

                    except ValueError:
                        time.sleep(.35)
                        print("Insira um número válido, por favor.")
                        time.sleep(.5)
                        continue

            case 4:
                print("\nVoltando...")
                time.sleep(.5)
                break

            case 5:
                try:
                    with open("relatorios_medicos.json", "w", encoding="utf-8") as arquivo:
                        json.dump(lista_relatorios, arquivo, indent=4, ensure_ascii=False)
                    print("Dados exportados com sucesso para 'relatorios_medicos.json'!")
                except Exception as e:
                    print(f"Erro ao exportar dados: {e}")
                break

            case _:
                print("\nOpção inválida!")
                time.sleep(.5)
                continue



#Função que retorna um médico do banco de dados, procurado pelo ID
def selectMedicoPorId(id):
    try:
        response_api = requests.get(f"{api_url}/medico/{id}")

        if not response_api.json():
            return None
        else:
            medico = {
                "id_medico": response_api.json()["id"],
                "nm_medico": response_api.json()["nomeMedico"],
                "ds_sexo_medico": response_api.json()["sexo"],
                "ds_setor_medico": response_api.json()["setorMedico"],
                "num_carga_horaria": response_api.json()["cargaHoraria"],
                "vl_hora": response_api.json()["valorHora"],
                "fk_id_instituicao": response_api.json()["empregador"]["id"]
            }

            return medico

    except requests.exceptions.RequestException as erro:
        print(f'Erro na requisição: {erro}')
        return None

    except Exception as e:
        print(f'Erro: {e}')
        return None

#Função que retorna todos os médicos cadastrados no banco de dados
def selectMedicos():
    lista_medicos = []

    try:
        response_api = requests.get(f"{api_url}/medico")

        for medico in response_api.json():
            novo_medico = {
                "id_medico": medico["id"],
                "nm_medico": medico["nomeMedico"],
                "ds_sexo_medico": medico["sexo"],
                "ds_setor_medico": medico["setorMedico"],
                "num_carga_horaria": medico["cargaHoraria"],
                "vl_hora": medico["valorHora"],
                "fk_id_instituicao": medico["empregador"]["id"]
            }
            lista_medicos.append(novo_medico)

    except requests.exceptions.RequestException as erro:
        print(f'Erro na requisição: {erro}')

    except Exception as e:
        print(f'Erro: {e}')

    return lista_medicos

#Método que mostra o menu de médicos responsáveis
def menu_medicos_responsaveis():
    while True:
        lista_medicos = selectMedicos()

        print("Lista de Médicos que se responsabilizaram ou podem se responsabilizar por você:")

        for medico in lista_medicos:
            instituicao = selectInstituicaoPorId(medico['fk_id_instituicao'])

            time.sleep(.35)
            print(f"--------------------------"
                  f"\nNome: {medico['nm_medico']};"
                  f"\nSexo: {medico['ds_sexo_medico']};"
                  f"\nSetor: {medico["ds_setor_medico"]};"
                  f"\nInstituição Empregadora: {instituicao['nm_razao_social']};")
        print("--------------------------")

        print("\n0 - Voltar")
        time.sleep(.45)

        try:
            opcao_medicos_responsaveis = int(input("\nInsira o número de sua escolha: "))

            time.sleep(.45)
            match opcao_medicos_responsaveis:
                case 0:
                    print("\nVoltando...")
                    time.sleep(.5)
                    break

                case _:
                    print("\nOpção inválida!")
                    time.sleep(.5)
                    continue

        except ValueError:
            time.sleep(.35)
            print("Insira um número válido, por favor.")
            time.sleep(.5)
            continue



#Função que retorna uma instituição do banco de dados, procurada pelo ID
def selectInstituicaoPorId(id):
    try:
        response_api = requests.get(f"{api_url}/instituicao/{id}")

        if not response_api.json():
            return None
        else:
            instituicao = {
                "id_instituicao": response_api.json()["id"],
                "nm_razao_social": response_api.json()["razaoSocial"],
                "nm_fantasia": response_api.json()["nomeFantasia"],
                "ds_setor": response_api.json()["setor"],
                "num_cnpj": response_api.json()["cnpj"],
                "ds_endereco": response_api.json()["sede"]
                #"ds_endereco": f"{response_api.json()["logradouro"]} {response_api.json()["numero"]} — {response_api.json()["bairro"]}, {response_api.json()["cidade"]} - {response_api.json()["cep"]}"
            }

            return instituicao

    except requests.exceptions.RequestException as erro:
        print(f'Erro na requisição: {erro}')
        return None

    except Exception as e:
        print(f'Erro: {e}')
        return None


#Função que retorna todas as instituições do banco de dados
def selectInstituicao():
    lista_instituicoes = []

    try:
        response_api = requests.get(f"{api_url}/instituicao")

        for instituicao in response_api.json():
            nova_instituicao = {
                "id_instituicao": instituicao["id"],
                "nm_razao_social": instituicao["razaoSocial"],
                "nm_fantasia": instituicao["nomeFantasia"],
                "ds_setor": instituicao["setor"],
                "num_cnpj": instituicao["cnpj"],
                "ds_endereco": instituicao["sede"]
            }
            lista_instituicoes.append(nova_instituicao)

    except requests.exceptions.RequestException as erro:
        print(f'Erro na requisição: {erro}')

    except Exception as e:
        print(f'Erro: {e}')

    return lista_instituicoes

#Método que mostra o menu de instituições médicas
def menu_instituicoes_medicas():
    while True:
        lista_instituicoes = selectInstituicao()

        print("\nLista de Instituições hospitalares:\n")
        time.sleep(.35)
        for instituicao in lista_instituicoes:
            time.sleep(.35)
            print(
                "--------------------------"
                f"\nRazão Social: {instituicao['nm_razao_social']}"
                f"\nNome Fantasia: {instituicao['nm_fantasia']}"
                f"\nSetor: {instituicao['ds_setor']}"
                f"\nCNPJ: {instituicao['num_cnpj']}"
                f"\nEndereço: {instituicao['ds_endereco']['logradouro']}, "
                f"{instituicao['ds_endereco']['numero']} - "
                f"{instituicao['ds_endereco']['bairro']}, "
                f"{instituicao['ds_endereco']['cidade']} "
                f"({instituicao['ds_endereco']['cep']})"
            )

        print("--------------------------")

        print("\n0 - Voltar")

        time.sleep(.45)
        try:
            opcao_instituicoes = int(input("\nInsira o número de sua escolha: "))
            time.sleep(.45)

            match opcao_instituicoes:
                case 0:
                    print("\nVoltando...")
                    time.sleep(.5)
                    break

                case _:
                    print("\nOpção inválida!")
                    time.sleep(.5)
                    continue

        except ValueError:
            time.sleep(.45)
            print("Insira um número válido, por favor.")
            time.sleep(.5)
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

        time.sleep(.35)

        voltar_para_menu = input("\nVoltar para o menu? (Sim/Não): ")
        time.sleep(.45)

        if checarInputSim(voltar_para_menu):
            print("\nVoltando.")
            time.sleep(.5)
            break
        else:
            #Se o paciente não quiser voltar para o menu principal, ele verá o menu de ajuda novamente
            time.sleep(.5)
            continue



#Método que mostra a lista de opções do menu e retorna um input para escolha
def menu_paciente_escolha():
    print("\n\nMenu do Paciente:"
          "\n1 - Dados da minha Conta;"
          "\n2 - Meus Dados;"
          "\n3 - Agendamentos;"
          "\n4 - Convênio Médico;"
          "\n5 - Relatórios Médicos;"
          "\n6 - Médicos Responsáveis;"
          "\n7 - Instituições Médicas;"
          "\n8 - Ajuda;"
          "\n9 - Desconectar."
          "\n\n")

    time.sleep(.5)

    return int(input("Insira o número de sua escolha: "))



#Método PRINCIPAL
def main():
    print("Seja bem-vindo(a) ao painel de pacientes da HC!")
    time.sleep(0.35)
    print("Esperamos que tenha uma ótima experiência.")
    time.sleep(0.3)

    print("\n Antes de efetuarmos o seu acesso, responda:\n")
    time.sleep(.5)

    conta_paciente, info_paciente = loginERegistro()
    time.sleep(.5)

    # Loop será infinito até o usuário voluntariamente sair
    while True:
        conta_paciente = selectContaPacientePorId(conta_paciente["id_conta_paciente"])
        info_paciente = selectPacientePorId(info_paciente["id_paciente"])

        time.sleep(.5)
        '''Usa o input retornado do método que demonstra o menu de escolhas do paciente e guarda numa variável, é relativamente
        grande, logo coloquei num método a parte para não poluir o flow principal'''
        opcao_menu = menu_paciente_escolha()
        time.sleep(.25)

        '''
        Menu do Paciente:
          1 - Dados da minha Conta;
          2 - Meus Dados;
          3 - Agendamentos;
          4 - Convênio Médico;
          5 - Relatórios Médicos;
          6 - Médicos Responsáveis;
          7 - Instituições Médicas;
          8 - Ajuda;
          9 - Desconectar.
        '''

        match opcao_menu:
            case 1:
                menu_minha_conta(conta_paciente)

            case 2:
                menu_meus_dados(info_paciente)

            case 3:
                menu_agendamentos(info_paciente["id_paciente"])

            case 4:
                menu_convenio_medico(info_paciente["id_paciente"])

            case 5:
                menu_relatorios_medicos(info_paciente["id_paciente"])

            case 6:
                menu_medicos_responsaveis()

            case 7:
                menu_instituicoes_medicas()

            case 8:
                menu_ajuda()

            case 9:
                print("Muito obrigado por utilizar o sistema de pacientes da HC, desenvolvido por estudantes da FIAP!")
                time.sleep(.5)
                print("Saindo...")
                time.sleep(.65)
                break

            case _:
                print("Opção inválida!")
                time.sleep(.5)
                continue

main()