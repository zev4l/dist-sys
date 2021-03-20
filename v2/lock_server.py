
"""
Aplicações distribuídas - Projeto 1 - lock_server.py
Grupo: 77
Números de aluno: 55373, 55371
"""

# Zona para fazer importação

import time
import sys
import sock_utils as su
import color_utils as cu

###############################################################################


class resource_lock:
    """
    Classe dedicada à representação de um recurso.
    """

    def __init__(self, resource_id):
        """
        Define e inicializa as características de um recurso.
        """
        self._resource_id = resource_id
        self._state = "UNLOCKED"
        self._lock_client_id = -1
        self._lock_timer = time.time()
        self._lock_counter = 0

    def lock(self, client_id, time_limit):
        """
        Tenta bloquear o recurso pelo cliente client_id, durante time_limit 
        segundos, alterando os valores associados ao bloqueio. Retorna OK ou NOK.
        """

        # Caso o recurso se encontre desbloqueado, o mesmo passa a estar bloqueado
        if self._state == "UNLOCKED": 
            self._state = "LOCKED"
            self._lock_client_id = client_id
            self._lock_counter += 1
            self._lock_timer = time.time() + time_limit
            return "OK"
            
        # Caso o recurso se encontre bloqueado && o cliente que esteja
        # a tentar bloquear o recurso seja o dono do bloqueio atual, 
        # o tempo de bloqueio é estendido    
        elif self._state == "LOCKED": 
            if self._lock_client_id == client_id: 
                self._lock_timer = time.time() + time_limit
                self._lock_counter += 1
                return "OK"
        return "NOK"

    def release(self):
        """
        Liberta o recurso incondicionalmente, alterando
        os valores associados ao bloqueio.
        """
        self._state = "UNLOCKED"

    def unlock(self, client_id):
        """
        Liberta o recurso se este está bloqueado pelo cliente client_id.
        Retorna OK ou NOK.
        """
        # Caso o cliente que esteja a tentar desbloquear o recurso 
        # seja o mesmo que o bloqueou, o recurso é desbloqueado 
        if self._lock_client_id == client_id: 
            self.release()
            return "OK"
        return "NOK"

    def status(self, option):
        """
        Obtém o estado do recurso. Se option for R, retorna LOCKED ou UNLOCKED 
        ou DISABLED. Se option for K, retorna <número de bloqueios feitos no 
        recurso>. Se option for T, retorna <epoch de tempo bloqueado>.
        """
        if option == 'R':
            return self._state
        elif option == 'K':
            return self._lock_counter
        elif option == 'T':
            return self._lock_timer

    def disable(self):
        """
        Coloca o recurso como desabilitado incondicionalmente, alterando os 
        valores associados à sua disponibilidade.
        """
        self._state = "DISABLED"

    def __repr__(self):
        """
        Representação da classe para a saída standard. A string devolvida por
        esta função é usada, por exemplo, se uma instância da classe for
        passada à função print ou str.
        """
        output = f"R {self._resource_id} {self._state} {self._lock_counter} "
        
        # Se o recurso está bloqueado:
        # R <número do recurso> bloquado <id do cliente> <instante limite da 
        # concessão do bloqueio>
        # Se o recurso está desbloquado:
        # R <número do recurso> desbloqueado
        # Se o recurso está inativo:
        # R <número do recurso> inativo
        
        if self._state == "LOCKED":
            output += f"{self._lock_client_id} {int(self._lock_timer)}"
        
        return output

###############################################################################

