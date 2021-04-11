"""
Aplicações distribuídas - Projeto 2 - lock_client.py
Grupo: 77
Números de aluno: 55373, 55371
"""

### Imports

import sys
import getopt
import requests
# from lock_stub import stub
from os import system
from time import sleep

# import net_client as nc
import color_utils as cu
from pprint import pprint

### Variáveis Globais

# Mensagens de Erro

serverCommands = ("CREATE", "READ", "DELETE", "UPDATE")
PARAMETER_ERROR = "Verifique os parâmetros.\nUtilização: lock_client.py [-c] [-r] <ID> <IP/Hostname> <Porto>"
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

    argLimitsCreate = {"UTILIZADOR": 3,
                       "ARTISTA": 2,
                       "ALBUM": 2
                       }

    argLimitsReadDelete = {"UTILIZADOR": 2,
                           "ARTISTA": 2,
                           "ALBUM": 2
                           }

    argLimitsReadDeleteAll = {"UTILIZADORES": 2,
                              "ARTISTAS": 2,
                              "ALBUNS_A": 3,
                              "ALBUNS_U": 3,
                              "ALBUNS": 3}

    # if len(arguments) < argLimits[command]:
    #     # Emitir erro de argumentos insuficientes e retornar False caso
    #     # a quantidade de argumentos presentes nos dados introduzidos pelo
    #     # utilizador for menor que a quantidadede argumentos esperada para
    #     # o comando em causa.
    #
    #     print(MISSING_ARGUMENTS_ERROR)
    #     return False
    #
    # elif len(arguments) > argLimits[command]:
    #     # Emitir erro de argumentos em demasia e retornar False caso a
    #     # quantidade de argumentos presentes nos dados introduzidos pelo
    #     # utilizador não for maior que a quantidade de argumentos esperada
    #     # para o comando em causa.
    #
    #     print(EXCESSIVE_ARGUMENTS_ERROR)
    #     return False

    # A partir desta linha:
    #    Verifica-se a validade de cada argumento para cada comando (na lista acima
    #    definida), devolvendo False e emitindo um erro de argumentos inválidos caso
    #    os tipos de dados dos argumentos introduzidos pelo utilizador não corresponderem
    #    com os tipos de dados esperados para os argumentos do comando em causa.

    if command == "CREATE":
        try:
            option = arguments[0]
            if not option.isnumeric():
                max_arg = argLimitsCreate.get(option)
                if len(arguments) < max_arg:
                    # Emitir erro de argumentos insuficientes e retornar False caso
                    # a quantidade de argumentos presentes nos dados introduzidos pelo
                    # utilizador for menor que a quantidadede argumentos esperada para
                    # o comando em causa.

                    print(MISSING_ARGUMENTS_ERROR)
                    return False

                elif len(arguments) > max_arg:
                    # Emitir erro de argumentos em demasia e retornar False caso a
                    # quantidade de argumentos presentes nos dados introduzidos pelo
                    # utilizador não for maior que a quantidade de argumentos esperada
                    # para o comando em causa.

                    print(EXCESSIVE_ARGUMENTS_ERROR)
                    return False

            else:
                if len(arguments) < 3:
                    print(MISSING_ARGUMENTS_ERROR)
                    return False

                elif len(arguments) > 3:
                    print(EXCESSIVE_ARGUMENTS_ERROR)
                    return False

                id_user = int(arguments[1])
                id_album = int(arguments[2])

            return True


        except:
            print(INVALID_ARGUMENTS_ERROR)
            return False

    elif command == "READ" or command == "DELETE":
        try:
            option = arguments[0]
            sub_option = arguments[1]
            if option != "ALL":
                max_arg = argLimitsReadDelete.get(option)
            else:
                max_arg = argLimitsReadDeleteAll.get(sub_option)
            if sub_option != "ALBUNS":
                if len(arguments) < max_arg:
                    # Emitir erro de argumentos insuficientes e retornar False caso
                    # a quantidade de argumentos presentes nos dados introduzidos pelo
                    # utilizador for menor que a quantidadede argumentos esperada para
                    # o comando em causa.

                    print(MISSING_ARGUMENTS_ERROR)
                    return False

                elif len(arguments) > max_arg:
                    # Emitir erro de argumentos em demasia e retornar False caso a
                    # quantidade de argumentos presentes nos dados introduzidos pelo
                    # utilizador não for maior que a quantidade de argumentos esperada
                    # para o comando em causa.

                    print(EXCESSIVE_ARGUMENTS_ERROR)
                    return False
            else:
                if len(arguments) > 3:
                    print(EXCESSIVE_ARGUMENTS_ERROR)
                    return False

            if option in ("UTILIZADOR", "ARTISTA", "ALBUM"):
                id = int(arguments[1])
            elif option == "ALL":
                sub_option = arguments[1]
                if sub_option in ("ALBUNS_A", "ALBUNS_U"):
                    id = int(arguments[2])
                elif sub_option in ("ALBUNS", "AVALIACOES", "ARTISTAS", "UTILIZADORES"):
                    return True
                else:
                    return False
            else:
                return False

            return True

        except:
            print(INVALID_ARGUMENTS_ERROR)
            return False

    elif command == "UPDATE":
        try:
            option = arguments[0]
            if option == "ALBUM":
                if len(arguments) < 4:
                    print(MISSING_ARGUMENTS_ERROR)
                    return False
                elif len(arguments) > 4:
                    print(EXCESSIVE_ARGUMENTS_ERROR)
                    return False
                id_album = int(arguments[1])
                id_user = int(arguments[3])
                return True
            elif option == "UTILIZADOR":
                if len(arguments) < 3:
                    print(MISSING_ARGUMENTS_ERROR)
                    return False
                elif len(arguments) > 3:
                    print(EXCESSIVE_ARGUMENTS_ERROR)
                    return False
                id_user = int(arguments[1])
                return True
            return False
        except:
            print(INVALID_ARGUMENTS_ERROR)
            return False


