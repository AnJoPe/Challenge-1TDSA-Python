import oracledb
import random
import time
from datetime import datetime, timedelta

#Método SUPER IMPORTANTE que gera uma nova conexão ao Banco de Dados
def getConexao():
    try:
        conexao = oracledb.connect(
            user="rm562682",
            password="270906",
            host="oracle.fiap.com.br",
            port="1521",
            service_name="orcl"
        )

    except Exception as e:
        print(f'Encontramos um problema ao acessar o banco de dados, tente novamente mais tarde!: {e}')

    return conexao

#Método que cria as tabelas do banco de dados se ainda não existem
def criarTabelasBancoDados(conexao):
    cursor = conexao.cursor()

    try:
        codigo_sql = """
            create table Instituicao(
            id_instituicao int primary key not null,
            nm_razao_social varchar2(150) unique not null,
            nm_fantasia varchar2(100) not null,
            ds_setor varchar(100) not null,
            num_cnpj varchar(20) unique not null,
            ds_endereco varchar2(250) not null
        );
         
        create table Medico(
            id_medico int primary key not null,
            nm_medico varchar2(150) unique not null,
            ds_sexo_medico varchar2(10) not null,
            ds_setor_medico varchar(100) not null,
            num_carga_horaria int not null check (num_carga_horaria > 10 and num_carga_horaria <  50),
            vl_hora float not null check (vl_hora > 0),
            fk_id_instituicao int,
            FOREIGN KEY (fk_id_instituicao) REFERENCES Instituicao(id_instituicao)
        );
         
        create table Paciente(
            id_paciente int primary key,
            num_tel varchar2(25) not null,
            ds_endereco varchar2(300) not null,
            nm_paciente varchar2(250) not null,
            num_idade int not null,
            ds_sexo_paciente varchar2(10) not null,
            num_altura float not null,
            num_peso float not null,
            ds_rg varchar2(15) unique not null,
            ds_cpf varchar2(14) unique not null
        );
         
        create table Agendamento(
            id_agendamento int primary key,
            dt_consulta date not null,
            hr_consulta varchar(5) not null,
            fk_id_medico int,
            FOREIGN KEY (fk_id_medico) REFERENCES Medico(id_medico),
            fk_id_instituicao int,
            FOREIGN KEY (fk_id_instituicao) REFERENCES Instituicao(id_instituicao),
            fk_id_paciente int,
            FOREIGN KEY (fk_id_paciente) REFERENCES Paciente(id_paciente)
        );
         
        create table Relatorio_Medico(
            id_relatorio_medico int primary key,
            dt_relatorio date not null,
            ds_relatorio varchar2(500) not null,
            fk_id_medico int,
            FOREIGN KEY (fk_id_medico) REFERENCES Medico(id_medico),
            fk_id_paciente int,
            FOREIGN KEY (fk_id_paciente) REFERENCES Paciente(id_paciente)
        );
         
        create table Convenio(
            id_convenio int primary key,
         
            nm_operadora varchar2(250) unique not null,
            num_carteirinha varchar(40) not null,
            dt_inicio date not null,
            dt_validade date not null,
            fk_id_paciente int,
            FOREIGN KEY (fk_id_paciente) REFERENCES Paciente(id_paciente)
        );
        
        create table Conta_Paciente(
            id_conta_paciente int primary key,
            ds_email varchar(50) unique not null,
            ds_senha varchar(15) not null,
            fk_id_paciente int,
            FOREIGN KEY (fk_id_paciente) REFERENCES Paciente(id_paciente),
            fk_id_convenio int,
            FOREIGN KEY (fk_id_convenio) REFERENCES Convenio(id_convenio)
        );
        """

        cursor.execute(codigo_sql)
        print("Todas as tabelas foram criadas com sucesso!")

    except oracledb.Error as error:
        #ORA-00955 é um erro que indica que a tabela já existe, logo não precisa nem avisar
            #Só fale que deu um erro na criação quando o erro for algum outro
        if not "ORA-00955" in str(error):
            print(f'Erro na criação das tabelas: {error}')

    finally:
        if conexao:
            conexao.close()

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
    def gerarNovoIdConvenio():
        conexao_id = getConexao()

        if not conexao_id:
            return False

        try:
            cursor_id = conexao_id.cursor()
            sql_id = """select MAX(id_convenio) from Convenio"""
            cursor_id.execute(sql_id)

            maior_id = cursor_id.fetchone()

            return (maior_id[0] or 0) + 1

        except oracledb.Error as e:
            print(f'\nErro ao conectar ao Banco de Dados: {e}')
        finally:
            if conexao_id:
                conexao_id.close()

    conexao = getConexao()

    if not conexao:
        return

    try:
        cursor = conexao.cursor()
        sql = """
                INSERT INTO Convenio (id_convenio, nm_operadora, num_carteirinha, dt_inicio, dt_validade, fk_id_paciente)
                VALUES (:id_convenio, :nm_operadora, :num_carteirinha, :dt_inicio, :dt_validade, :fk_id_paciente)
            """

        # Data de agora
        data_agora = datetime.now()

        # "Formato SQL" = só a data (ano-mes-dia)
        data_formatada_sql = data_agora.date()

        # Data em 3 anos (365 dias * 3)
        data_em_tres_anos = data_agora + timedelta(days=3 * 365)

        data_em_tres_anos_formatada_sql = data_em_tres_anos.date()

        id_convenio = gerarNovoIdConvenio()

        cursor.execute(sql, {
            'id_convenio': id_convenio,
            'nm_operadora': convenio["operadora"],
            'num_carteirinha': convenio["codigo"],
            'dt_inicio': data_formatada_sql,
            'dt_validade': data_em_tres_anos_formatada_sql,
            'fk_id_paciente': id_paciente
        })
        conexao.commit()
        print(f'Convênio cadastrado com sucesso!')

        return id_convenio

    except oracledb.Error as e:
        print(f'\nErro ao cadastrar o convênio: {e}')
        conexao.rollback()
    finally:
        if conexao:
            conexao.close()

