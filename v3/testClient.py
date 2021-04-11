import requests
import json

# Check reference client on how to use requests module to query the REST server

# For argument checking and all the rest, rip it from the v2 client


#### TEST LINES

# TESTES UTILIZADORES

# CREATE

# names = ["Rudy",
# "Amos",
# "Alfredo",
# "Everette",
# "Rogelio",
# "Zane",
# "Caleb",
# "Cyrus",
# "Reed",
# "Lenard",
# "Lucas",
# "Roberto",
# "Art",
# "Parker",
# "Geoffrey"]
# for name in names:
#     utilizador = {'nome': f"{name}", 'senha': "31231231"}
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
#            {"id_spotify":"3Gm5F95VdRxW3mqCn8RPBJ", "nome":"Aminé"},
#            {"id_spotify":"699OTQXzgjhIYAHMy9RyPD", "nome":"Playboy Carti"},
#            {"id_spotify":"0WgyCbru4tXnMsbTmX4mFw", "nome":"Atlanta Rythm Section"},
#            {"id_spotify":"4tZwfgrHOc3mvqYlEYSvVi", "nome":"Daft Punk"},
#            {"id_spotify":"0ndWKGm6Kl92RMNKdEsco1", "nome":"Exodia"}]
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
# albuns = [{"id_spotify":"78bpIziExqiI9qztvNFlQu", "nome":"AM", "id_artista":1},
#           {"id_spotify":"3lajefIuUk4SfzqVBSJy8p", "nome":"Good For You", "id_artista":2},
#           {"id_spotify":"493HYe7N5pleudEZRyhE7R", "nome":"All I Want Is You", "id_artista":4},
#           {"id_spotify":"3mH6qwIy9crq0I9YQbOuDf", "nome":"Blonde", "id_artista":5}]
# for album in albuns:
#     r = requests.post('http://localhost:5000/albuns', json = album)
#     print(r.status_code)
#     print("***")
# album = {"id_spotify":"5Y04ylQjDWsawOUJXzY4YO", "nome":"The Powers That B", "id_artista":2}
# r = requests.post('http://localhost:5000/albuns', json = album)
# print(r.status_code)
# print("***")
# #
# #
# # # # AVALIACOES
# aval = [{"id_user":1, "id_album":1, "id_avaliacao":5},
#         {"id_user":2, "id_album":4, "id_avaliacao":4},
#         {"id_user":3, "id_album":1, "id_avaliacao":3},
#         {"id_user":4, "id_album":2, "id_avaliacao":2},
#         {"id_user":5, "id_album":3, "id_avaliacao":4}]
#
# for elem in aval:
#     r = requests.post('http://localhost:5000/albuns/avaliacoes', json = elem)
#     print(r.status_code)
#     print("***")

# DELETE
# r = requests.delete("http://localhost:5000/albuns/1")
# print(r.status_code)
# print("***")

# r = requests.delete("http://localhost:5000/albuns/avaliacoes/4")
# print(r.status_code)
# print("***")

# UPDATE

# update = {"id_album":2, "id_user":4, "id_avaliacao":5}
# r = requests.put("http://localhost:5000/albuns/avaliacoes", json=update)
# print(r.status_code)
# print("***")

def rebuild_db():
    names = ["Rudy",
    "Amos",
    "Alfredo",
    "Everette",
    "Rogelio",
    "Zane",
    "Caleb",
    "Cyrus",
    "Reed",
    "Lenard",
    "Lucas",
    "Roberto",
    "Art",
    "Parker",
    "Geoffrey"]
    for name in names:
        utilizador = {'nome': f"{name}", 'senha': "31231231"}
        r = requests.post('http://localhost:5000/utilizadores', json = utilizador)
        print(r.status_code)
        print('***')

    artistas =[{"id_spotify":"7Ln80lUS6He07XvHI8qqHH"},
               {"id_spotify":"3Gm5F95VdRxW3mqCn8RPBJ"},
               {"id_spotify":"699OTQXzgjhIYAHMy9RyPD"},
               {"id_spotify":"0WgyCbru4tXnMsbTmX4mFw"},
               {"id_spotify":"4tZwfgrHOc3mvqYlEYSvVi"},
               {"id_spotify":"0ndWKGm6Kl92RMNKdEsco1"}]

    for artista in artistas:
        r = requests.post("http://localhost:5000/artistas", json = artista)
        print(r.status_code)
        print("***")


    albuns = [{"id_spotify":"78bpIziExqiI9qztvNFlQu"},
              {"id_spotify":"3lajefIuUk4SfzqVBSJy8p"},
              {"id_spotify":"493HYe7N5pleudEZRyhE7R"},
              {"id_spotify":"3mH6qwIy9crq0I9YQbOuDf"}]

    for album in albuns:
        r = requests.post('http://localhost:5000/albuns', json = album)
        print(r.status_code)
        print("***")

    aval = [{"id_user":1, "id_album":1, "id_avaliacao":5},
            {"id_user":2, "id_album":4, "id_avaliacao":4},
            {"id_user":3, "id_album":1, "id_avaliacao":3},
            {"id_user":4, "id_album":2, "id_avaliacao":2},
            {"id_user":5, "id_album":3, "id_avaliacao":4}]

    for elem in aval:
        r = requests.post('http://localhost:5000/albuns/avaliacoes', json = elem)
        print(r.status_code)
        print("***")

