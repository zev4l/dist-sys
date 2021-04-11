import requests # To interact with Spotify API
import sqlite3
from db import connect_db
from os.path import isfile
from flask import Flask, g, request, make_response, jsonify

CLIENT_ID = "a040271774db4f40b192f953a0872d84"
CLIENT_SECRET = "6460e1db9bd24d3398044e3c96d2a513"

# TODO: remove these imports
import traceback as t
from pprint import pprint

app = Flask(__name__)
DATABASE = "data.db"

# TODO: In every exception include JSON description of error instead of error 500 (Slide 4 TP07)

# TODO: To properly except everything, use "exception.__class__.__name__" to get exception names. Ex: if UNIQUE fails it's an IntegrityError

# TODO: Revise all status codes

# Using Spotify API

def query_spotify(id, type = "artist", keys="all"):
    # Obtaining access token

    AUTH_URL = 'https://accounts.spotify.com/api/token'
    BASE_URL = 'https://api.spotify.com/v1/'

    auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,})

    access_token = auth_response.json()['access_token']

    headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)}

    if type == "artist":

        r = requests.get(BASE_URL + 'artists/' + id, headers=headers)

        data = r.json()

        if keys == "all":

            url = data["external_urls"]["spotify"]
            followers = data["followers"]["total"]
            genres = data["genres"]
            popularity = data["popularity"]

            return {"url_spotify":url,
                    "seguidores":followers,
                    "generos":genres,
                    "popularidade":popularity}
        else:

            return [data[key] for key in keys]

    elif type == "album":

        r = requests.get(BASE_URL + 'albums/' + id, headers=headers)

        data = r.json()

        if keys == "all":


            cover = data["images"][0]["url"]
            url = data["external_urls"]["spotify"]
            label = data["label"]
            tracks = data["total_tracks"]
            release_date = data["release_date"]
            artists = [artist["name"] for artist in data["artists"]]

            return {"capa":cover,
                    "url_spotify":url,
                    "quantidade_faixas":tracks,
                    "data_lancamento":release_date,
                    "artistas":artists}
        else:

            return [data[key] for key in keys]

# Routes...

@app.route('/utilizadores', methods = ['POST', 'GET', 'DELETE'])
@app.route('/utilizadores/<int:id_user>', methods = ["GET", "DELETE", "PUT"])
# Check reference server for individual functions and arguments...
def utilizadores(id_user = None):

    r = make_response()

    if request.method == "GET":
        try:
            # Logic if GET -> READ
            if id_user:
                sql = f"SELECT id, nome FROM utilizadores WHERE id = {id_user}"
            else:
                sql = "SELECT id, nome FROM utilizadores"

            results = query_db(sql)

            # Creating response
            r = make_response(jsonify(results))

            # Setting status codes based on query results
            if len(results) > 0:
                r.status_code = 200
            else:
                # TODO: perhaps 404?
                r.status_code = 400

        except:
            r = make_response()
            r.status_code = 500


    elif request.method == "POST":
        # Logic if POST -> CREATE

        try:

            data = request.json

            name = data["nome"]
            password = data["senha"]

            sql = f"INSERT INTO utilizadores (nome, senha) VALUES ('{name}', '{password}')"

            query_db(sql)

            r.status_code = 200

        except Exception as e:
            r.status_code = 500
            print(e)
            print(e.__class__.__name__)



    elif request.method == "DELETE":
        # Logic if DELETE -> DELETE

        try:
            if id_user:
                # Checking for results to decide response status code since SQLite DELETE
                # does not return number of deleted rows.
                sql_count = f"SELECT * FROM utilizadores WHERE id = {id_user};"

                # Deleting corresponding rows.
                sql = f"DELETE FROM utilizadores WHERE id = {id_user}"

            else:
                # Checking for results to decide response status code since SQLite DELETE
                # does not return number of deleted rows.
                sql_count = f"SELECT * FROM utilizadores"

                # Deleting corresponding rows.
                sql = f"DELETE FROM utilizadores"

            results = query_db(sql_count)
            query_db(sql)

            if len(results) > 0:
                r.status_code = 200
            else:
                r.status_code = 400

        except:
            # If no rows were deleted, set status code 400.
            r.status_code = 500


    elif request.method == "PUT":
        # Logic if PUT/PATCH -> UPDATE
        try:
            data = request.json
            password = data["senha"]

            # Checking for results to decide response status code since SQLite UPDATE
            # does not return number of deleted rows.
            sql_count = f"SELECT * FROM utilizadores WHERE id = {id_user};"
            results = query_db(sql_count)

            # Updating corresponding rows.
            sql = f"UPDATE utilizadores SET senha = '{password}' WHERE id = {id_user};"
            query_db(sql)

            if len(results) > 0:
                r.status_code = 200
            else:
                # If no rows were updated, set status code 400.
                r.status_code = 400

        except:
            r.status_code = 500




    return r

