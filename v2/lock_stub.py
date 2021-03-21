"""
Aplicações distribuídas - Projeto 2 - lock_stub.py
Grupo: 77
Números de aluno: 55373, 55371
"""

#TODO: Comment EVERYTHING

import pickle
import net_client as nc
import struct


class stub:
    def __init__(self, address, port):
        self._server = nc.server(address, port)
        self.connect()

    def connect(self):
        self._server.connect()

    def close(self):
        self._server.close()

    # Commands:

    def lock(self, resource_number, time_limit, ID):
        request = [10, resource_number, time_limit, ID]

        return self._processRequest(request)
        
    def unlock(self, resource_number, ID):
        request = [20, resource_number, ID]

        return self._processRequest(request)


    def status(self, option, resource_number):
        codes = {"R":30, "K":40}
        request = [codes[option], resource_number]

        return self._processRequest(request)


    def stats(self, option):
        codes = {"Y":50, "N":60, "D":70}
        request = [codes[option]]

        return self._processRequest(request)


    def print(self):
        request = [80]

        return self._processRequest(request)


    # Auxilliary Functions

    def compact(self, content):
        request_bytes = pickle.dumps(content, -1)
        size_bytes = struct.pack('i',len(request_bytes))
        return size_bytes, request_bytes

    def _processRequest(self, request):
        # Compactar e enviar pedido

        size_bytes, request_bytes = self.compact(request)

        self._server.send(size_bytes)
        self._server.send(request_bytes)

        # Receber resposta e descompactar

        size_bytes = self._server.recv(4)
        size_bytes = struct.unpack('i',size_bytes)[0]
        response_bytes = self._server.receive_all(size_bytes)

        response = pickle.loads(response_bytes)

        return response

    # Auxiliary Functions




    