#Função que cadastra o perfil médico do paciente no banco de dados
def criarPerfilPaciente(perfil_paciente):
    def gerarNovoIdPaciente():
        conexao_id = getConexao()

        if not conexao_id:
            return False

        try:
            cursor_id = conexao_id.cursor()
            sql_id = """select MAX(id_paciente) from Paciente"""
            cursor_id.execute(sql_id)

            maior_id = cursor_id.fetchone()

            return (maior_id[0] or 0) + 1

        except oracledb.Error as e:
            print(f'\nErro ao conectar ao Banco de Dados: {e}')
        finally:
            if conexao_id:
                conexao_id.close()

    conexao = getConexao()

    if not conexao:
        return

    try:
        cursor = conexao.cursor()
        sql = """
                INSERT INTO Paciente (id_paciente, num_tel, ds_endereco, nm_paciente, num_idade, ds_sexo_paciente, num_altura, num_peso, ds_rg, ds_cpf)
                VALUES (:id_paciente, :num_tel, :ds_endereco, :nm_paciente, :num_idade, :ds_sexo_paciente, :num_altura, :num_peso, :ds_rg, :ds_cpf)
            """

        stringEndereco = f"{perfil_paciente["endereco"]["logradouro"]} {perfil_paciente["endereco"]["numero"]} - {perfil_paciente["endereco"]["bairro"]}, {perfil_paciente["endereco"]["cidade"]} - {perfil_paciente["endereco"]["cep"]}"

        id_paciente = gerarNovoIdPaciente()

        cursor.execute(sql, {
            'id_paciente': id_paciente,
            'num_tel': perfil_paciente["telefone"],
            'ds_endereco': stringEndereco,
            'nm_paciente': perfil_paciente["nome_completo"],
            'num_idade': perfil_paciente["idade"],
            'ds_sexo_paciente': perfil_paciente["sexo"],
            'num_altura': perfil_paciente["altura"],
            'num_peso': perfil_paciente["peso"],
            'ds_rg': perfil_paciente["rg"],
            'ds_cpf': perfil_paciente["cpf"]
        })
        conexao.commit()
        print(f'Paciente cadastrado com sucesso!')

        perfil_paciente["id_paciente"] = id_paciente

        return perfil_paciente

    except oracledb.Error as e:
        print(f'\nErro ao cadastrar o paciente: {e}')
        conexao.rollback()
    finally:
        if conexao:
            conexao.close()

