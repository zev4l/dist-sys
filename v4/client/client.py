"""
Aplicações distribuídas - Projeto 4 - client.py
Grupo: 77
Alunos: José Almeida - 55373, Augusto Gouveia - 55371
"""

### Imports

import sys
import getopt
import requests
import os
import color_utils as cu
from pprint import pprint
import urllib3
urllib3.disable_warnings(urllib3.exceptions.SecurityWarning)

### Variáveis Globais

CERT_PATH = "/mnt/d/_/Projects/FCUL/AD/dist-sys/v4/certs/"
AUTH_ARGUMENTS = {"verify":CERT_PATH + 'root.pem', "cert":(CERT_PATH + 'cli.crt',CERT_PATH + 'cli.key')}

# Mensagens de Erro

serverCommands = ("CREATE", "READ", "DELETE", "UPDATE")
PARAMETER_ERROR = "Verifique os parâmetros.\nUtilização: client.py [-c] <IP/Hostname> <Porto>"
UNKNOWN_COMMAND_ERROR = "UNKNOWN COMMAND, TYPE 'HELP'"
MISSING_ARGUMENTS_ERROR = "MISSING ARGUMENTS"
EXCESSIVE_ARGUMENTS_ERROR = "TOO MANY ARGUMENTS"
INVALID_ARGUMENTS_ERROR = "INVALID ARGUMENTS"

GENERAL_CONNECTION_ERROR = cu.colorWrite("CONNECTION ERROR - Make sure that you're logged in and try again.", 'red')
CONNECTION_REFUSED_ERROR = cu.colorWrite("CONNECTION REFUSED", 'red')

HELP_MESSAGE = f"""{cu.colorWrite('Comandos Disponíveis', 'green')}:
  {cu.colorWrite('Servidor', 'blue')}:
    - CREATE
        - UTILIZADOR <nome> <senha>
        - ALBUM <id_spotify>
        - ARTISTA <id_spotify>
        - <id_user> <id_album> <avaliacao>
    - READ
        - UTILIZADOR <id_user>
        - ALBUM <id_album>
        - ARTISTA <id_artista>
        - ALBUM <id_album>
        - ALL <UTILIZADORES | ARTISTAS | ALBUNS>
        - ALL ALBUNS_A <id_artista>
        - ALL ALBUNS_U <id_user>
        - ALL ALBUNS <avaliacao>
    - DELETE
        - UTILIZADOR <id_user>
        - ALBUM <id_album>
        - ARTISTA <id_artista>
        - ALBUM <id_album>
        - ALL <UTILIZADORES | ARTISTAS | ALBUNS>
        - ALL ALBUNS_A <id_artista>
        - ALL ALBUNS_U <id_user>
        - ALL ALBUNS <avaliacao>
    - UPDATE
        - UTILIZADOR <id_user> <senha>
        - ALBUM <id_album> <avaliacao> <id_user>

  {cu.colorWrite('Cliente', 'blue')}:
    - CLEAR
    - HELP
    - EXIT"""



