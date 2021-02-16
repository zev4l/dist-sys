#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - lock_client.py
Grupo: 07
Números de aluno: 55373, 55371
"""
# Zona para fazer imports

import sys
import re


# Programa principal

args = sys.argv[1:]

if len(args) != 3:
    print("Utilização: lock_client.py <ID> <IP/Hostname> <Porto>")
    sys.exit()


# Verificação de argumentos

try:
    
    ID = int(args[0])
    HOST = str(args[1])
    PORT = int(args[2])

    pattern = re.compile(r"^((25[0-5]|(2[0-4]|1[0-9]|[1-9]|)[0-9])(\.(?!$)|$)){4}$")

    if not pattern.search(HOST):
        raise Exception
    
except Exception as e:
    print("Utilização: lock_client.py <ID> <IPv4/Hostname> <Port>")
    sys.exit(1)



while True:
    query = input("Comando > ")
    if query.upper() == "EXIT":
        break


#print(args)