@app.route('/albuns', methods = ['POST', 'DELETE', 'GET'])
@app.route('/albuns/<int:id_album>', methods = ['GET', 'DELETE'])
@app.route('/albuns/avaliacoes', methods = ['POST', 'GET', 'PUT'])
@app.route('/albuns/avaliacoes/<int:id_avaliacao>', methods = ['GET', 'DELETE'])
@app.route('/albuns/utilizadores/<int:id_user>', methods = ['GET', 'DELETE'])
@app.route('/albuns/artistas/<int:id_artista>', methods = ['GET', 'DELETE'])
# Check reference server for individual functions and arguments...
def albuns(id_avaliacao = None, id_album = None, id_user = None, id_artista = None):

    r = make_response()

    if request.method == "GET":
        if "avaliacoes" in request.path:
            if id_avaliacao:
                sql = f"""SELECT DISTINCT A.id, A.id_spotify, A.nome, A.id_artista
                          FROM albuns AS A, listas_albuns as LA
                          WHERE A.id == LA.id_album AND LA.id_avaliacao = {id_avaliacao}"""
            else:
                sql = f"SELECT * FROM listas_albuns"

        elif "utilizadores" in request.path:
            sql = f"""SELECT DISTINCT A.id, A.id_spotify, A.nome, A.id_artista
                      FROM albuns AS A, listas_albuns as LA
                      WHERE A.id == LA.id_album AND LA.id_user = {id_user}"""

        elif "artistas" in request.path:
            sql = f"SELECT id, id_spotify, nome, id_artista FROM albuns WHERE id_artista = {id_artista}"

        else:
            # Logic if GET -> READ or READ ALL
            if id_album:
                sql = f"SELECT id, id_spotify, nome, id_artista FROM albuns WHERE id = {id_album}"
            else:
                sql = "SELECT id, id_spotify, nome, id_artista FROM albuns"

        results = query_db(sql)

        processed_results = []
        for album in results:
            spotify_details = query_spotify(album["id_spotify"], type="album")
            print(spotify_details)

            # Merging both dictionaries and appending to results
            processed_results.append({**album, **spotify_details})


        # Creating response
        r = make_response(jsonify(processed_results))

        # Setting status codes based on query results
        if len(results) > 0:
            r.status_code = 200
        else:
            # TODO: perhaps 404?
            r.status_code = 400


    elif request.method == "POST":
        # Logic if POST -> CREATE

        try:
            # If we're dealing with a new rating instead of a new album
            if "avaliacoes" in request.path:
                data = request.json

                id_user = data["id_user"]
                id_album = data["id_album"]
                id_avaliacao = data["id_avaliacao"]

                sql = f"INSERT INTO listas_albuns (id_user, id_album, id_avaliacao) VALUES ('{id_user}', '{id_album}', {id_avaliacao})"

            else:
                data = request.json
                id_spotify = data["id_spotify"]

                # Obter informações sobre o album. Nome e info. sobre o artista
                name, info_spotify_artista = query_spotify(id_spotify, type="album", keys=["name", "artists"])

                # Selecionar o ID do spotify do artista
                id_spotify_artista = info_spotify_artista[0]["id"]

                # Verificar se, internamente, existe algum artista com esse id_spotify
                search_artist = f"SELECT id FROM artistas WHERE id_spotify = '{id_spotify_artista}'"


                id_artista = query_db(search_artist)

                # Caso exista, continuar com a inserção do album.
                # Caso não exista, inseri-lo na base de dados e obter o seu ID interno.
                if not id_artista:
                    insert_artist(id_spotify_artista)
                    id_artista = query_db(search_artist)[0].get("id")
                else:
                    id_artista = id_artista[0]["id"]

                sql = f'INSERT INTO albuns (id_spotify, nome, id_artista) VALUES ("{id_spotify}", "{name}", {id_artista})'

            query_db(sql)

            r.status_code = 200

        except Exception as e:
            print(e)
            print(e.__class__.__name__)
            r.status_code = 500


    elif request.method == "DELETE":
        # Logic if DELETE -> DELETE
        try:
            if "avaliacoes" in request.path:
                # Checking for results to decide response status code since SQLite DELETE
                # does not return number of deleted rows.
                sql_count = f"""SELECT A.id
                                FROM albuns AS A, listas_albuns AS LA
                                WHERE A.id = LA.id_album AND LA.id_avaliacao = {id_avaliacao}"""

                # Deleting corresponding rows
                sql = f"""DELETE
                          FROM albuns AS A
                          WHERE A.id in ({sql_count})"""

            elif "utilizadores" in request.path:
                # Checking for results to decide response status code since SQLite DELETE
                # does not return number of deleted rows.
                sql_count = f"""SELECT A.id, A.id_spotify, A.nome, A.id_artista
                          FROM albuns AS A, listas_albuns AS LA
                          WHERE A.id = LA.id_album AND LA.id_user = {id_user}"""

                # Deleting corresponding rows
                sql = f"""DELETE
                          FROM albuns AS A, listas_albuns AS LA
                          WHERE A.id = LA.id_album AND LA.id_user = {id_user}"""

            elif "artistas" in request.path:
                # Checking for results to decide response status code since SQLite DELETE
                # does not return number of deleted rows.
                sql_count = f"SELECT id, id_spotify, nome, id_artista FROM albuns WHERE id_artista = {id_artista}"

                # Deleting corresponding rows
                sql = f"DELETE FROM albuns WHERE id_artista = {id_artista}"

            else:
                # Logic if GET -> READ or READ ALL
                if id_album:
                    # Checking for results to decide response status code since SQLite DELETE
                    # does not return number of deleted rows.
                    sql_count = f"SELECT id, id_spotify, nome, id_artista FROM albuns WHERE id = {id_album}"

                    # Deleting corresponding rows
                    sql = f"DELETE FROM albuns WHERE id = {id_album}"

                else:

                    # Deleting all rows
                    sql = "DELETE FROM albuns"

            results = query_db(sql_count)
            query_db(sql)

            if len(results) > 0:
                r.status_code = 200
            else:
                r.status_code = 400

        except Exception as e:
            print(e)
            print(e.__class__.__name__)
            r.status_code = 500


    elif request.method == "PUT":
        # Logic if PUT/PATCH -> UPDATE
        try:
            data = request.json
            id_album = data["id_album"]
            id_user = data["id_user"]
            id_avaliacao = data["id_avaliacao"]

            # Checking for results to decide response status code since SQLite UPDATE
            # does not return number of deleted rows.
            sql = f"""SELECT * FROM listas_albuns
                      WHERE id_album = {id_album} AND id_user = {id_user};"""
            results = query_db(sql)

            print(results)

            # Updating corresponding rows.
            sql = f"""UPDATE listas_albuns
                      SET id_avaliacao = {id_avaliacao}
                      WHERE id_user = {id_user} AND id_album = {id_album};"""

            query_db(sql)

            if len(results) > 0:
                r.status_code = 200
            else:
                # If no rows were updated, set status code 400.
                r.status_code = 400

        except Exception as e:
            print(e)
            print(e.__class__.__name__)
            r.status_code = 500


    return r

