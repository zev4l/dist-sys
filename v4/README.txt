Aplicações Distribuídas - Projeto 4
Grupo 77

Augusto Gouveia - 55371
José Almeida - 55373

Funcionalidades:

[server.py]

• Utilização: server

• Serviço Web com um API REST para gerir um sistema simplificado de classificação de álbuns de música de utilizadores,
  com a capacidade de interrogar o API REST do Spotify sobre mais informações em relação a um álbum/artista em particular.

• Verificação de autenticidade do cliente fazendo uso do protocolo SSL/TLS garantindo comunicação confidencial (cifrada).

• Utilização do protocolo OAuth2 (integradamente com o Flask) para obtenção da autorização requerida pelo REST API do Spotify.

• Redirecionamento do utilizador para /login quando este tenta aceder aos recursos /artistas e /albuns antes de fazer login (i.e antes de ter um token valido).

• Código detalhadamente documentado.


[client.py]

• Utilização: client [-c] [IP/Hostname] [Port]

• Funcionamento: Para utilizar qualquer comando de acesso ao servidor, é necessário estar autenticado no Spotify.
  Na primeira utilização, deve obter o token através do login em https://localhost:5000/login . O token é obtido e guardado localmente.
  De seguida, pode utilizar qualquer comando de acesso ao servidor (HELP para obter a lista de comandos disponíveis).

• Extra modo adicionado:
	- Colorless (-c), cujo desativa a funcionalidade das cores.

• Extra comandos adicionados:
	- HELP, cujo apresenta os comandos disponíveis e a sua respetiva sintaxe
	- CLEAR, cujo limpa o histórico de comandos

• Verificação de autenticidade do servidor fazendo uso do protocolo SSL/TLS garantindo comunicação confidencial (cifrada).

• Comunicação com o servidor através do módulo requests (com devida autenticação).

• Interface de pedido de comandos informa ao utilizador qual o host ao qual está a enviar comandos.

• Leitura de comandos através de stdin.

• Programação defensiva que permite que o programa não falhe quando um comando é introduzido incorretamente.
Inclui também feedback sobre o erro/exceção, ajudando o utilizador a corrigir o erro.

• Código detalhadamente documentado.
