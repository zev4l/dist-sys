Aplicações Distribuídas - Projeto 2
Grupo 77


Augusto Gouveia - 55371
José Almeida - 55373

Funcionalidades:

[lock_server.py]

• Utilização: lock_server [IP/Hostname] [Port] [Nr. Recursos] [Max bloqueios por recurso] [Max recursos bloqueados simultaneamente]

• Melhoramentos do Projeto 1 para o Projeto 2:
    
    ○ Respostas passam a ser serializadas.

    ○ Implementação de multiplexação de objetos de IO, através do método select.
    
    ○ Reformatação da resposta do servidor:
        - Resposta elaborada com o formato de uma lista, constituída pelo código da operação e do estado da mesma.
        - Substituição das respostas "OK", "NOK" e "UNKNOWN RESOURCE" por True, False e None, respetivamente.
        - Substituição do estado "DISABLED" pelo objeto literal Ellipsis.

    ○ Reorganização do código com a implementação de um skeleton, de modo a seguir o modelo de comunicação baseado em RPC.
    
• Implementação de novas mensagens de estado:
    ○ Ao conectarem-se novos utilizadores, aparecerão mensagens de estado o indicam, mencionando o endereço e porta do
      respectivo utilizador.
    ○ O mesmo acontecerá para utilizadores que se desconectarem.
    ○ Juntamente com ambos estes tipos de mensagens, será também referenciado o número de utilizadores conectados no momento.

[lock_client.py]

• Utilização: lock_client [-c] [-r] [ID do cliente] [IP/Hostname] [Port]

• Melhoramentos do Projeto 1 para o Projeto 2:
    
    ○ Pedidos passam a ser serializados.
   
    ○ Reformatação do pedido ao servidor:
        - Resposta elaborada com o formato de uma lista, constituída pelo código da operação e pelos parâmetros requisitados pela mesma.

    ○ Reorganização do código com a implementação de um stub, de modo a seguir o modelo de comunicação baseado em RPC.

• Implementação de duas novas opções ao comando.
    
    ○ [-c] : Modo colorless. O output não contém quaisquer cores.

    ○ [-r] : Modo readable. Os estados retornados pelo servidor (True, False, None, Ellipsis) são substituídos pelos estados 
             (OK, NOK, UNKNOWN RESOURCE e DISABLED) respetivamente, de modo a facilitar a compreensão dos comandos ao cliente. 
