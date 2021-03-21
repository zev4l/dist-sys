Aplicações Distribuídas - Projeto 2
Grupo 77


Augusto Gouveia - 55371
José Almeida - 55373

Funcionalidades:

[lock_server.py]

• Utilização: lock_server [IP/Hostname] [Port] [Nr. Recursos] [Max bloqueios por recurso] [Max recursos bloqueados simultaneamente]

• Realçamento de mensagens de sucesso a verde e dos erros a vermelho, incluindo outros detalhes esteticamente destacados.

• Código detalhadamente documentado.

• Processamento seguro do sinal SIGINT: ao ser recebido o sinal SIGINT, é primeiro encerrada a socket
para que o servidor termine o processo corretamente. 

[lock_client.py]

• Utilização: lock_client [ID do cliente] [IP/Hostname] [Port] 

• Extra comando adicionado: HELP, cujo apresenta os comandos disponíveis e a sua respetiva sintaxe

• Interface de pedido de comandos informa ao utilizador qual é o seu ID de cliente, bem como o host ao qual está a enviar comandos.

• Leitura de comandos através de stdin.

• Realçamento de mensagens de sucesso a verde e dos erros a vermelho, incluindo outros detalhes esteticamente destacados.

• Programação defensiva que permite que o programa não falhe quando um comando é introduzido incorretamente.
Inclui também feedback sobre o erro/exceção, ajudando o utilizador a corrigir o erro.

• Código detalhadamente documentado.