@app.route('/artistas', methods = ['POST', 'DELETE', 'GET'])
@app.route('/artistas/<int:id_artista>', methods = ["GET", "DELETE"])
# Check reference server for individual functions and arguments...
def artistas(id_artista = None):

    r = make_response()

    if request.method == "GET":
        # Logic if GET -> READ or READ ALL

        if id_artista:
            sql = f"SELECT id, id_spotify, nome FROM artistas WHERE id = {id_artista}"
        else:
            sql = "SELECT id, id_spotify, nome FROM artistas"



        results = query_db(sql)

        processed_results = []

        for artist in results:
            spotify_details = query_spotify(artist["id_spotify"], type="artist")

            # Merging both dictionaries and appending to results
            processed_results.append({**artist, **spotify_details})

        # Creating response
        r = make_response(jsonify(processed_results))

        # Setting status codes based on query results
        if len(results) > 0:
            r.status_code = 200
        else:
            # TODO: perhaps 404?
            r.status_code = 400


    elif request.method == "POST":
        # Logic if POST -> CREATE

        try:

            data = request.json

            id_spotify = data["id_spotify"]

            insert_artist(id_spotify)

            r.status_code = 200

        except Exception as e:
            r.status_code = 500
            print(e.__class__.__name__)
            print(e)


    elif request.method == "DELETE":
        # Logic if DELETE -> DELETE

        try:
            if id_artista:
                # Checking for results to decide response status code since SQLite DELETE
                # does not return number of deleted rows.
                sql_count = f"SELECT * FROM artistas WHERE id = {id_artista};"

                # Deleting corresponding rows.
                sql = f"DELETE FROM artistas WHERE id = {id_artista}"

            else:
                # Checking for results to decide response status code since SQLite DELETE
                # does not return number of deleted rows.
                sql_count = f"SELECT * FROM artistas"

                # Deleting corresponding rows.
                sql = f"DELETE FROM artistas"

            results = query_db(sql_count)
            query_db(sql)

            if len(results) > 0:
                r.status_code = 200
            else:
                r.status_code = 400

        except:
            # If no rows were deleted, set status code 400.
            r.status_code = 500

    return r

# Helper functions

def insert_artist(id_spotify):

    name = query_spotify(id_spotify, type="artist", keys=["name"])[0]

    sql = f"INSERT INTO artistas (id_spotify, nome) VALUES ('{id_spotify}', '{name}')"

    query_db(sql)

def error_json(title, description):
    message = {"title":title,
               "description":description}


# Database related functions

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db(DATABASE)
    # Foreign s must be activated for every connection
    db.execute("PRAGMA foreign_keys = ON;")
    return db

def query_db(query, args=(), one=False):
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(query, args)
    conn.commit()
    rv = cursor.fetchall()
    cursor.close()

    # This is so that row names are also returned
    # so that they can be used as JSON keys
    return [dict(row) for row in rv]

## Closing database connection

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(debug = True)
