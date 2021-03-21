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

        # Obtenção do pedido do cliente
        request = pickle.loads(msg_bytes)

        # Criação da lista da resposta
        response = []

        # Remoção de bloqueios expirados/desabilitação de recursos
        self._lockpool.clear_expired_locks()

        if request[0] == 10:
            # Caso o comando seja "LOCK" (10), são passados como argumentos ao comando interno
            # o ID do recurso, o tempo limite desejado e o ID do cliente
            response.append(11)
            r_id = int(request[1])
            time_limit = int(request[2])
            c_id = int(request[3])

            # A resposta ao cliente depende da conclusão do comando pretendido
            response.append(self._lockpool.lock(r_id, c_id, time_limit))

        elif request[0] == 20:
            # Caso o comando seja "UNLOCK" (20), são passados como argumentos ao comando interno
            # o ID do recurso e o ID do cliente
            response.append(21)
            r_id = int(request[1])
            c_id = int(request[2])

            # A resposta ao cliente depende da conclusão do comando pretendido
            response.append(self._lockpool.unlock(r_id, c_id))


        elif request[0] in [30, 40]:
            # Caso o comando seja "STATUS" (30 = STATUS R, 40 = STATUS K), são passados 
            # como argumentos ao comando interno a opção pretendida e o ID do cliente
            response.append(request[0] + 1)
            option = {30: "R",
                      40: "K"}
            r_id = int(request[1])

            # A resposta ao cliente depende da conclusão do comando pretendido
            response.append(self._lockpool.status(option[request[0]], r_id))

        elif request[0] in [50, 60, 70]:
            # Caso o comando seja "STATS" (50 = STATS Y, 60 = STATS N, 70 = STATS D), 
            # é passado como argumento ao comando interno a opção pretendida
            response.append(request[0] + 1)

            option = {50:"Y",
                      60:"N",
                      70:"D"}

            # A resposta ao cliente depende da conclusão do comando pretendido
            response.append(self._lockpool.stats(option[request[0]]))

        elif request[0] == 80:
            # Caso o comando seja "PRINT" (80), é enviada como response o epoch atual
            # e o estado de cada recurso
            response.append(81)
            response.append(repr(self._lockpool))

        print(f'Received: \n    {str(request)}')
        print("Sent: " + "\n    " + str(response) + "\n")

        return self.compact(response)