#Função que cadastra a conta do paciente no banco de dados
def criarContaPaciente(dadosPaciente):
    def gerarNovoIdContaPaciente():
        conexao_id = getConexao()

        if not conexao_id:
            return False

        try:
            cursor_id = conexao_id.cursor()
            sql_id = """select MAX(id_conta_paciente) from Conta_Paciente"""
            cursor_id.execute(sql_id)

            maior_id = cursor_id.fetchone()

            return (maior_id[0] or 0) + 1

        except oracledb.Error as e:
            print(f'\nErro ao conectar ao Banco de Dados: {e}')
        finally:
            if conexao_id:
                conexao_id.close()

    conexao = getConexao()

    if not conexao:
        return

    try:
        cursor = conexao.cursor()
        sql = """
                INSERT INTO Conta_Paciente (id_conta_paciente, ds_email, ds_senha, fk_id_paciente, fk_id_convenio)
                VALUES (:id_conta_paciente, :ds_email, :ds_senha, :fk_id_paciente, :fk_id_convenio)
            """

        id_conta = gerarNovoIdContaPaciente()

        cursor.execute(sql, {
            'id_conta_paciente': id_conta,
            'ds_email': dadosPaciente["email"],
            'ds_senha': dadosPaciente["senha"],
            'fk_id_paciente': dadosPaciente["id_paciente"],
            'fk_id_convenio': dadosPaciente["id_convenio"],
        })
        conexao.commit()
        print(f'Conta cadastrada com sucesso!')

        dadosPaciente["id_conta_paciente"] = id_conta

        return dadosPaciente

    except oracledb.Error as e:
        print(f'\nErro ao cadastrar a conta: {e}')
        conexao.rollback()
    finally:
        if conexao:
            conexao.close()

#Função que retorna a conta do paciente no banco de dados procurada pelo email
def selectContaPacientePorEmail(email):
    conexao = getConexao()
    if not conexao:
        return

    try:
        cursor = conexao.cursor()
        codigo_sql = """
            SELECT * from Conta_Paciente where ds_email = :email
        """
        cursor.execute(codigo_sql, {
            'email': email
        })

        registros = cursor.fetchall()
        if not registros or len(registros) == 0:
            return None
        else:
            conta = {
                "id_conta_paciente": registros[0][0],
                "email": registros[0][1],
                "senha": registros[0][2],
                "fk_id_paciente": registros[0][3],
                "fk_id_convenio": registros[0][4]
            }

            return conta

    except oracledb.Error as error:
        print(f"Falha no acesso ao Banco de Dados: {error}")

    finally:
        if conexao:
            conexao.close()

#Função que retorna a conta do paciente no banco de dados procurada pelo ID
def selectContaPacientePorId(id):
    conexao = getConexao()
    if not conexao:
        return

    try:
        cursor = conexao.cursor()
        codigo_sql = """
            SELECT * from Conta_Paciente where id_conta_paciente = :id
        """
        cursor.execute(codigo_sql, {
            'id': id
        })

        registros = cursor.fetchall()
        if not registros or len(registros) == 0:
            return None
        else:
            conta = {
                "id_conta_paciente": registros[0][0],
                "email": registros[0][1],
                "senha": registros[0][2],
                "fk_id_paciente": registros[0][3],
                "fk_id_convenio": registros[0][4]
            }

            return conta

    except oracledb.Error as error:
        print(f"Falha no acesso ao Banco de Dados: {error}")

    finally:
        if conexao:
            conexao.close()

#Função que retorna o id do perfil médico do paciente no banco de dados, procurado pelo RG
def selectIdPerfilPacientePorRg(rg):
    conexao = getConexao()
    if not conexao:
        return

    try:
        cursor = conexao.cursor()
        codigo_sql = """
                SELECT id_paciente from Paciente where ds_rg = :rg
            """
        cursor.execute(codigo_sql, {
            'rg': rg
        })

        registros = cursor.fetchall()
        if not registros or len(registros) == 0:
            return None
        else:

            return registros[0][0]

    except oracledb.Error as error:
        print(f"Falha no acesso ao Banco de Dados: {error}")

    finally:
        if conexao:
            conexao.close()

