"""
Aplicações distribuídas - Projeto 2 - lock_pool.py
Grupo: 77
Números de aluno: 55373, 55371
"""

import time

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
        time_limit segundos. Retorna True, False ou None.
        """
        if resource_id >= 0 and resource_id < (len(self._locks)): # Se o recurso que pretende bloquear existe na pool

            # Se o recurso ainda não atingiu o máximo de bloqueios && 
            # o total de recursos bloqueados não excedem o máximo de recursos bloqueados
            if self.status('K', resource_id) < self._max_lock_counter and self.stats('Y') < self._max_locked_resources:    
                if self.status('R', resource_id) != Ellipsis: # Se o recurso não se encontra desabilitado
                    resource = self._locks[resource_id]

                    # O resultado desta função depende da conclusão da função do recurso
                    return resource.lock(client_id, time_limit)
            return False
        return None
                
    def unlock(self, resource_id, client_id):
        """
        Liberta o bloqueio sobre o recurso resource_id pelo cliente client_id.
        Retorna True, False ou None.
        """
        if resource_id >= 0 and resource_id < (len(self._locks)): # Se o recurso que pretende desbloquear existe na pool
            if self.status('R', resource_id) != "UNLOCKED" and self.status('R', resource_id) != Ellipsis: # Se o recurso está bloqueado
                resource = self._locks[resource_id]
                
                # O resultado desta função depende da conclusão da função do recurso
                return resource.unlock(client_id)
            return False
        return None

    def status(self, option, resource_id):
        """
        Obtém o estado de um recurso. Se option for R, retorna LOCKED, UNLOCKED,
        Ellipsis ou None. Se option for K, retorna <número de 
        bloqueios feitos no recurso> ou None.
        """
        if resource_id >= 0 and resource_id < (len(self._locks)): # Se o recurso que pretende consultar existe na pool
            resource = self._locks[resource_id]
            
            # O resultado desta função depende da conclusão da função do recurso
            return resource.status(option)
        return None

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
                if lock.status('R') == Ellipsis:
                    total_disabled_resources += 1
            return total_disabled_resources
        return None

    def __repr__(self):
        """
        Representação da classe para a saída standard. A string devolvida por
        esta função é usada, por exemplo, se uma instância da classe for
        passada à função print ou str.
        """

        # Acrescentar no output uma linha por cada recurso
        
        return "\n".join([repr(lock) for lock in self._locks])

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
        segundos, alterando os valores associados ao bloqueio. Retorna True ou False.
        """

        # Caso o recurso se encontre desbloqueado, o mesmo passa a estar bloqueado
        if self._state == "UNLOCKED": 
            self._state = "LOCKED"
            self._lock_client_id = client_id
            self._lock_counter += 1
            self._lock_timer = time.time() + time_limit
            return True
            
        # Caso o recurso se encontre bloqueado && o cliente que esteja
        # a tentar bloquear o recurso seja o dono do bloqueio atual, 
        # o tempo de bloqueio é estendido    
        elif self._state == "LOCKED": 
            if self._lock_client_id == client_id: 
                self._lock_timer = time.time() + time_limit
                self._lock_counter += 1
                return True
        return False

    def release(self):
        """
        Liberta o recurso incondicionalmente, alterando
        os valores associados ao bloqueio.
        """
        self._state = "UNLOCKED"

    def unlock(self, client_id):
        """
        Liberta o recurso se este está bloqueado pelo cliente client_id.
        Retorna True ou False.
        """
        # Caso o cliente que esteja a tentar desbloquear o recurso 
        # seja o mesmo que o bloqueou, o recurso é desbloqueado 
        if self._lock_client_id == client_id: 
            self.release()
            return True
        return False

    def status(self, option):
        """
        Obtém o estado do recurso. Se option for R, retorna LOCKED ou UNLOCKED 
        ou Ellipsis. Se option for K, retorna <número de bloqueios feitos no 
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
        self._state = Ellipsis

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
