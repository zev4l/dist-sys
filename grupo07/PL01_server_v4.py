import sock_utils as su
import sys
from pprint import pprint

# total arguments
args = sys.argv
data = {}
try:
        
    HOST = str(args[1]) #pode ser vazio, localhost ou 127.0.0.1
    PORT = int(args[2])
except:
    print("Utilização: server.py <IPv4 endereço> <int porto>")
    sys.exit(1)

try:
    sock = su.listener_socket(HOST, PORT, 1)
    (conn_sock, (addr, port)) = sock.accept()
    
    while True:
        
        

        print('ligado a %s no porto %s' % (addr,port))

        msg = su.dados_recebidos(conn_sock, 1024).decode("utf-8")
        print(f'Recebi: {msg}')
        

        parsed_msg = msg.split()

        if ("GET" in msg.upper() and len(parsed_msg) == 2 and parsed_msg[1].isdigit()) or ("LIST" in msg.upper() and len(parsed_msg) == 1):
            queryType = parsed_msg[0].upper()
            
            if queryType == "GET":
                value = int(parsed_msg[1])
                if value >= len(data):
                    reply = "Chave Inexistente"
                else:
                    reply = data[value]
            
            if queryType == "LIST":
                if len(data) == 0:
                    reply = "Dicionário Vazio"
                else:
                    reply = ", ".join(data.values())
        else:
            reply = str(len(data))
            data[len(data)] = msg

        

        conn_sock.sendall(reply.encode("utf-8"))
        print("Enviei:", reply)

    sock.close()



except KeyboardInterrupt as e:
    print("\n")
    pprint(data)
    sock.close()

#conn_sock.sendall(bytes('Aqui vai a resposta', encoding="utf-8"))