#Função que retorna a conta do paciente no banco de dados procurada pelo ID
def selectPacientePorId(id):
    conexao = getConexao()
    if not conexao:
        return

    try:
        cursor = conexao.cursor()
        codigo_sql = """
                    SELECT * from Paciente where id_paciente = :id
                """
        cursor.execute(codigo_sql, {
            'id': id
        })

        registros = cursor.fetchall()
        if not registros or len(registros) == 0:
            return None
        else:
            linha_atual = registros[0]
            paciente = {
                'id_paciente': linha_atual[0],
                'num_tel': linha_atual[1],
                'ds_endereco': linha_atual[2],
                'nm_paciente': linha_atual[3],
                'num_idade': linha_atual[4],
                'ds_sexo_paciente': linha_atual[5],
                'num_altura': linha_atual[6],
                'num_peso': linha_atual[7],
                'ds_rg': linha_atual[8],
                'ds_cpf': linha_atual[9]
            }
            return paciente

    except oracledb.Error as error:
        print(f"Falha no acesso ao Banco de Dados: {error}")

    finally:
        if conexao:
            conexao.close()

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
                if not "@" in email_registro or " " in email_registro:
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

                if not "@" in email_login or " " in email_login:
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
    conexao = getConexao()
    if not conexao:
        return

    lista_agendamentos = []

    try:
        cursor = conexao.cursor()
        codigo_sql = """
                    SELECT * from Agendamento where fk_id_paciente = :id
                """
        cursor.execute(codigo_sql, {
            'id': id_paciente
        })

        registros = cursor.fetchall()
        if not registros or len(registros) == 0:
            return []
        else:
            for agendamento in registros:
                novo_agendamento = {
                    "id_agendamento": agendamento[0],
                    "dt_consulta": agendamento[1],
                    "hr_consulta": agendamento[2],
                    "fk_id_medico": agendamento[3],
                    "fk_id_instituicao": agendamento[4],
                    "fk_id_paciente": agendamento[5]
                }
                lista_agendamentos.append(novo_agendamento)

            return lista_agendamentos

    except oracledb.Error as error:
        print(f"Falha no acesso ao Banco de Dados: {error}")

    finally:
        if conexao:
            conexao.close()

#Função que cadastra um novo agendamento no banco de dados
def criarAgendamento(agendamento, id_paciente, id_medico, id_instituicao):
    def gerarNovoIdAgendamento():
        conexao_id = getConexao()

        if not conexao_id:
            return False

        try:
            cursor_id = conexao_id.cursor()
            sql_id = """select MAX(id_agendamento) from Agendamento"""
            cursor_id.execute(sql_id)

            maior_id = cursor_id.fetchone()

            return (maior_id[0] or 0) + 1

        except oracledb.Error as e:
            print(f'\nErro ao conectar ao Banco de Dados: {e}')
        finally:
            if conexao_id:
                conexao_id.close()

    conexao = getConexao()

    if not conexao:
        return

    try:
        cursor = conexao.cursor()
        sql = """
                INSERT INTO Agendamento (id_agendamento, dt_consulta, hr_consulta, fk_id_medico, fk_id_instituicao, fk_id_paciente)
                VALUES (:id_agendamento, :dt_consulta, :hr_consulta, :fk_id_medico, :fk_id_instituicao, :fk_id_paciente)
            """

        id_agendamento = gerarNovoIdAgendamento()

        cursor.execute(sql, {
            'id_agendamento': id_agendamento,
            'dt_consulta': agendamento["dt_consulta"],
            'hr_consulta': agendamento["hr_consulta"],
            'fk_id_medico': id_medico,
            'fk_id_instituicao': id_instituicao,
            'fk_id_paciente': id_paciente
        })
        conexao.commit()
        print(f'Agendamento cadastrado com sucesso!')

        return id_agendamento

    except oracledb.Error as e:
        print(f'\nErro ao cadastrar o convênio: {e}')
        conexao.rollback()
    finally:
        if conexao:
            conexao.close()

