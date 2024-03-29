"""
Aplicações distribuídas - Projeto 1 - lock_client.py
Grupo: 77
Números de aluno: 55373, 55371
"""

### Imports

import color_utils as cu
from os import system
import sys
from time import sleep
import net_client as nc

### Variáveis Globais

# Mensagens de Erro

serverCommands = ("LOCK", "UNLOCK", "STATUS", "STATS", "PRINT")
PARAMETER_ERROR = "Verifique os parâmetros.\nUtilização: lock_client.py <ID> <IP/Hostname> <Porto>"
UNKNOWN_COMMAND_ERROR = "UNKNOWN COMMAND, TYPE 'HELP'"
MISSING_ARGUMENTS_ERROR = "MISSING ARGUMENTS"
EXCESSIVE_ARGUMENTS_ERROR = "TOO MANY ARGUMENTS"
INVALID_ARGUMENTS_ERROR = "INVALID ARGUMENTS"
GENERAL_CONNECTION_ERROR = cu.colorWrite("CONNECTION ERROR", 'red')
CONNECTION_REFUSED_ERROR = cu.colorWrite("CONNECTION REFUSED", 'red')

HELP_MESSAGE = f"""{cu.colorWrite('Comandos Disponíveis', 'green')}:
  {cu.colorWrite('Servidor', 'blue')}:
    -LOCK <número do recurso> <limite de tempo>
    -UNLOCK <número do recurso>
    -STATUS R/K <número do recurso>
    -STATS Y/N/D
    -PRINT

  {cu.colorWrite('Cliente', 'blue')}:
    -SLEEP <limite de tempo>
    -HELP
    -EXIT"""



def argumentChecker(userInput):
    """
    Verifica a integridade e validade dos argumentos relativos aos comandos
    suportados pelo servidor (LOCK, UNLOCK, STATUS, STATS, PRINT).
    Requires: userInput é uma lista representante dos vários dados introduzidos
    pelo utilizador.
    Ensures: Devolve um booleano representando a validade dos argumentos introduzidos
    respetivamente ao comando invocado.
    """
    

    # O número de argumentos tem que excluir o nome do comando
    command = userInput[0]
    arguments = userInput[1:]

    argLimits = {"LOCK":2,
                 "UNLOCK":1,
                 "STATUS":2,
                 "STATS":1,
                 "PRINT":0}

    if len(arguments) < argLimits[command]:
        # Emitir erro de argumentos insuficientes e retornar False caso 
        # a quantidade de argumentos presentes nos dados introduzidos pelo
        # utilizador for menor que a quantidadede argumentos esperada para
        # o comando em causa. 

        print(MISSING_ARGUMENTS_ERROR)
        return False

    elif len(arguments) > argLimits[command]:
        # Emitir erro de argumentos em demasia e retornar False caso a 
        # quantidade de argumentos presentes nos dados introduzidos pelo
        # utilizador não for maior que a quantidade de argumentos esperada
        # para o comando em causa. 
        
        print(EXCESSIVE_ARGUMENTS_ERROR)
        return False
        

    # A partir desta linha:
    #    Verifica-se a validade de cada argumento para cada comando (na lista acima
    #    definida), devolvendo False e emitindo um erro de argumentos inválidos caso
    #    os tipos de dados dos argumentos introduzidos pelo utilizador não corresponderem
    #    com os tipos de dados esperados para os argumentos do comando em causa.

    if command == "LOCK":
        # Caso o comando seja LOCK, deve-se verificar o tipo de dados
        # e integridade dos argumentos fornecidos. (int, int)
        try:
            int(arguments[0])
            int(arguments[1])
            return True

        except:
            print(INVALID_ARGUMENTS_ERROR)
            return False

    if command == "UNLOCK":
        # Caso o comando seja UNLOCK, deve-se verificar o tipo de dados
        # e integridade dos argumentos fornecidos. (int)
        try:
            int(arguments[0])
            return True

        except:
            print(INVALID_ARGUMENTS_ERROR)
            return False

    if command == "STATUS":
        # Caso o comando seja STATUS, deve-se verificar o tipo de dados
        # e integridade dos argumentos fornecidos. (("R", "K"), int)

        try:
            if arguments[0] not in ("R", "K"):
                raise INVALID_ARGUMENTS_ERROR
                
            int(arguments[1])
            return True

        except:
            print(INVALID_ARGUMENTS_ERROR)
            return False

    if command == "STATS":
        # Caso o comando seja STATS, deve-se verificar
        # e integridade dos argumentos fornecidos. (("Y", "N", "D"))

        try:
            if arguments[0] not in ("Y", "N", "D"):
                raise INVALID_ARGUMENTS_ERROR

            return True
        
        except:
            print(INVALID_ARGUMENTS_ERROR)
            return False

    if command == "PRINT":
        # Caso o comando seja PRINT, dão-se automaticamente como válidos
        # os dados introduzidos pelo utilizador pois este comando não requer
        # argumentos.

        return True


