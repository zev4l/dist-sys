# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - net_client.py
Grupo: 07
Números de aluno: 55373, 55371
"""

# zona para fazer importação

from sock_utils import create_tcp_client_socket

# definição da classe server

class server:
    """
    Abstrai uma ligação a um servidor TCP. Implementa métodos para: estabelecer 
    a ligação; envio de um comando e receção da resposta; terminar a ligação.
    """
    def __init__(self, address, port):
        """
        Inicializa a classe com parâmetros para funcionamento futuro.
        """
        pass # Remover esta linha e fazer implementação da função
        
    def connect(self):
        """
        Estabelece a ligação ao servidor especificado na inicialização.
        """
        pass # Remover esta linha e fazer implementação da função

    def send_receive(self, data):
        """
        Envia os dados contidos em data para a socket da ligação, e retorna
        a resposta recebida pela mesma socket.
        """
        pass # Remover esta linha e fazer implementação da função
    
    def close(self):
        """
        Termina a ligação ao servidor.
        """
        pass # Remover esta linha e fazer implementação da função
