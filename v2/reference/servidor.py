import sys, socket as s
import select as sel

HOST = ''

if len(sys.argv) > 1:
    
    PORT = int(sys.argv[1])
    
else:
    PORT = 9999
    
sock = s.socket(s.AF_INET, s.SOCK_STREAM)
sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)

sock.bind((HOST, PORT))
sock.listen(1)

list = []


SocketList = [sock, sys.stdin]
halt = False

while True and not halt:
    R, W, X = sel.select(SocketList, [], [])
    for sckt in R:
        if sckt is sock:

            (conn_sock, addr) = sock.accept()
            addr, port = conn_sock.getpeername()
            print(f"Novo cliente ligado de:{addr}:{port}")
            SocketList.append(conn_sock)
        
        elif sckt is sys.stdin:



            input = sys.stdin.readline()
            
            if "sair" in input:
                halt = True


        else:
            msg = sckt.recv(1024)
            

            if msg.decode():
                resp = 'Ack'

                if msg.decode() == 'LIST':
                    resp = str(list)
                
                elif msg.decode() == 'CLEAR':
                    list = []
                    resp = "Lista apagada"
                else:
                    list.append(msg.decode())

                sckt.sendall(resp.encode())

                print ('list= %s' % list)

                
            else:
                print ('Cliente fechou a ligação!')
                sckt.close()
                SocketList.remove(conn_sock)


sock.close()