class lock_pool:
    """
    Classe dedicada à pool de recursos.
    """
    def __init__(self, N, K, Y):
        """
        Define um array com um conjunto de N recursos. Os recursos podem
        ser manipulados pelos métodos desta classe. Define K, o número máximo 
        de bloqueios permitidos para cada recurso. Ao atingir K, o recurso fica 
        desabilitado. Define Y, o número máximo permitido de recursos 
        bloqueados num dado momento. Ao atingir Y, não é possível realizar mais 
        bloqueios até que um recurso seja libertado.
        """
        self._locks = []

        for i in range(N):
            self._locks.append(resource_lock(i)) 
        
        self._max_lock_counter = K
        self._max_locked_resources = Y
    

    def clear_expired_locks(self):
        """
        Verifica se os recursos que estão bloqueados ainda estão dentro do tempo
        de concessão dos bloqueios. Remove os bloqueios para os quais o tempo de
        concessão tenha expirado.
        """
        for i in self._locks:

            # Se o recurso se encontra bloqueado && 
            # o epoch atual for maior do que o epoch de bloqueio do recurso, 
            # o mesmo deve ser desbloqueado
            if i.status('R') == "LOCKED" and time.time() > i.status('T'): 
                i.release()

                # Se o contador de bloqueios do recurso é igual ao 
                # número máximo de bloqueios permitidos para cada recurso, 
                # procede-se à desabilitação do mesmo
                if i.status('K') == self._max_lock_counter: 
                    i.disable()


    def lock(self, resource_id, client_id, time_limit):
        """
        Tenta bloquear o recurso resource_id pelo cliente client_id, durante
        time_limit segundos. Retorna OK, NOK ou UNKNOWN RESOURCE.
        """
        if resource_id >= 0 and resource_id < (len(self._locks)): # Se o recurso que pretende bloquear existe na pool

            # Se o recurso ainda não atingiu o máximo de bloqueios && 
            # o total de recursos bloqueados não excedem o máximo de recursos bloqueados
            if self.status('K', resource_id) < self._max_lock_counter and self.stats('Y') < self._max_locked_resources:    
                if self.status('R', resource_id) != "DISABLED": # Se o recurso não se encontra desabilitado
                    resource = self._locks[resource_id]

                    # O resultado desta função depende da conclusão da função do recurso
                    return resource.lock(client_id, time_limit)
            return "NOK"
        return "UNKNOWN RESOURCE"
                
    def unlock(self, resource_id, client_id):
        """
        Liberta o bloqueio sobre o recurso resource_id pelo cliente client_id.
        Retorna OK, NOK ou UNKNOWN RESOURCE.
        """
        if resource_id >= 0 and resource_id < (len(self._locks)): # Se o recurso que pretende desbloquear existe na pool
            if self.status('R', resource_id) != "UNLOCKED" and self.status('R', resource_id) != "DISABLED": # Se o recurso está bloqueado
                resource = self._locks[resource_id]
                
                # O resultado desta função depende da conclusão da função do recurso
                return resource.unlock(client_id)
            return "NOK"
        return "UNKNOWN RESOURCE"

    def status(self, option, resource_id):
        """
        Obtém o estado de um recurso. Se option for R, retorna LOCKED, UNLOCKED,
        DISABLED ou UNKNOWN RESOURCE. Se option for K, retorna <número de 
        bloqueios feitos no recurso> ou UNKNOWN RESOURCE.
        """
        if resource_id >= 0 and resource_id < (len(self._locks)): # Se o recurso que pretende consultar existe na pool
            resource = self._locks[resource_id]
            
            # O resultado desta função depende da conclusão da função do recurso
            return resource.status(option)
        return "UNKNOWN RESOURCE"

    def stats(self, option):
        """
        Obtém o estado do serviço de exclusão mútua. Se option for Y, retorna 
        <número de recursos bloqueados atualmente>. Se option for N, retorna 
        <número de recursos disponíveis atualmente>. Se option for D, retorna 
        <número de recursos desabilitados>
        """
        if option.upper() == 'Y':
            total_locked_resources = 0
            # Iterar a lista de recursos à procura dos que se encontram bloqueados
            for lock in self._locks:
                if lock.status('R') == 'LOCKED':
                    total_locked_resources += 1
            return total_locked_resources
        
        elif option.upper() == "N":
            total_unlocked_resources = 0
            # Iterar a lista de recursos à procura dos que se encontram desbloqueados
            for lock in self._locks:
                if lock.status('R') == "UNLOCKED":
                    total_unlocked_resources += 1
            return total_unlocked_resources

        elif option.upper() == "D":
            total_disabled_resources = 0
            # Iterar a lista de recursos à procura dos que se encontram desabilitados
            for lock in self._locks:
                if lock.status('R') == "DISABLED":
                    total_disabled_resources += 1
            return total_disabled_resources
        return "UNKNOWN OPTION"

    def __repr__(self):
        """
        Representação da classe para a saída standard. A string devolvida por
        esta função é usada, por exemplo, se uma instância da classe for
        passada à função print ou str.
        """

        # Acrescentar no output uma linha por cada recurso
        
        return "\n    ".join([repr(lock) for lock in self._locks])

###############################################################################

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
    lockpool = lock_pool(RESOURCES, MAX_RESOURCE_LOCKS, MAX_RESOURCES_LOCKED)
    
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