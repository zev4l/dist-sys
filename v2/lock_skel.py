"""
Aplicações distribuídas - Projeto 2 - lock_skel.py
Grupo: 77
Números de aluno: 55373, 55371
"""

import pickle
import struct
import lock_pool as lp
import time

class skel:

    def __init__(self, N, K, Y):
        self._lockpool = lp.lock_pool(N, K, Y)

    def translate(self, content):
        content = content.copy()

        element = 0
        while element < len(content):
            if content[element] == "OK":
                content[element] = True
            
            elif content[element] == "NOK":
                content[element] = False

            elif content[element] == "UNKNOWN RESOURCE":
                content[element] = None

            elif content[element] == "DISABLED":
                content[element] = Ellipsis
        
        return content

    # Auxiliary Functions

    def compact(self, content):
        reply_bytes = pickle.dumps(content, -1)
        size_bytes = struct.pack('i',len(reply_bytes))
        return size_bytes, reply_bytes


    def processMessage(self, msg_bytes):
        # pedido = bytesToList(msg_bytes)
        pedido = pickle.loads(msg_bytes)

        response = []

        # Remoção de bloqueios expirados/desabilitação de recursos
        self._lockpool.clear_expired_locks()

        if pedido[0] == 10:
            # Caso o comando seja "LOCK", são passados como argumentos ao comando interno
            # o ID do recurso, o tempo limite desejado e o ID do cliente
            response.append(11)
            r_id = int(pedido[1])
            time_limit = int(pedido[2])
            c_id = int(pedido[3])

            # A resposta ao cliente depende da conclusão do comando pretendido
            response.append(self._lockpool.lock(r_id, c_id, time_limit))

        elif pedido[0] == 20:
            # Caso o comando seja "UNLOCK", são passados como argumentos ao comando interno
            # o ID do recurso e o ID do cliente
            response.append(21)
            r_id = int(pedido[1])
            c_id = int(pedido[2])

            # A resposta ao cliente depende da conclusão do comando pretendido
            response.append(self._lockpool.unlock(r_id, c_id))


        elif pedido[0] in [30, 40]:
            # Caso o comando seja "STATUS", são passados como argumentos ao comando interno
            # a opção pretendida e o ID do cliente
            response.append(pedido[0] + 1)
            option = {30: "R",
                      40: "K"}
            r_id = int(pedido[1])

            # A resposta ao cliente depende da conclusão do comando pretendido
            response.append(self._lockpool.status(option[pedido[0]], r_id))

        elif pedido[0] in [50, 60, 70]:
            # Caso o comando seja "STATS", é passado como argumento ao comando interno
            # a opção pretendida
            response.append(pedido[0] + 1)
            option = {50:"Y",
                      60:"N",
                      70:"D"}

            # A resposta ao cliente depende da conclusão do comando pretendido
            response.append(self._lockpool.stats(option[pedido[0]]))

        elif pedido[0] == 80:
            # Caso o comando seja "PRINT", é enviada como response o epoch atual
            # e o estado de cada recurso
            response.append(81)
            reply = f"Current Epoch: {int(time.time())}\n    "
            reply += repr(self._lockpool)
            response.append(reply)





            # # Caso o comando seja "PRINT", é feita uma colorização ao estado de cada recurso
            # if command == "PRINT":
            #     reply = cu.color(reply, "PRINT")
            # else:
            #     reply = cu.color(reply)

            # print(f'Received: \n    {msg}')
            # print("Sent: " + "\n    " + reply + "\n")

        return self.compact(response)


