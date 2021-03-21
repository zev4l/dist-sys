class ListStub:

	def __init__(self):
		self.conn_sock = None

	def connect(self, host, port):
		# código para estabelecer uma ligação,
		# i.i., tornando self.conn_sock válida
		
	def disconnect(self):
		# Fecha a ligação conn_sock

	def append(self, element):
	
	def list(self):

	def clear(self):

	# outros métodos possíveis


class ListSkeleton:

	def __init__(self):
		self.servicoLista = [];

	def processMessage(self, msg_bytes):
		pedido = bytesToList(msg_bytes)

		resposta = []

		if pedido == None or len(pedido) == 0:
			resposta.append('INVALID MESSAGE')
		else:
			if pedido[0] == 'append' and len(pedido) > 1:
				self.servicoLista.append(msg_bytes[1])
				resposta.append('OK')
			elif pedido[0] == 'list':
				resposta.append(str(self.servicoLista))
			elif pedido[0] == 'clear':
				self.servicoLista = []
				resposta.append('OK')
			else:
				resposta.append('INVALID MESSAGE')
		
		return listToBytes(resposta)

	#fim do método processMessage
	#outros métodos possíveis
