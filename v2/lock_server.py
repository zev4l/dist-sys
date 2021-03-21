
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

    while True:
        
        # Aguarda por um pedido de conexão de um cliente        
        (conn_sock, (addr, port)) = sock.accept()
        
        # (Uso do módulo color_utils por razões estéticas)
        print(SEPARATOR)
        print(cu.colorWrite(f'Connected to {addr} on port {port}\n', 'green'))
        
        # Remoção de bloqueios expirados/desabilitação de recursos 
        lockpool.clear_expired_locks()

        # Receção da mensagem do cliente
        # TODO: Altera para receber primeiro os 4 bytes do inteiro e depois a mensagem
 

        msg = su.receive_all(conn_sock, 1024).decode("utf-8")

        # Divisão da mensagem recebida 
        parsed_msg = msg.split()

        # O comando pretendido encontra-se na primeira parte da mensagem recebida
        command = parsed_msg[0].upper()

        reply = "NOK"

        if command == "LOCK": 
            # Caso o comando seja "LOCK", são passados como argumentos ao comando interno 
            # o ID do recurso, o tempo limite desejado e o ID do cliente
            r_id = int(parsed_msg[1])
            time_limit = int(parsed_msg[2])
            c_id = int(parsed_msg[3])

            # A resposta ao cliente depende da conclusão do comando pretendido
            reply = lockpool.lock(r_id, c_id, time_limit)
        
        elif command == "UNLOCK":
            # Caso o comando seja "UNLOCK", são passados como argumentos ao comando interno
            # o ID do recurso e o ID do cliente
            r_id = int(parsed_msg[1])
            c_id = int(parsed_msg[2])
            
            # A resposta ao cliente depende da conclusão do comando pretendido
            reply = lockpool.unlock(r_id, c_id)
        
        elif command == "STATUS":
            # Caso o comando seja "STATUS", são passados como argumentos ao comando interno
            # a opção pretendida e o ID do cliente
            option = parsed_msg[1]
            r_id = int(parsed_msg[2])

            # A resposta ao cliente depende da conclusão do comando pretendido
            reply = lockpool.status(option, r_id)

        elif command == "STATS":
            # Caso o comando seja "STATS", é passado como argumento ao comando internp
            # a opção pretendida
            option = parsed_msg[1]

            # A resposta ao cliente depende da conclusão do comando pretendido
            reply = lockpool.stats(option)
        
        elif command == "PRINT":
            # Caso o comando seja "PRINT", é enviada como resposta o epoch atual
            # e o estado de cada recurso
            reply = f"Current Epoch: {int(time.time())}\n    "
            reply += repr(lockpool)

        # Cast da resposta para uma string
        reply = str(reply)

        # Envio da resposta ao cliente
        conn_sock.sendall(reply.encode("utf-8"))

        # Caso o comando seja "PRINT", é feita uma colorização ao estado de cada recurso
        if command == "PRINT":
            reply = cu.color(reply, "PRINT")
        else:
            reply = cu.color(reply)

        print(f'Received: \n    {msg}')
        print("Sent: " + "\n    " + reply + "\n")

        # Fecho da ligação com o cliente
        conn_sock.close()
        
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