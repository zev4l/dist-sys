"""
Aplicações distribuídas - Projeto 1 - net_client.py
Grupo: 77
Números de aluno: 55373, 55371
"""

# zona para fazer importação

from sock_utils import client_socket, receive_all

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
        self._address = address
        self._port = port

        self._sock = client_socket()
        
    def connect(self):
        """
        Estabelece a ligação ao servidor especificado na inicialização.
        """
        self._sock.connect((self._address, self._port))

    def send_receive(self, data):
        """
        Envia os dados contidos em data para a socket da ligação, e retorna
        a resposta recebida pela mesma socket.
        """
        self._sock.sendall(data)
        
        return receive_all(self._sock, 1024)
    
    def close(self):
        """
        Termina a ligação ao servidor.
        """
        self._sock.close()
