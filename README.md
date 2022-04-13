<div align="center">
  <a href="https://github.com/zev4l/dist-sys">
    <img src="https://i.ibb.co/jkrgphM/dist2.png" alt="Logo" width="150" height="150">
  </a>
 
  <h3 align="center">dist-sys (g-77)</h3>
  <h5 align="center">Projeto para a cadeira de Aplicações Distribuídas (2020/2021)</h5>
  <h5 align="center">(Projeto em 4 versões)</h5>

  ![Grupo](https://img.shields.io/badge/Grupo-77-green)
  ![Jose](https://img.shields.io/badge/Jos%C3%A9%20Almeida-55373-blue)
  ![Augusto](https://img.shields.io/badge/Augusto%20Gouveia-55371-blue)

</div>

## Funcionalidades:

## Servidor
#### [server.py](./v4/server/server.py)
* Utilização: `server`
* Serviço Web com um API REST para gerir um sistema simplificado de classificação de álbuns de música de utilizadores,
  com a capacidade de interrogar o API REST do Spotify sobre mais informações em relação a um álbum/artista em particular.
* Verificação de autenticidade do cliente fazendo uso do protocolo SSL/TLS garantindo comunicação confidencial (cifrada).
* Utilização do protocolo OAuth2 (integradamente com o Flask) para obtenção da autorização requerida pelo REST API do Spotify.
* Redirecionamento do utilizador para /login quando este tenta aceder aos recursos /artistas e /albuns antes de fazer login (i.e antes de ter um token valido).
* Código detalhadamente documentado.

## Cliente
#### [client.py](./v4/client/client.py)

* Utilização: `client [-c] [IP/Hostname] [Port]`
* Funcionamento: Para utilizar qualquer comando de acesso ao servidor, é necessário estar autenticado no Spotify.
  Na primeira utilização, deve obter o token através do login em https://localhost:5000/login . O token é obtido e guardado localmente.
  De seguida, pode utilizar qualquer comando de acesso ao servidor (`HELP` para obter a lista de comandos disponíveis).
* Extra modo adicionado:
  * Colorless (`-c`), cujo desativa a funcionalidade das cores.
* Extra comandos adicionados:
  * `HELP`, cujo apresenta os comandos disponíveis e a sua respetiva sintaxe
  + `CLEAR`, cujo limpa o histórico de comandos
* Verificação de autenticidade do servidor fazendo uso do protocolo SSL/TLS garantindo comunicação confidencial (cifrada).
* Comunicação com o servidor através do módulo requests (com devida autenticação).
* Interface de pedido de comandos informa ao utilizador qual o _host_ ao qual está a enviar comandos.
* Leitura de comandos através de _stdin_.
* Programação defensiva que permite que o programa não falhe quando um comando é introduzido incorretamente.
Inclui também feedback sobre o erro/exceção, ajudando o utilizador a corrigir o erro.
* Código detalhadamente documentado.


## Notas
* Para questões de teste, deverá ser utilizada a [versão 4](./v4).
* Estão presentes no repositório pares de chaves assimétricas e certificados utilizados apenas como exemplo. Num ambiente de produção, estas chaves já não poderiam ser utilizadas.
