#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - lock_server.py
Grupo: 07
Números de aluno: 55373, 55371
"""

# Zona para fazer importação



###############################################################################

class resource_lock:
    def __init__(self, resource_id):
        """
        Define e inicializa as características de um LOCK num recurso.
        """
        pass # Remover esta linha e fazer implementação da função

    def lock(self, client_id, time_limit):
        """
        Tenta bloquear o recurso pelo cliente client_id, durante time_limit 
        segundos. Retorna OK ou NOK.
        """
        pass # Remover esta linha e fazer implementação da função

    def release(self):
        """
        Liberta o recurso incondicionalmente, alterando os valores associados
        ao bloqueio.
        """
        pass # Remover esta linha e fazer implementação da função

    def unlock(self, client_id):
        """
        Liberta o recurso se este está bloqueado pelo cliente client_id.
        Retorna OK ou NOK.
        """
        pass # Remover esta linha e fazer implementação da função

    def status(self, option):
        """
        Obtém o estado do recurso. Se option for R, retorna LOCKED ou UNLOCKED 
        ou DISABLED. Se option for K, retorna <número de bloqueios feitos no 
        recurso>.
        """
        pass # Remover esta linha e fazer implementação da função
   
    def disable(self):
        """
        Coloca o recurso como desabilitdado incondicionalmente, alterando os 
        valores associados à sua disponibilidade.
        """
        pass # Remover esta linha e fazer implementação da função

    def __repr__(self):
        """
        Representação da classe para a saída standard. A string devolvida por
        esta função é usada, por exemplo, se uma instância da classe for
        passada à função print ou str.
        """
        output = ""
        # Se o recurso está bloqueado:
        # R <número do recurso> bloquado <id do cliente> <instante limite da 
        #concessão do bloqueio>
        # Se o recurso está desbloquado:
        # R <número do recurso> desbloqueado
        # Se o recurso está inativo:
        # R <número do recurso> inativo
        return output

###############################################################################

class lock_pool:
    def __init__(self, N, K, Y):
        """
        Define um array com um conjunto de locks para N recursos. Os locks podem
        ser manipulados pelos métodos desta classe. Define K, o número máximo 
        de bloqueios permitidos para cada recurso. Ao atingir K, o recurso fica 
        desabilitdado. Define Y, o número máximo permitido de recursos 
        bloqueados num dado momento. Ao atingir Y, não é possível realizar mais 
        bloqueios até que um recurso seja libertado.
        """
        pass # Remover esta linha e fazer implementação da função
        
    def clear_expired_locks(self):
        """
        Verifica se os recursos que estão bloqueados ainda estão dentro do tempo
        de concessão dos bloqueios. Remove os bloqueios para os quais o tempo de
        concessão tenha expirado.
        """
        pass # Remover esta linha e fazer implementação da função

    def lock(self, resource_id, client_id, time_limit):
        """
        Tenta bloquear o recurso resource_id pelo cliente client_id, durante
        time_limit segundos. Retorna OK, NOK ou UNKNOWN RESOURCE.
        """
        pass # Remover esta linha e fazer implementação da função

    def unlock(self, resource_id, client_id):
        """
        Liberta o bloqueio sobre o recurso resource_id pelo cliente client_id.
        Retorna OK, NOK ou UNKNOWN RESOURCE.
        """
        pass # Remover esta linha e fazer implementação da função

    def status(self, option, resource_id):
        """
        Obtém o estado de um recurso. Se option for R, retorna LOCKED, UNLOCKED,
        DISABLED ou UNKNOWN RESOURCE. Se option for K, retorna <número de 
        bloqueios feitos no recurso> ou UNKNOWN RESOURCE.
        """
        pass # Remover esta linha e fazer implementação da função

    def stats(self, option):
        """
        Obtém o estado do serviço de exclusão mútua. Se option for Y, retorna 
        <número de recursos bloqueados atualmente>. Se option for N, retorna 
        <número de recursos bloqueados atualmente>. Se option for D, retorna 
        <número de recursos desabilitdados>
        """
        pass # Remover esta linha e fazer implementação da função

    def __repr__(self):
        """
        Representação da classe para a saída standard. A string devolvida por
        esta função é usada, por exemplo, se uma instância da classe for
        passada à função print ou str.
        """
        output = ""
        #
        # Acrescentar no output uma linha por cada recurso
        #
        return output

###############################################################################

# código do programa principal
