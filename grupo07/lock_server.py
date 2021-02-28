#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - lock_server.py
Grupo: 07
Números de aluno: 55373, 55371
"""

# Zona para fazer importação

import time
import sys
import sock_utils as su
import color_utils as cu

## TODO: Implement clear console
## TODO: GREEN OK RED NOK E POR CORES EM TUDO XDDDDDDDDDDDDD

###############################################################################


class resource_lock:
    def __init__(self, resource_id):
        """
        Define e inicializa as características de um LOCK num recurso.
        """
        self._resource_id = resource_id
        self._state = "UNLOCKED"
        self._lock_client_id = -1
        self._lock_timer = time.time()
        self._lock_counter = 0

    def lock(self, client_id, time_limit):
        """
        Tenta bloquear o recurso pelo cliente client_id, durante time_limit 
        segundos. Retorna OK ou NOK.
        """
        if self._state == "UNLOCKED":
            self._state = "LOCKED"
            self._lock_client_id = client_id
            self._lock_counter += 1
            self._lock_timer = time.time() + time_limit
            return "OK"
        elif self._state == "LOCKED":
            if self._lock_client_id == client_id:
                self._lock_timer = time.time() + time_limit
                self._lock_counter += 1
                return "OK"
        return "NOK"

    def release(self):
        """
        Liberta o recurso incondicionalmente, alterando os valores associados
        ao bloqueio.
        """
        self._state = "UNLOCKED"
        # self._lock_timer = time.time()

    def unlock(self, client_id):
        """
        Liberta o recurso se este está bloqueado pelo cliente client_id.
        Retorna OK ou NOK.
        """
        if self._lock_client_id == client_id:
            self.release()
            return "OK"
        return "NOK"

    def status(self, option):
        """
        Obtém o estado do recurso. Se option for R, retorna LOCKED ou UNLOCKED 
        ou DISABLED. Se option for K, retorna <número de bloqueios feitos no 
        recurso>.
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
    def __init__(self, N, K, Y):
        """
        Define um array com um conjunto de locks para N recursos. Os locks podem
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
            if i.status('R') == "LOCKED" and time.time() > i.status('T'):
                i.release()
                if i.status('K') == self._max_lock_counter:
                    i.disable()


    def lock(self, resource_id, client_id, time_limit):
        """
        Tenta bloquear o recurso resource_id pelo cliente client_id, durante
        time_limit segundos. Retorna OK, NOK ou UNKNOWN RESOURCE.
        """
        # resource = self._locks[resource_id]
        if resource_id >= 0 and resource_id < (len(self._locks)):
            if self.status('K', resource_id) < self._max_lock_counter and self.stats('Y') < self._max_locked_resources:
                if self.status('R', resource_id) != "DISABLED":
                    return self._locks[resource_id].lock(client_id, time_limit)
            return "NOK"
        return "UNKNOWN RESOURCE"
                

    def unlock(self, resource_id, client_id):
        """
        Liberta o bloqueio sobre o recurso resource_id pelo cliente client_id.
        Retorna OK, NOK ou UNKNOWN RESOURCE.
        """
        if resource_id >= 0 and resource_id < (len(self._locks)):
            if self.status('R', resource_id) != "UNLOCKED" and self.status('R', resource_id) != "DISABLED":
                return self._locks[resource_id].unlock(client_id)
            return "NOK"
        return "UNKNOWN RESOURCE"

    def status(self, option, resource_id):
        """
        Obtém o estado de um recurso. Se option for R, retorna LOCKED, UNLOCKED,
        DISABLED ou UNKNOWN RESOURCE. Se option for K, retorna <número de 
        bloqueios feitos no recurso> ou UNKNOWN RESOURCE.
        """
        if resource_id >= 0 and resource_id < (len(self._locks)):
            return self._locks[resource_id].status(option)
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
            for lock in self._locks:
                if lock.status('R') == 'LOCKED':
                    total_locked_resources += 1
            return total_locked_resources

            # return len([lock for lock in self._locks if lock.status('R') == 'LOCKED'])
        
        elif option.upper() == "N":
            total_unlocked_resources = 0
            for lock in self._locks:
                if lock.status('R') == "UNLOCKED":
                    total_unlocked_resources += 1
            return total_unlocked_resources

        elif option.upper() == "D":
            total_disabled_resources = 0
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

PARAMETER_ERROR = "Verifique os parâmetros.\nUtilização: lock_server.py <IP/Hostname> <Porto> <Nº de Recursos> <Nº de Bloqueios Permitidos> <Max. de Recursos Bloqueados Simultaneamente"
NETWORK_ERROR = "Host/Port inválidos ou outro problema de ligação."
SEPARATOR = "———————————————————————————————————————"

args = sys.argv[1:]

if len(args) != 5:
    print(PARAMETER_ERROR)
    sys.exit()

# Verificação de argumentos

try:
    
    HOST = str(args[0])
    PORT = int(args[1])
    RESOURCES = int(args[2])
    MAX_RESOURCE_LOCKS = int(args[3])
    MAX_RESOURCES_LOCKED = int(args[4])
    

    
except Exception as e:
    print(PARAMETER_ERROR)
    sys.exit(1)

try:
    lockpool = lock_pool(RESOURCES, MAX_RESOURCE_LOCKS, MAX_RESOURCES_LOCKED)
    
    sock = su.listener_socket(HOST, PORT, 1)

    while True:
        
        # TODO - Deal with disabling resources with max locks reached
        
        (conn_sock, (addr, port)) = sock.accept()
        print(SEPARATOR)
        print(cu.colorWrite(f'Connected to {addr} on port {port}\n', 'green'))
        
        lockpool.clear_expired_locks()

        msg = su.receive_all(conn_sock, 1024).decode("utf-8")

        parsed_msg = msg.split()

        command = parsed_msg[0].upper()

        reply = "NOK"

        if command == "LOCK":
            r_id = int(parsed_msg[1])
            time_limit = int(parsed_msg[2])
            c_id = int(parsed_msg[3])
            reply = lockpool.lock(r_id, c_id, time_limit)
        
        elif command == "UNLOCK":
            r_id = int(parsed_msg[1])
            c_id = int(parsed_msg[2])
            reply = lockpool.unlock(r_id, c_id)
        
        elif command == "STATUS":
            option = parsed_msg[1]
            r_id = int(parsed_msg[2])
            reply = lockpool.status(option, r_id)

        elif command == "STATS":
            option = parsed_msg[1]
            reply = lockpool.stats(option)
        
        elif command == "PRINT":
            reply = f"Current Epoch: {int(time.time())}\n    "
            reply += repr(lockpool)

        reply = str(reply)

        conn_sock.sendall(reply.encode("utf-8"))

        if command == "PRINT":
            reply = cu.color(reply, "PRINT")
        else:
            reply = cu.color(reply)

        print(f'Received: \n    {msg}')
        print("Sent: " + "\n    " + reply + "\n")

        # TODO - Close the connection?
        # do you agree with him?
        conn_sock.close()
        
    sock.close()

    
except KeyboardInterrupt as e:
    print("\nReceived SIGINT, stopping.\n") #Received SIGINT
    sock.close()
    sys.exit(1)

except (ConnectionError, OSError):
    print(NETWORK_ERROR)
    sys.exit(1)