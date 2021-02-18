"""
Aplicações distribuídas - Projeto 1 - lock_server.py
Grupo: 07
Números de aluno: 55373, 55371
"""

import socket as s

# TODO: DOCUMENT EVERYTHING

def create_tcp_server_socket(address, port, queue_size):
    
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)

    # If you're having problems you might wanna comment this out 
    sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
    sock.bind((address, port))
    sock.listen(queue_size)

    return sock

def create_tcp_client_socket():
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    return sock

def receive_all(socket, length):
    # TODO: FIX THIS ON FRIDAY
    
    try:
        socket.settimeout(30)
        received_data = socket.recv(length)

        return received_data
        
    except s.timeout:
        print("CONNECTION TIMED OUT")

    
    

listener_socket = create_tcp_server_socket
client_socket = create_tcp_client_socket
dados_recebidos = receive_all
