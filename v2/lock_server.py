
"""
Aplicações distribuídas - Projeto 2 - lock_server.py
Grupo: 77
Números de aluno: 55373, 55371
"""

# Zona para fazer importação

import sys
import sock_utils as su
import color_utils as cu
import lock_pool as lp
import time
import select as sel
from lock_skel import skel
import struct


# código do programa principal

PARAMETER_ERROR = "Verifique os parâmetros.\nUtilização: lock_server.py <IP/Hostname> <Port> <Nº de Recursos> <Nº de Bloqueios Permitidos> <Max. de Recursos Bloqueados Simultaneamente"
NETWORK_ERROR = "Host/Port inválidos ou outro problema de ligação."
SEPARATOR = "———————————————————————————————————————"

args = sys.argv[1:]

# Verificação de argumentos

if len(args) != 5:
    print(PARAMETER_ERROR)
    sys.exit()

try:
    
    HOST = str(args[0])
    PORT = int(args[1])
    RESOURCES = int(args[2])
    MAX_RESOURCE_LOCKS = int(args[3])
    MAX_RESOURCES_LOCKED = int(args[4])
        
except Exception as e: # Se algum parâmetro se encontra incorreto, é apresentada uma mensagem de aviso 
    print(PARAMETER_ERROR)
    sys.exit(1)

try:

    # Inicialização da pool de recursos
    lockpool = lp.lock_pool(RESOURCES, MAX_RESOURCE_LOCKS, MAX_RESOURCES_LOCKED)
    
    # Inicialização de uma socket de escuta
    sock = su.listener_socket(HOST, PORT, 1)

    SocketList = [sock, sys.stdin]
    halt = False

    while True and not halt:
        
        R, W, X = sel.select(SocketList, [], [])

        for sckt in R:
            if sckt is sock:
                # Aguarda por um pedido de conexão de um cliente        
                (conn_sock, (addr, port)) = sock.accept()
                
                # (Uso do módulo color_utils por razões estéticas)
                print(SEPARATOR)
                print(cu.colorWrite(f'Connected to {addr} on port {port}\n', 'green'))
                SocketList.append(conn_sock)

            elif sckt is sys.stdin:

                command = sys.stdin.readline()
                if command.upper() == "EXIT":
                    halt = True

            else:

                # Receção da mensagem do cliente
                # Receber primeiro a quantidade de bytes na mensagem
                size_bytes = conn_sock.recv(4)
                size_bytes = struct.unpack('i',size_bytes)[0]

                print(size_bytes)

                if size_bytes:

                    # E seguidamente os bytes da mensagem
                    msg_bytes = su.receive_all(conn_sock, size_bytes)


                    # Obtenção da resposta
                    size_bytes, reply_bytes = skel.processMessage(msg_bytes)

                    # Enviar primeiro a quantidade de bytes ao cliente
                    conn_sock.sendall(size_bytes)
                    # E seguidamente, enviar os bytes da mensagem
                    conn_sock.sendall(reply_bytes)

                    # Caso o comando seja "PRINT", é feita uma colorização ao estado de cada recurso
                    if command == "PRINT":
                        reply = cu.color(reply, "PRINT")
                    else:
                        reply = cu.color(reply)

                    print(f'Received: \n    {msg}')
                    print("Sent: " + "\n    " + reply + "\n")

                else:
                    print(cu.colorWrite(f'Client from {addr} on port {port} has disconnected.\n', 'red'))
                    sckt.close()
                    SocketList.remove(conn_sock)

        
    sock.close()

# Caso o servidor seja interrompido, é fechada a socket do servidor
except KeyboardInterrupt as e:
    print("\nReceived SIGINT, stopping.\n") #Received SIGINT
    sock.close()
    sys.exit(1)

# Caso haja algum problema com a abertura da socket, é comunicado o problema
except (ConnectionError, OSError):
    print(NETWORK_ERROR)
    sys.exit(1)