#Função que deleta um agendamento do banco de dados
def deleteAgendamentoPorId(id):
    conexao = getConexao()

    if not conexao:
        return

    try:
        cursor = conexao.cursor()

        sql = "DELETE FROM Agendamento WHERE id_agendamento = :id"

        cursor.execute(sql, {'id': id})
        conexao.commit()

        if cursor.rowcount > 0:
            print(f'O Agendamento foi excluído com sucesso!')
        else:
            print(f'Nenhum Agendamento com id: {id} foi encontrado!')
    except oracledb.Error as e:
        print(f'\n Erro ao excluir Agendamento: {e}')
        conexao.rollback()
    finally:
        if conexao:
            conexao.close()

        #Método que mostra a lista de opções do menu de agendamentos

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
              "\n4 - Voltar"
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

                    data_formatada = agendamento["dt_consulta"].strftime("%d/%m/%Y")  # pega só dia/mês/ano
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

                #Looping que ocorrerá até todas as informações serem válidas
                while not informacoes_corretas:
                    print(f"\nNovo agendamento:\n")
                    time.sleep(.3)
                    data_str = input("Por favor, insira a data do agendamento (DD/MM/AAAA): ")
                    time.sleep(.35)
                    horario_str = input("Agora insira o horário no qual o agendamento ocorrerá (HH:MM): ")
                    time.sleep(.5)

                    #Escolhe um médico aleatório, visto que teria acesso a todos os possíveis na situação real
                    lista_medicos = selectMedicos()
                    medico = random.choice(lista_medicos)

                    #Escolhe uma instituição aleatória, visto que teria acesso a todas as possíveis na situação real
                    lista_locais = selectInstituicao()
                    local = random.choice(lista_locais)

                    novo_agendamento = {}

                    try:
                        data_agendamento = datetime.strptime(data_str, "%d/%m/%Y")
                        hora, minuto = map(int, horario_str.split(":"))

                        data_hoje = datetime.now()

                        '''
                            - Não tem como agendar num ano que já passou
                            - A hora não pode ser negativa e nem passar de um dia
                            - Os minutos não podem ser negativos e nem passarem de uma hora
                        '''

                        # Ano no passado
                        if data_agendamento.year < data_hoje.year:
                            print("O ano não pode ser menor que o atual!")
                            time.sleep(.35)
                            continue

                        # Horas
                        if hora < 0 or hora > 23:
                            print("Hora inválida, precisa estar entre 0 e 23.")
                            time.sleep(.35)
                            continue

                        # Minutos
                        if minuto < 0 or minuto > 59:
                            print("Minutos inválidos, precisam estar entre 0 e 59.")
                            time.sleep(.35)
                            continue

                        # Dictionary do novo agendamento
                        novo_agendamento = {
                            "dt_consulta": data_agendamento,
                            "hr_consulta": f"{hora}:{minuto}"
                        }

                        criarAgendamento(novo_agendamento, id_paciente, medico["id_medico"], local["id_instituicao"])
                        time.sleep(.5)

                    except ValueError:
                        print("Formato inválido! Use DD/MM/AAAA para a data e HH:MM para o horário.")


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
                            data_formatada = agendamento["dt_consulta"].strftime("%d/%m/%Y")
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

            case _:
                print("\nOpção inválida!")
                time.sleep(.5)
                continue



#Função que atualiza o telefone do perfil médico do paciente no banco de dados através do ID
def updateTelefonePacientePorId(id, telefone):
    conexao = getConexao()
    if not conexao:
        return

    try:
        cursor = conexao.cursor()
        sql = "UPDATE Paciente SET num_tel = :telefone WHERE id_paciente = :id"
        cursor.execute(sql, {'telefone': telefone, 'id': id})

        conexao.commit()

    except oracledb.Error as e:
        print(f'\nErro ao atualizar telefone: {e}')
        conexao.rollback()

    finally:
        if conexao:
            conexao.close()

#Função que atualiza a altura do perfil médico do paciente no banco de dados através do ID
def updateAlturaPacientePorId(id, altura):
    conexao = getConexao()
    if not conexao:
        return

    try:
        cursor = conexao.cursor()
        sql = "UPDATE Paciente SET num_altura = :altura WHERE id_paciente = :id"
        cursor.execute(sql, {'altura': altura, 'id': id})

        conexao.commit()

    except oracledb.Error as e:
        print(f'\nErro ao atualizar altura: {e}')
        conexao.rollback()

    finally:
        if conexao:
            conexao.close()

