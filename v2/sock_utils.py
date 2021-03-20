"""
Aplicações distribuídas - Projeto 1 - sock_utils.py
Grupo: 77
Números de aluno: 55373, 55371
"""

import socket as s

def create_tcp_server_socket(address, port, queue_size):
    """
    Cria uma socket de servidor.
    Requires: address e port são válidos. queue_size é um inteiro.
    Ensures: retorno de uma socket de servidor anexada ao endereço e porta
    referidos.
    """
    
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
    sock.bind((address, port))
    sock.listen(queue_size)

    return sock

def create_tcp_client_socket():
    """
    Cria uma socket de cliente.
    Ensures: retorno de uma socket de cliente.
    
    """
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    return sock

def receive_all(socket, length):
    """
    Recebe a length especificada de dados através da socket especificada.
    Requires: socket é uma socket, length é um inteiro.
    Ensures: devolve dados obtidos através da socket.
    """
    
    try:
        socket.settimeout(30)
        received_data = socket.recv(length)

        return received_data
        
    except s.timeout:
        print("CONNECTION TIMED OUT")

    
    

listener_socket = create_tcp_server_socket
client_socket = create_tcp_client_socket
dados_recebidos = receive_all
