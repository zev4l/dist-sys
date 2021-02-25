import socket as s
import sock_utils as su
import sys
 
# total arguments
args = sys.argv

try:
        
    HOST = str(args[1]) #pode ser vazio, localhost ou 127.0.0.1
    PORT = int(args[2])
except:
    print("Utilização: server.py <IPv4 endereço> <int porto>")
    sys.exit(1)

sock = su.client_socket()
sock.connect((HOST, PORT))

while True:
    message = input("Introduza a mensagem a ser enviada: ")
    
    sock.sendall(message.encode("utf-8"))

    resposta = su.dados_recebidos(sock, 1024).decode("utf-8")

    print(f'Recebi: {resposta}')

sock.close()