#Função que atualiza o peso do perfil médico do paciente no banco de dados através do ID
def updatePesoPacientePorId(id, peso):
    conexao = getConexao()
    if not conexao:
        return

    try:
        cursor = conexao.cursor()
        sql = "UPDATE Paciente SET num_peso = :peso WHERE id_paciente = :id"
        cursor.execute(sql, {'peso': peso, 'id': id})

        conexao.commit()

    except oracledb.Error as e:
        print(f'\nErro ao atualizar peso: {e}')
        conexao.rollback()

    finally:
        if conexao:
            conexao.close()

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

                print("\nNovo email salvo com sucesso!")

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
    conexao = getConexao()
    if not conexao:
        return

    try:
        cursor = conexao.cursor()
        sql = "UPDATE Conta_Paciente SET ds_email = :email WHERE id_conta_paciente = :id"
        cursor.execute(sql, {'email': email, 'id': id})

        conexao.commit()

    except oracledb.Error as e:
        print(f'\nErro ao atualizar email: {e}')
        conexao.rollback()

    finally:
        if conexao:
            conexao.close()

#Função que atualiza a senha da conta do paciente no banco de dados através do ID
def updateSenhaContaPacientePorId(id, senha):
    conexao = getConexao()
    if not conexao:
        return

    try:
        cursor = conexao.cursor()
        sql = "UPDATE Conta_Paciente SET ds_senha = :senha WHERE id_conta_paciente = :id"
        cursor.execute(sql, {'senha': senha, 'id': id})

        conexao.commit()

    except oracledb.Error as e:
        print(f'\nErro ao atualizar senha: {e}')
        conexao.rollback()

    finally:
        if conexao:
            conexao.close()

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
              f"\n4 - Voltar")

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
                if nova_altura < 10:
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

            case _:
                print("Escolha inválida")
                .5
                continue


#Função que retorna o convênio médico do paciente no banco de dados, procurado com o ID do mesmo
def selectConvenioMedicoPorIdPaciente(id_paciente):
    conexao = getConexao()
    if not conexao:
        return

    try:
        cursor = conexao.cursor()
        codigo_sql = """
                        SELECT * from Convenio where fk_id_paciente = :id
                    """
        cursor.execute(codigo_sql, {
            'id': id_paciente
        })

        fetch_convenio = cursor.fetchone()
        if not fetch_convenio:
            return None
        else:
            convenio_medico = {
                "id_convenio": fetch_convenio[0],
                "nm_operadora": fetch_convenio[1],
                "num_carteirinha": fetch_convenio[2],
                "dt_inicio": fetch_convenio[3],
                "dt_validade": fetch_convenio[4],
                "fk_id_paciente": fetch_convenio[5]
            }

            return convenio_medico

    except oracledb.Error as error:
        print(f"Falha no acesso ao Banco de Dados: {error}")

    finally:
        if conexao:
            conexao.close()

#Método que mostra o menu de convênio médico
def menu_convenio_medico(id_paciente):
    while True:
        convenio_medico = selectConvenioMedicoPorIdPaciente(id_paciente)

        emissao_formatada = convenio_medico["dt_inicio"].strftime("%d/%m/%Y")  # pega só dia/mês/ano
        validade_formatada = convenio_medico["dt_validade"].strftime("%d/%m/%Y")  # pega só dia/mês/ano

        time.sleep(.35)
        print(f"\nInformações do meu Convênio Médico:"
              f"\nOperadora: {convenio_medico["nm_operadora"]};"
              f"\nNúmero da Carteirinha: {convenio_medico["num_carteirinha"]};"
              f"\nEmissão: {emissao_formatada};"
              f"\nValidade: {validade_formatada};"
              f"\n"
              f"\n0 - Voltar")

        time.sleep(.25)
        try:
            opcao_meus_dados = int(input("\nInsira o número de sua escolha: "))
            time.sleep(.3)
            match opcao_meus_dados:
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
    def gerarNovoIdRelatorio():
        conexao_id = getConexao()

        if not conexao_id:
            return False

        try:
            cursor_id = conexao_id.cursor()
            sql_id = """select MAX(id_relatorio_medico) from Relatorio_Medico"""
            cursor_id.execute(sql_id)

            maior_id = cursor_id.fetchone()

            return (maior_id[0] or 0) + 1

        except oracledb.Error as e:
            print(f'\nErro ao conectar ao Banco de Dados: {e}')
        finally:
            if conexao_id:
                conexao_id.close()

    conexao = getConexao()

    if not conexao:
        return

    try:
        cursor = conexao.cursor()
        sql = """
                INSERT INTO Relatorio_Medico (id_relatorio_medico, dt_relatorio, ds_relatorio, fk_id_medico, fk_id_paciente)
                VALUES (:id_relatorio_medico, :dt_relatorio, :ds_relatorio, :fk_id_medico, :fk_id_paciente)
            """

        id_relatorio = gerarNovoIdRelatorio()

        cursor.execute(sql, {
            'id_relatorio_medico': id_relatorio,
            'dt_relatorio': relatorio["dt_relatorio"],
            'ds_relatorio': relatorio["ds_relatorio"],
            'fk_id_medico': id_medico,
            'fk_id_paciente': id_paciente
        })
        conexao.commit()
        print(f'Relatório emitido com sucesso!')

        return id_relatorio

    except oracledb.Error as e:
        print(f'\nErro ao cadastrar o Relatório Médico: {e}')
        conexao.rollback()
    finally:
        if conexao:
            conexao.close()