def argumentChecker(userInput):
    """
    Verifica a integridade e validade dos argumentos relativos aos comandos
    suportados pelo servidor (CREATE, READ, DELETE, UPDATE).
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

    # A partir desta linha:
    #    Verifica-se a validade de cada argumento para cada comando (nas listas acima
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

                id_user = int(arguments[0])
                id_album = int(arguments[1])

            return True

        except:  # Se o programa cai numa exceção, significa que os argumentos dados são inválidos
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

        except:  # Se o programa cai numa exceção, significa que os argumentos dados são inválidos
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
            print(INVALID_ARGUMENTS_ERROR)
            return False
        except:  # Se o programa cai numa exceção, significa que os argumentos dados são inválidos
            print(INVALID_ARGUMENTS_ERROR)
            return False


# Programa Principal

# Verificação e validação de argumentos iniciais
#
try:

    opts, args = getopt.getopt(sys.argv[1:], "c")

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

    queryUrlReadDelete = {"UTILIZADOR": f"https://{HOST}:{PORT}/utilizadores/",
                          "ALBUM": f"https://{HOST}:{PORT}/albuns/",
                          "ARTISTA": f"https://{HOST}:{PORT}/artistas/"}

    queryUrlReadDeleteAll = {"UTILIZADORES": f"https://{HOST}:{PORT}/utilizadores",
                             "ALBUNS": f"https://{HOST}:{PORT}/albuns",
                             "ARTISTAS": f"https://{HOST}:{PORT}/artistas",
                             "ALBUNS_A": f"https://{HOST}:{PORT}/albuns/artistas/",
                             "ALBUNS_U": f"https://{HOST}:{PORT}/albuns/utilizadores/",
                             "AVALIACOES": f"https://{HOST}:{PORT}/albuns/avaliacoes"}

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


            elif command == "CLEAR":
                # Limpar o histórico da consola.
                if os.name == "nt":
                    os.system("cls")
                else:
                    os.system("clear")

            elif command in serverCommands:

                if argumentChecker(userInput):
                    # Uso da função argumentChecker para verificar a integridade de validade
                    # dos argumentos fornecidos pelo utilizador em relação ao comando que o mesmo
                    # invocou

                    # Formular o pedido antes de ser enviado ao servidor, contendo o comando
                    # e os respetivos argumentos na posição correta.

                    if command == "CREATE":
                        option = arguments[0].upper()
                        if option == "UTILIZADOR":
                            utilizador = {"nome": arguments[1],
                                          "senha": arguments[2]}
                            # efetuar request
                            r = requests.post(f"https://{HOST}:{PORT}/utilizadores", json=utilizador, **AUTH_ARGUMENTS)
                            print(r.status_code)
                            print("***")
                        elif option == "ARTISTA" or option == "ALBUM":
                            query = {"id_spotify": arguments[1]}
                            # efetuar request
                            if option == "ARTISTA":
                                r = requests.post(f"https://{HOST}:{PORT}/artistas", json=query, **AUTH_ARGUMENTS)
                                print(r.status_code)
                                print("***")
                            else:
                                r = requests.post(f"https://{HOST}:{PORT}/albuns", json=query, **AUTH_ARGUMENTS)
                                print(r.status_code)
                                print("***")

                        else:
                            avaliacao = {"id_user": int(arguments[0]),
                                         "id_album": int(arguments[1]),
                                         "id_avaliacao": avaliacoes.get(arguments[2])}
                            r = requests.post(f"https://{HOST}:{PORT}/albuns/avaliacoes", **AUTH_ARGUMENTS, json=avaliacao)
                            print(r.status_code)
                            print("***")
                            # efetuar request

                    elif command == "READ" or command == "DELETE":
                        option = arguments[0]
                        if option in ("UTILIZADOR", "ARTISTA", "ALBUM"):
                            id = arguments[1]
                            # efetuar request
                            if command == "READ":
                                r = requests.get(queryUrlReadDelete.get(option) + id, **AUTH_ARGUMENTS)
                                print(r.status_code)
                                pprint(r.json())
                                print("***")
                            else:
                                r = requests.delete(queryUrlReadDelete.get(option) + id, **AUTH_ARGUMENTS)
                                print(r.status_code)
                                print("***")
                        else:
                            sub_option = arguments[1]
                            if sub_option in ("UTILIZADORES", "ARTISTAS", "AVALIACOES"):
                                if command == "READ":
                                    r = requests.get(queryUrlReadDeleteAll.get(sub_option), **AUTH_ARGUMENTS)
                                    print(r.status_code)
                                    pprint(r.json())
                                    print("***")
                                else:
                                    r = requests.delete(queryUrlReadDeleteAll.get(sub_option), **AUTH_ARGUMENTS)
                                    print(r.status_code)
                                    print("***")
                            elif sub_option == "ALBUNS":
                                if len(arguments) == 3:
                                    avaliacao = avaliacoes.get(arguments[2])
                                    if command == "READ":
                                        r = requests.get(queryUrlReadDeleteAll.get(sub_option) + f"/avaliacoes/{avaliacao}", **AUTH_ARGUMENTS)
                                        print(r.status_code)
                                        pprint(r.json())
                                        print("***")
                                    else:
                                        r = requests.delete(queryUrlReadDeleteAll.get(sub_option) + f"/avaliacoes/{avaliacao}", **AUTH_ARGUMENTS)
                                        print(r.status_code)
                                        print("***")
                                else:
                                    if command == "READ":
                                        r = requests.get(queryUrlReadDeleteAll.get(sub_option), **AUTH_ARGUMENTS)
                                        print(r.status_code)
                                        pprint(r.json())
                                        print("***")
                                    else:
                                        r = requests.delete(queryUrlReadDeleteAll.get(sub_option), **AUTH_ARGUMENTS)
                                        print(r.status_code)
                                        print("***")
                            else:
                                id = arguments[2]
                                if command == "READ":
                                    r = requests.get(queryUrlReadDeleteAll.get(sub_option) + id, **AUTH_ARGUMENTS)
                                    print(r.status_code)
                                    pprint(r.json())
                                    print("***")
                                else:
                                    r = requests.delete(queryUrlReadDeleteAll.get(sub_option) + id, **AUTH_ARGUMENTS)
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
                            r = requests.put(f"https://{HOST}:{PORT}/albuns/avaliacoes", json=avaliacao, **AUTH_ARGUMENTS)
                            print(r.status_code)
                            print("***")

                        else:  # UTILIZADOR
                            id_user = int(arguments[1])
                            utilizador = {"senha": arguments[2]}
                            # efetuar request
                            r = requests.put(f"https://{HOST}:{PORT}/utilizadores/{id_user}", json=utilizador, **AUTH_ARGUMENTS)
                            print(r.status_code)
                            print("***")

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
