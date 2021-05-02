Aplicações Distribuídas - Projeto 4
Grupo 77

Augusto Gouveia - 55371
José Almeida - 55373

Funcionalidades:

[server.py]

• Utilização: server

• Verificação de autenticidade do cliente fazendo uso do protocolo SSL/TLS garantindo comunicação confidencial (cifrada).

• Utilização do protocolo OAuth2 (integradamente com o Flask) para obtenção da autorização requerida pelo REST API do Spotify.

• Redirecionamento do utilizador para /login quando este tenta aceder aos recursos /artistas e /albuns antes de fazer login (i.e antes de ter um token valido).

• Código detalhadamente documentado.


[client.py]

• Utilização: client [-c] [IP/Hostname] [Port]

• Verificação de autenticidade do servidor fazendo uso do protocolo SSL/TLS garantindo comunicação confidencial (cifrada).

• Extra modo adicionado:
	- Colorless (-c), cujo desativa a funcionalidade das cores.

• Extra comandos adicionados:
	- HELP, cujo apresenta os comandos disponíveis e a sua respetiva sintaxe
	- CLEAR, cujo limpa o histórico de comandos

• Comunicação com o servidor através do módulo requests (com devida autenticação).

• Interface de pedido de comandos informa ao utilizador qual o host ao qual está a enviar comandos.

• Leitura de comandos através de stdin.

• Programação defensiva que permite que o programa não falhe quando um comando é introduzido incorretamente.
Inclui também feedback sobre o erro/exceção, ajudando o utilizador a corrigir o erro.

• Código detalhadamente documentado.