#Função que deleta um relatório médico do banco de dados através do ID
def deleteRelatorioPorId(id):
    conexao = getConexao()

    if not conexao:
        return

    try:
        cursor = conexao.cursor()

        sql = "DELETE FROM Relatorio_Medico WHERE id_relatorio_medico = :id"

        cursor.execute(sql, {'id': id})
        conexao.commit()

        if cursor.rowcount > 0:
            print(f'O Relatório foi excluído com sucesso!')
        else:
            print(f'Nenhum relatório com id: {id} foi encontrado!')
    except oracledb.Error as e:
        print(f'\n Erro ao excluir relatório: {e}')
        conexao.rollback()
    finally:
        if conexao:
            conexao.close()

#Função que retorna todos os relatórios médicos no banco de dados que têm o ID do paciente
def selectRelatoriosPorIdPaciente(id_paciente):
    conexao = getConexao()
    if not conexao:
        return

    lista_relatorios = []

    try:
        cursor = conexao.cursor()
        codigo_sql = """
                    SELECT * from Relatorio_Medico where fk_id_paciente = :id
                """
        cursor.execute(codigo_sql, {
            'id': id_paciente
        })

        registros = cursor.fetchall()
        if not registros or len(registros) == 0:
            return []
        else:
            for relatorio in registros:
                novo_relatorio = {
                    "id_relatorio_medico": relatorio[0],
                    "dt_relatorio": relatorio[1],
                    "ds_relatorio": relatorio[2],
                    "fk_id_medico": relatorio[3],
                    "fk_id_paciente": relatorio[4]
                }
                lista_relatorios.append(novo_relatorio)

            return lista_relatorios

    except oracledb.Error as error:
        print(f"Falha no acesso ao Banco de Dados: {error}")

    finally:
        if conexao:
            conexao.close()

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

                    data_formatada = relatorio["dt_relatorio"].strftime("%d/%m/%Y")  # pega só dia/mês/ano
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
                    medico = random.choice(lista_medicos)

                    novo_relatorio = {}

                    try:
                        data_relatorio = datetime.strptime(data_str, "%d/%m/%Y")

                        # Dictionary do novo agendamento
                        novo_relatorio = {
                            "dt_relatorio": data_relatorio,
                            "ds_relatorio": relatorio,
                        }

                        criarRelatorio(novo_relatorio, id_paciente, medico["id_medico"])

                    except ValueError:
                        time.sleep(.5)
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
                            data_formatada = relatorio["dt_relatorio"].strftime("%d/%m/%Y")
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

            case _:
                print("\nOpção inválida!")
                time.sleep(.5)
                continue



#Função que retorna um médico do banco de dados, procurado pelo ID
def selectMedicoPorId(id):
    conexao = getConexao()
    if not conexao:
        return

    try:
        cursor = conexao.cursor()
        codigo_sql = """
            SELECT * from Medico where id_medico = :id
        """
        cursor.execute(codigo_sql, {
            'id': id
        })

        fetch_medico = cursor.fetchone()
        if not fetch_medico:
            return None
        else:
            medico = {
                "id_medico": fetch_medico[0],
                "nm_medico": fetch_medico[1],
                "ds_sexo_medico": fetch_medico[2],
                "ds_setor_medico": fetch_medico[3],
                "num_carga_horaria": fetch_medico[4],
                "vl_hora": fetch_medico[5],
                "fk_id_instituicao": fetch_medico[6]
            }

            return medico
    except oracledb.Error as error:
        print(f"Falha no acesso ao Banco de Dados: {error}")

    finally:
        if conexao:
            conexao.close()