# Programa Principal

args = sys.argv[1:]

# Verificaçã e validação de argumentos iniciais

try:
    
    ID = int(args[0])
    HOST = str(args[1])
    PORT = int(args[2])

    if len(args) != 3:
        raise PARAMETER_ERROR
    
except Exception as e:
    # Emitir erro de parâmetros e terminar o processo
    # caso a validade dos argumentos introduzidos não se
    # verifique.

    print(PARAMETER_ERROR)
    sys.exit(1)

halt = False

while not halt:
    try:

        # Inicialização da variável que irá albergar o request enviado para
        # o servidor
        request = ""

        # Processamento dos dados introduzidos pelo utilizador
        userInput = input(f"client_{ID} ▶ {cu.colorWrite(HOST, 'green')}: ").upper().split()

        # Passar ao próximo ciclo caso o utilizador não introduza nada
        if not userInput:
            continue

        command = userInput[0]
        arguments = userInput[1:]


        if command == "EXIT":
            # Sair do ciclo caso o utilizador invoque o comando EXIT
            halt = True
            continue

        elif command == "HELP":
            print(HELP_MESSAGE)


        elif command == "SLEEP":
            # Invocar sleep pela duração referida pelo utilizador caso este
            # use o comando SLEEP. Caso o utilizador inclua a quantidade errada
            # de argumentos, será informado através dos erros correspondentes,
            # o mesmo acontecerá caso o argumento seja inválido.
            
            try:
                if len(arguments) > 1:
                    raise AssertionError

                amount = int(arguments[0])
                sleep(amount)
                    
            except ValueError:
                print(INVALID_ARGUMENTS_ERROR)
            
            except AssertionError:
                print(EXCESSIVE_ARGUMENTS_ERROR)

            except:
                print(MISSING_ARGUMENTS_ERROR)


        elif command == "CLEAR":
            # Limpar o histórico da consola caso o utilizador invoque o comando SLEEP.
            system("clear")


        elif command in serverCommands:
            
            if argumentChecker(userInput):
            # Uso da função argumentChecker para verificar a integridade de validade
            # dos argumentos fornecidos pelo utilizador em relação ao comando que o mesmo
            # invocou


                # Formular o pedido antes de ser enviado ao servidor, contendo o comando
                # e os respetivos argumentos na posição correta.
                # Quando se trata de LOCK e UNLOCK, adicionar também o ID do cliente 
                # ao pedido.

                if command == "LOCK":
                    
                        request = f"{command} {arguments[0]} {arguments[1]} {ID}"

                if command == "UNLOCK":

                        request = f"{command} {arguments[0]} {ID}"

                
                if command == "STATUS":

                    option = arguments[0]
                    value = arguments[1]

                    request = f"{command} {option} {value}"

                if command == "STATS":

                    option = arguments[0]

                    request = f"{command} {option}"

                if command == "PRINT":
                    request = command
            

        else:
            # Emitir erro de comando desconhecido caso este não se encontre na lista
            # de comandos suportados pelo servidor e cliente.

            print(UNKNOWN_COMMAND_ERROR)


        # Caso o pedido tenha sido formulado corretamente:
        if request:
            
            try:
                # Uso do módulo net_client para estabelecer uma ligação ao servidor 
                server = nc.server(HOST, PORT)
                server.connect()

                # Processamento da resposta recebida e fecho da conexão
                response = server.send_receive(request.encode("utf-8")).decode("utf-8")
                server.close()

                # Uso do módulo color_utils para estilizar o output
                response = cu.color(response, command)

                print("\nSent:\n    " + request)
                print("Received:\n    " + response)

            except ConnectionRefusedError:
                # Emitir erro de conexão recusada caso seja impossível contactar o servidor.
                print(CONNECTION_REFUSED_ERROR)

            except:
                # Emitir erro geral de conexão caso hajam quaisqueres complicações no processo
                # de envio do pedido ao servidor e receção da resposta. 
                print(GENERAL_CONNECTION_ERROR)
            

    except KeyboardInterrupt as e:
        # Lidar com KeyboardInterrupt
        print("\nReceived SIGINT, stopping.\n")
        sys.exit(1)

    print()