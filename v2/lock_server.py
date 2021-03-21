
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
import traceback


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
    skel = skel(RESOURCES, MAX_RESOURCE_LOCKS, MAX_RESOURCES_LOCKED)
    
    # Inicialização de uma socket de escuta
    sock = su.listener_socket(HOST, PORT, 1)

    SocketList = [sock, sys.stdin]
    halt = False

    while not halt:
        
        R, W, X = sel.select(SocketList, [], [])

        for sckt in R:
            if sckt is sock:
                # Aguarda por um pedido de conexão de um cliente        
                (conn_sock, (addr, port)) = sock.accept()
                
                # (Uso do módulo color_utils por razões estéticas)
                # print(SEPARATOR)
                print(cu.colorWrite(f'Connected to {addr} on port {port}\n', 'green'), end="")
                SocketList.append(conn_sock)
                print(cu.colorWrite(f'{len(SocketList) - 2} user(s) connected\n', 'green'))


            elif sckt is sys.stdin:

                command = sys.stdin.readline().strip()
                if command.upper() == "EXIT":
                    halt = True

            else:

                # Receção da mensagem do cliente
                # Receber primeiro a quantidade de bytes na mensagem
                size_bytes = sckt.recv(4)

                if size_bytes:
                    
                    size_bytes = struct.unpack('i',size_bytes)[0]


                    # E seguidamente os bytes da mensagem
                    msg_bytes = su.receive_all(sckt, size_bytes)


                    # Obtenção da resposta
                    addr, port =  sckt.getpeername()
                    print(f"From client at {addr}:{port}")
                    size_bytes, reply_bytes = skel.processMessage(msg_bytes = msg_bytes)

                    # Enviar primeiro a quantidade de bytes ao cliente
                    sckt.sendall(size_bytes)
                    # E seguidamente, enviar os bytes da mensagem
                    sckt.sendall(reply_bytes)



                else:
                    addr, port =  sckt.getpeername()
                    print(cu.colorWrite(f'Client from {addr} on port {port} has disconnected\n', 'red'), end="")
                    sckt.close()
                    SocketList.remove(sckt)
                    print(cu.colorWrite(f'{len(SocketList) - 2} user(s) connected\n', 'red'))

    sock.close()

# Caso o servidor seja interrompido, é fechada a socket do servidor
except KeyboardInterrupt as e:
    print("\nReceived SIGINT, stopping.\n") #Received SIGINT
    sock.close()
    sys.exit(1)

# Caso haja algum problema com a abertura da socket, é comunicado o problema
except (ConnectionError, OSError):
    print(NETWORK_ERROR)
    traceback.print_exc()
    sys.exit(1)