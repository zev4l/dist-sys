import requests
import json

# Check reference client on how to use requests module to query the REST server

# For argument checking and all the rest, rip it from the v2 client


#### TEST LINES

# TESTES UTILIZADORES

# CREATE

#
# for i in range(5):
#     utilizador = {'nome': f"João {i}", 'senha': "AAAAAAAAAAAAA"}
#     r = requests.post('http://localhost:5000/utilizadores', json = utilizador)
#     print(r.status_code)
#     print('***')

####

# DELETE

# r = requests.delete('http://localhost:5000/utilizadores')
# print(r.status_code)
# print('***')

####

# READ ALL

# r = requests.get('http://localhost:5000/utilizadores')
# print(r.json)
# print(r.status_code)
# print('***')

####

# UPDATE
#
# utilizador = {'senha': 'TESTE123123123'}
# r = requests.put('http://localhost:5000/utilizadores/6', json = utilizador)
# print(r.status_code)
# print('***')


# TESTES ARTISTAS

# CREATE
# artistas =[{"id_spotify":"7Ln80lUS6He07XvHI8qqHH", "nome":"Arctic Monkeys"},
#            {"id_spotify":"699OTQXzgjhIYAHMy9RyPD", "nome":" Playboy Carti"},
#            {"id_spotify":"0WgyCbru4tXnMsbTmX4mFw", "nome":"Atlanta Rythm Section"},
#            {"id_spotify":"4tZwfgrHOc3mvqYlEYSvVi", "nome":"Daft Punk"},
#            {"id_spotify":"0ndWKGm6Kl92RMNKdEsco1", "nome":"Exodia"}
#            ]
#
# for artista in artistas:
#     r = requests.post("http://localhost:5000/artistas", json = artista)
#     print(r.status_code)
#     print("***")

# DELETE

# r = requests.delete('http://localhost:5000/artistas')
# print(r.status_code)
# print('***')

# TESTES ALBUNS
# INSERT
# ###
album = {"id_spotify":"78bpIziExqiI9qztvNFlQu", "nome":"AM", "id_artista":"1"}
albumErro = {"id_spotify":"78bpIziExqiI9qztvNFlQu", "nome":"AM", "id_artista":"5123123"}
r = requests.post('http://localhost:5000/albuns', json = album)
print(r.status_code)
print("***")


# # AVALIACOES
# aval = {"id_user":123, "id_album":123, "id_avaliacao":123}
# r = requests.post('http://localhost:5000/albuns/avaliacoes', json = aval)
# print(r.status_code)
# print("***")