# Programa Principal

# Verificação e validação de argumentos iniciais
#
try:

    opts, args = getopt.getopt(sys.argv[1:], "rc")

    HOST = str(args[0])
    PORT = int(args[1])

    if len(args) != 2:
        raise PARAMETER_ERROR

except Exception as e:
    # Emitir erro de parâmetros e terminar o processo
    # caso a validade dos argumentos introduzidos não se
    # verifique.

    print(PARAMETER_ERROR)
    sys.exit(1)

halt = False

try:
    avaliacoes = {"M": 1,
                  "m": 2,
                  "S": 3,
                  "B": 4,
                  "MB": 5}

    queryUrlReadDelete = {"UTILIZADOR": f"http://{HOST}:{PORT}/utilizadores/",
                          "ALBUM": f"http://{HOST}:{PORT}/albuns/",
                          "ARTISTA": f"http://{HOST}:{PORT}/artistas/"}

    queryUrlReadDeleteAll = {"UTILIZADORES": f"http://{HOST}:{PORT}/utilizadores",
                             "ALBUNS": f"http://{HOST}:{PORT}/albuns",
                             "ARTISTAS": f"http://{HOST}:{PORT}/artistas",
                             "ALBUNS_A": f"http://{HOST}:{PORT}/albuns/artistas/",
                             "ALBUNS_U": f"http://{HOST}:{PORT}/albuns/utilizadores/",
                             "AVALIACOES": f"http://{HOST}:{PORT}/albuns/avaliacoes"}

    while not halt:
        try:

            # Processamento dos dados introduzidos pelo utilizador
            if not len([opt for opt in opts if "-c" in opt]):
                handle = f"client ▶ {cu.colorWrite(HOST, 'green')}: "
            else:
                handle = f"client ▶ {HOST}:"

            userInput = input(handle).split()

            # Passar ao próximo ciclo caso o utilizador não introduza nada
            if not userInput:
                continue

            command = userInput[0].upper()
            arguments = userInput[1:]

            if command == "EXIT":
                # Sair do ciclo caso o utilizador invoque o comando EXIT
                halt = True
                continue

            elif command == "HELP":
                print(HELP_MESSAGE)


            # elif command == "SLEEP":
            #     # Invocar sleep pela duração referida pelo utilizador caso este
            #     # use o comando SLEEP. Caso o utilizador inclua a quantidade errada
            #     # de argumentos, será informado através dos erros correspondentes,
            #     # o mesmo acontecerá caso o argumento seja inválido.
            #
            #     try:
            #         if len(arguments) > 1:
            #             raise AssertionError
            #
            #         amount = int(arguments[0])
            #         sleep(amount)
            #
            #     except ValueError:
            #         print(INVALID_ARGUMENTS_ERROR)
            #
            #     except AssertionError:
            #         print(EXCESSIVE_ARGUMENTS_ERROR)
            #
            #     except:
            #         print(MISSING_ARGUMENTS_ERROR)

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

                    if command == "CREATE":
                        option = arguments[0].upper()
                        if option == "UTILIZADOR":
                            utilizador = {"nome": arguments[1],
                                          "senha": arguments[2]}
                            # efetuar request
                            r = requests.post(f"http://{HOST}:{PORT}/utilizadores", json=utilizador)
                            print(r.status_code)
                            print("***")
                        elif option == "ARTISTA" or option == "ALBUM":
                            query = {"id_spotify": arguments[1]}
                            # efetuar request
                            if option == "ARTISTA":
                                r = requests.post(f"http://{HOST}:{PORT}/artistas", json=query)
                                print(r.status_code)
                                print("***")
                            else:
                                r = requests.post(f"http://{HOST}:{PORT}/albuns", json=query)
                                print(r.status_code)
                                print("***")

                        else:
                            avaliacao = {"id_user": int(arguments[0]),
                                         "id_album": int(arguments[1]),
                                         "id_avaliacao": avaliacoes.get(arguments[2])}
                            r = requests.post(f"http://{HOST}:{PORT}/albuns/avaliacoes", json=avaliacao)
                            print(r.status_code)
                            print("***")
                            # efetuar request

                    elif command == "READ" or command == "DELETE":
                        option = arguments[0]
                        if option in ("UTILIZADOR", "ARTISTA", "ALBUM"):
                            id = arguments[1]
                            # efetuar request
                            if command == "READ":
                                r = requests.get(queryUrlReadDelete.get(option) + id)
                                print(r.status_code)
                                pprint(r.json())
                                print("***")
                            else:
                                r = requests.delete(queryUrlReadDelete.get(option) + id)
                                print(r.status_code)
                                print("***")
                        else:
                            sub_option = arguments[1]
                            if sub_option in ("UTILIZADORES", "ARTISTAS", "AVALIACOES"):
                                if command == "READ":
                                    r = requests.get(queryUrlReadDeleteAll.get(sub_option))
                                    print(r.status_code)
                                    pprint(r.json())
                                    print("***")
                                else:
                                    r = requests.delete(queryUrlReadDeleteAll.get(sub_option))
                                    print(r.status_code)
                                    print("***")
                            elif sub_option == "ALBUNS":
                                if len(arguments) == 3:
                                    avaliacao = avaliacoes.get(arguments[2])
                                    if command == "READ":
                                        r = requests.get(queryUrlReadDeleteAll.get(sub_option) + f"/avaliacoes/{avaliacao}")
                                        print(r.status_code)
                                        pprint(r.json())
                                        print("***")
                                    else:
                                        r = requests.delete(queryUrlReadDeleteAll.get(sub_option + f"/avaliacoes/{avaliacao}"))
                                        print(r.status_code)
                                        print("***")
                                else:
                                    if command == "READ":
                                        r = requests.get(queryUrlReadDeleteAll.get(sub_option))
                                        print(r.status_code)
                                        pprint(r.json())
                                        print("***")
                                    else:
                                        r = requests.delete(queryUrlReadDeleteAll.get(sub_option))
                                        print(r.status_code)
                                        print("***")
                            else:
                                id = arguments[2]
                                if command == "READ":
                                    r = requests.get(queryUrlReadDeleteAll.get(sub_option) + id)
                                    print(r.status_code)
                                    pprint(r.json())
                                    print("***")
                                else:
                                    r = requests.delete(queryUrlReadDeleteAll.get(sub_option) + id)
                                    print(r.status_code)
                                    print("***")
                                # efetuar request

                    else:  # UPDATE
                        option = arguments[0]
                        if option == "ALBUM":
                            avaliacao = {"id_album": int(arguments[1]),
                                         "id_avaliacao": avaliacoes.get(arguments[2]),
                                         "id_user": int(arguments[3])}
                            # efetuar request
                            r = requests.put(f"http://{HOST}:{PORT}/albuns/avaliacoes", json=avaliacao)
                            print(r.status_code)
                            print("***")

                        else:  # UTILIZADOR
                            id_user = int(arguments[1])
                            utilizador = {"senha": arguments[2]}
                            # efetuar request
                            r = requests.put(f"http://{HOST}:{PORT}/utilizadores/{id_user}", json=utilizador)
                            print(r.status_code)
                            print("***")

                    # if len([opt for opt in opts if "-r" in opt]):
                    #     # Uso da função auxiliar translate() para traduzir o conteúdo
                    #     # recebido do servidor em algo legível para o utilizador
                    #     response = translate(response)
                    #
                    # if not len([opt for opt in opts if "-c" in opt]):
                    #     # Uso do módulo color_utils para estilizar o output
                    #     response = cu.color(response, command)

                    # Impressão dos dados enviados e recebidos
                    # print("\nSent:\n" + str(request))
                    #
                    # if command == "PRINT":
                    #     print("\nReceived:\n[" + str(response[0]) + ",")
                    #     print(response[1] + "]\n")
                    # else:
                    #     print("\nReceived:\n" + "[" + ", ".join([str(elem) for elem in response]) + "]" + "\n")

            else:
                # Emitir erro de comando desconhecido caso este não se encontre na lista
                # de comandos suportados pelo servidor e cliente.

                print(UNKNOWN_COMMAND_ERROR)

        except KeyboardInterrupt as e:
            # Lidar com KeyboardInterrupt
            print("\nReceived SIGINT, stopping.\n")
            sys.exit(1)

except ConnectionRefusedError:
    # Emitir erro de conexão recusada caso seja impossível contactar o servidor.
    print(CONNECTION_REFUSED_ERROR)

except Exception as e:
    # Emitir erro geral de conexão caso hajam quaisqueres complicações no processo
    # de envio do pedido ao servidor e receção da resposta.
    print(GENERAL_CONNECTION_ERROR)