def test():





    # READ ALL

    r = requests.get('http://localhost:5000/utilizadores')
    print(r.json())
    print(r.status_code)
    print('***')

    r = requests.get('http://localhost:5000/utilizadores/5')
    print(r.json())
    print(r.status_code)
    print('***')


    # DELETE

    r = requests.delete('http://localhost:5000/utilizadores')
    print(r.status_code)
    print('***')


    ####

    # UPDATE
    #
    utilizador = {'senha': 'TESTE123123123'}
    r = requests.put('http://localhost:5000/utilizadores/6', json = utilizador)
    print(r.status_code)
    print('***')


    # Artistas

    r = requests.get('http://localhost:5000/artistas')
    print(r.json())
    print(r.status_code)
    print('***')

    r = requests.get('http://localhost:5000/artistas/5')
    print(r.json())
    print(r.status_code)
    print('***')

    r = requests.delete('http://localhost:5000/artistas/5')
    print(r.status_code)
    print('***')

    r = requests.delete('http://localhost:5000/artistas')
    print(r.status_code)
    print('***')

    # Albuns

    r = requests.get('http://localhost:5000/albuns')
    print(r.json())
    print(r.status_code)
    print('***')

    r = requests.get('http://localhost:5000/albuns/5')
    print(r.json())
    print(r.status_code)
    print('***')


    r = requests.delete("http://localhost:5000/albuns/1")
    print(r.status_code)
    print("***")

    r = requests.delete("http://localhost:5000/albuns")
    print(r.status_code)
    print("***")

    # Avaliacoes

    update = {"id_album":2, "id_user":4, "id_avaliacao":5}
    r = requests.put("http://localhost:5000/albuns/avaliacoes", json=update)
    print(r.status_code)
    print("***")

def rebuild_db():
    # TESTES UTILIZADORES

    # CREATE

    names = ["Rudy",
    "Amos",
    "Alfredo",
    "Everette",
    "Rogelio",
    "Zane",
    "Caleb",
    "Cyrus",
    "Reed",
    "Lenard",
    "Lucas",
    "Roberto",
    "Art",
    "Parker",
    "Geoffrey"]
    for name in names:
        utilizador = {'nome': f"{name}", 'senha': "31231231"}
        r = requests.post('http://localhost:5000/utilizadores', json = utilizador)
        print(r.status_code)
        print('***')

    ####



    # TESTES ARTISTAS

    # CREATE
    artistas =[{"id_spotify":"7Ln80lUS6He07XvHI8qqHH", "nome":"Arctic Monkeys"},
               {"id_spotify":"3Gm5F95VdRxW3mqCn8RPBJ", "nome":"Aminé"},
               {"id_spotify":"699OTQXzgjhIYAHMy9RyPD", "nome":"Playboy Carti"},
               {"id_spotify":"0WgyCbru4tXnMsbTmX4mFw", "nome":"Atlanta Rythm Section"},
               {"id_spotify":"4tZwfgrHOc3mvqYlEYSvVi", "nome":"Daft Punk"},
               {"id_spotify":"0ndWKGm6Kl92RMNKdEsco1", "nome":"Exodia"}]

    for artista in artistas:
        r = requests.post("http://localhost:5000/artistas", json = artista)
        print(r.status_code)
        print("***")



    # TESTES ALBUNS
    # INSERT
    # ###
    albuns = [{"id_spotify":"78bpIziExqiI9qztvNFlQu", "nome":"AM", "id_artista":1},
              {"id_spotify":"3lajefIuUk4SfzqVBSJy8p", "nome":"Good For You", "id_artista":2},
              {"id_spotify":"493HYe7N5pleudEZRyhE7R", "nome":"All I Want Is You", "id_artista":4},
              {"id_spotify":"3mH6qwIy9crq0I9YQbOuDf", "nome":"Blonde", "id_artista":5}]
    for album in albuns:
        r = requests.post('http://localhost:5000/albuns', json = album)
        print(r.status_code)
        print("***")
    album = {"id_spotify":"5Y04ylQjDWsawOUJXzY4YO", "nome":"The Powers That B", "id_artista":2}
    r = requests.post('http://localhost:5000/albuns', json = album)
    print(r.status_code)
    print("***")
    #
    #
    # # # # AVALIACOES
    aval = [{"id_user":1, "id_album":1, "id_avaliacao":5},
            {"id_user":2, "id_album":4, "id_avaliacao":4},
            {"id_user":3, "id_album":1, "id_avaliacao":3},
            {"id_user":4, "id_album":2, "id_avaliacao":2},
            {"id_user":5, "id_album":3, "id_avaliacao":4}]

    for elem in aval:
        r = requests.post('http://localhost:5000/albuns/avaliacoes', json = elem)
        print(r.status_code)
        print("***")
# rebuild_db()
# test()

# rebuild_db()
# album = {"id_spotify":"78bpIziExqiI9qztvNFlQu"}
# r = requests.post("http://localhost:5000/albuns", json=album)
# print(r.status_code)
# print(r.json())
# print("***")

# review = {"id_user":5, "id_album":3, "id_avaliacao":4}
# r = requests.post("http://localhost:5000/albuns/avaliacoes", json=review)
# print(r.status_code)
# print(r.json())
# print("***")

r = requests.delete("http://localhost:5000/albuns/utilizadores/5")
print(r.status_code)
print(r.json())
print("***")

#
