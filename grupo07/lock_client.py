#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - lock_client.py
Grupo: 07
Números de aluno: 55373, 55371
"""

# TODO: DOCUMENT EVERYTHING
# TODO: colors

### Imports

from color_utils import color
from os import system
import sys
import re
from time import sleep
import net_client as nc

### Variáveis Globais

# Mensagens de Erro

serverCommands = ("LOCK", "UNLOCK", "STATUS", "STATS", "PRINT")
PARAMETER_ERROR = "Verifique os parâmetros.\nUtilização: lock_client.py <ID> <IP/Hostname> <Porto>"
UNKNOWN_COMMAND_ERROR = "UNKNOWN COMMAND"
MISSING_ARGUMENTS_ERROR = "MISSING ARGUMENTS"
EXCESSIVE_ARGUMENTS_ERROR = "TOO MANY ARGUMENTS"
INVALID_ARGUMENTS_ERROR = "INVALID ARGUMENTS"
GENERAL_CONNECTION_ERROR = "CONNECTION ERROR"
CONNECTION_REFUSED_ERROR = "CONNECTION REFUSED"
SEPARATOR = "———————————————————————"


def argumentChecker(userInput):

    # O número de argumentos tem que excluir o nome do comando
    command = userInput[0]
    arguments = userInput[1:]

    argLimits = {"LOCK":2,
                 "UNLOCK":1,
                 "STATUS":2,
                 "STATS":1,
                 "PRINT":0}

    if len(arguments) < argLimits[command]:
        print(MISSING_ARGUMENTS_ERROR)
        return False

    elif len(arguments) > argLimits[command]:
        print(EXCESSIVE_ARGUMENTS_ERROR)
        return False
        
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
        # Caso o comando seja STATS, deve-se verificar o tipo de dados
        # e integridade dos argumentos fornecidos. (("Y", "N", "D"))

        try:
            if arguments[0] not in ("Y", "N", "D"):
                raise INVALID_ARGUMENTS_ERROR

            return True
        
        except:
            print(INVALID_ARGUMENTS_ERROR)
            return False

    #TODO: fix later

    if command == "PRINT":

        return True

            



# Programa Principal

args = sys.argv[1:]

if len(args) != 3:
    print(PARAMETER_ERROR)
    sys.exit()


# Verificação de argumentos

try:
    
    ID = int(args[0])
    HOST = str(args[1])
    PORT = int(args[2])

#     TODO: fix this, has to accept all hostnames
    
#    pattern = re.compile(r"^((25[0-5]|(2[0-4]|1[0-9]|[1-9]|)[0-9])(\.(?!$)|$)){4}$")

#    if not pattern.search(HOST) and HOST.lower() != "localhost" :
#        raise Exception
    
except Exception as e:
    print(PARAMETER_ERROR)
    sys.exit(1)



while True:
    try:
        request = ""

        userInput = input("Command > ").upper().split()
        command = userInput[0]
        arguments = userInput[1:]

        if command == "EXIT":
            break

        if command == "SLEEP":
            try:
                amount = int(arguments[0])
                sleep(amount)
                    
            except:
                print(MISSING_ARGUMENTS_ERROR)
            
            continue

        if command == "CLEAR":
            system("clear")
            continue

        if command in serverCommands:


            if argumentChecker(userInput):
            
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
            print(UNKNOWN_COMMAND_ERROR)



        if request:
            
            try:
            
                server = nc.server(HOST, PORT)
                server.connect()
                response = server.send_receive(request.encode("utf-8")).decode("utf-8")
                server.close()

                response = color(response, command)

                print("Sent:\n    " + request)
                print("Received:\n    " + response)

            except ConnectionRefusedError:
                print(CONNECTION_REFUSED_ERROR)

            except ConnectionError:
                print(GENERAL_CONNECTION_ERROR)

    except KeyboardInterrupt as e:
        print("\nReceived SIGINT, stopping.\n") #Received SIGINT
        sys.exit(1)

    print()