#Função que retorna todos os médicos cadastrados no banco de dados
def selectMedicos():
    conexao = getConexao()
    if not conexao:
        return


    try:
        lista_medicos = []
        cursor = conexao.cursor()
        codigo_sql = """SELECT * from Medico"""
        cursor.execute(codigo_sql)

        registros = cursor.fetchall()
        if not registros or len(registros) == 0:
            return []
        else:
            for medico in registros:
                novo_medico = {
                    "id_medico": medico[0],
                    "nm_medico": medico[1],
                    "ds_sexo_medico": medico[2],
                    "ds_setor_medico": medico[3],
                    "num_carga_horaria": medico[4],
                    "vl_hora": medico[5],
                    "fk_id_instituicao": medico[6]
                }

                lista_medicos.append(novo_medico)

            return lista_medicos

    except oracledb.Error as error:
        print(f"Falha no acesso ao Banco de Dados: {error}")

    finally:
        if conexao:
            conexao.close()

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
                  f"\nSetor: {medico["ds_setor_medico"]}"
                  f"\nInstituição Empregadora: {instituicao['nm_razao_social']}")
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
    conexao = getConexao()
    if not conexao:
        return

    try:
        cursor = conexao.cursor()
        codigo_sql = """
            SELECT * from Instituicao where id_instituicao = :id
        """
        cursor.execute(codigo_sql, {
            'id': id
        })

        fetch_instituicao = cursor.fetchone()
        if not fetch_instituicao:
            return None
        else:
            instituicao = {
                "id_instituicao": fetch_instituicao[0],
                "nm_razao_social": fetch_instituicao[1],
                "nm_fantasia": fetch_instituicao[2],
                "ds_setor": fetch_instituicao[3],
                "num_cnpj": fetch_instituicao[4],
                "ds_endereco": fetch_instituicao[5]
            }

            return instituicao
    except oracledb.Error as error:
        print(f"Falha no acesso ao Banco de Dados: {error}")

    finally:
        if conexao:
            conexao.close()

#Função que retorna todas as instituições do banco de dados
def selectInstituicao():
    conexao = getConexao()
    if not conexao:
        return

    lista_instituicoes = []

    try:
        cursor = conexao.cursor()
        codigo_sql = """
                SELECT * from Instituicao
            """
        cursor.execute(codigo_sql)

        registros = cursor.fetchall()
        if not registros or len(registros) == 0:
            return []
        else:
            for instituicao in registros:
                nova_instituicao = {
                    "id_instituicao": instituicao[0],
                    "nm_razao_social": instituicao[1],
                    "nm_fantasia": instituicao[2],
                    "ds_setor": instituicao[3],
                    "num_cnpj": instituicao[4],
                    "ds_endereco": instituicao[5]
                }

                lista_instituicoes.append(nova_instituicao)

            return lista_instituicoes

    except oracledb.Error as error:
        print(f"Falha no acesso ao Banco de Dados: {error}")

    finally:
        if conexao:
            conexao.close()

#Método que mostra o menu de instituições médicas
def menu_instituicoes_medicas():
    while True:
        lista_instituicoes = selectInstituicao()

        print("\nLista de Instituições hospitalares:\n")
        time.sleep(.35)
        for instituicao in lista_instituicoes:
            time.sleep(.35)
            print(f"--------------------------"
                  f"\nRazão Social: {instituicao['nm_razao_social']};"
                  f"\nNome: {instituicao['nm_fantasia']};"
                  f"\nSetor: {instituicao["ds_setor"]}"
                  f"\nCNPJ: {instituicao['num_cnpj']}"
                  f"\nEndereço: {instituicao['ds_endereco']}")
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
          "\n8 - Documentos Necessários;"
          "\n9 - Ajuda;"
          "\n10 - Desconectar."
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

        time.sleep(.65)
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