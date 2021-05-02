"""
Aplicações distribuídas - Projeto 4 - server.py
Grupo: 77
Alunos: José Almeida - 55373, Augusto Gouveia - 55371
"""

import requests # To interact with Spotify API
import sqlite3
import ssl
from db import connect_db
from os.path import isfile
from flask import Flask, g, request, make_response, jsonify, redirect, url_for
from requests_oauthlib import OAuth2Session

# Cert path
CERT_PATH = "/mnt/d/_/Projects/FCUL/AD/dist-sys/v4/certs/"

# OAuth2 related constants
CLIENT_ID = "a040271774db4f40b192f953a0872d84"
CLIENT_SECRET = "6460e1db9bd24d3398044e3c96d2a513"
AUTHORIZATION_BASE_URL = 'https://accounts.spotify.com/authorize'
REDIRECT_URI = 'https://localhost:5000/callback'
spotify = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)


INTERNAL_SERVER_ERROR = (500,
                         "Something went wrong while processing your request. Double-check your arguments or try again later.")

app = Flask(__name__)
DATABASE = "data.db"

# Using Spotify API

def query_spotify(id, type = "artist", keys="all"):
    """
    Query Spotify REST API for data regarding artist or album.
    """

    BASE_URL = 'https://api.spotify.com/v1/'

    headers = {
    'Authorization': 'Bearer {token}'.format(token=spotify.access_token)}

    if type == "artist":

        r = requests.get(BASE_URL + 'artists/' + id, headers=headers)

        print(r.status_code == 401)

        if r.status_code == 401:
            return "INVALID"

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

        # Return INVALID if the access token is invalid
        if r.status_code == 401:
            return "INVALID"

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


# ROUTES

#Login Route:
@app.route('/login', methods = ["GET"])
def login():
	# Pedido do authorization_code ao servidor de autorização (e dono do recuro a aceder)
	AUTHORIZATION_URL, state = spotify.authorization_url(AUTHORIZATION_BASE_URL)

	return redirect(AUTHORIZATION_URL)

@app.route('/callback', methods = ["GET"])
def callback():
    try:

        r = make_response("Autorizado")
        TOKEN_URL = 'https://accounts.spotify.com/api/token'
        URL_RESPONSE = request.url
        spotify.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET, authorization_response=URL_RESPONSE)

        print(spotify.access_token)

    except:
        redirect(url_for('.login'))

    return r

# Utilizadores Route:
@app.route('/utilizadores', methods = ['POST', 'GET', 'DELETE'])
@app.route('/utilizadores/<int:id_user>', methods = ["GET", "DELETE", "PUT"])

def utilizadores(id_user = None):
    """
    Handles requests for route /utilizadores regarding methods POST, GET, DELETE and PUT.
    """

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
            if len(results) > 0 or id_user == None:
                r.status_code = 200
            else:
                r = make_response(error_json(404,
                                             f"The requested user ({id_user}) could not be found."))
                r.status_code = 404

        except:
            r = make_response(error_json(*INTERNAL_SERVER_ERROR))
            r.status_code = 500


    elif request.method == "POST":
        # Logic if POST -> CREATE

        try:

            data = request.json

            # Getting JSON data
            name = data["nome"]
            password = data["senha"]

            # Executing SQL instructions - Inserting new user
            sql = f"INSERT INTO utilizadores (nome, senha) VALUES ('{name}', '{password}')"
            query_db(sql)

            # Status code 201: Successfully Created
            r.status_code = 201

        except sqlite3.IntegrityError as e:
            # Catching IntegrityError, in case request user has already been created
            if "UNIQUE" in e.__str__():
                r = make_response(error_json(409, "This request violates policy. This resource has already been registered"))
                # Status code 409: Conflict
                r.status_code = 409

        except KeyError:
            # Catching KeyError if client fails to provide all required JSON arguments.
            r = make_response(error_json(400, "Wrong syntax. Make sure to include all JSON arguments."))

        except:
            # Catching all other exceptions.
            r = make_response(error_json(*INTERNAL_SERVER_ERROR))
            r.status_code = 500



    elif request.method == "DELETE":
        # Logic if DELETE -> DELETE

        try:
            if id_user:
                # If a user has been specified for deletion.
                # Deleting corresponding rows.
                sql = f"DELETE FROM utilizadores WHERE id = {id_user}"

            else:
                # If no user has been specified (delete every user).
                # Deleting corresponding rows.
                sql = f"DELETE FROM utilizadores"

            # Executing SQL instructions
            query_db(sql)

            # Status code 204: OK but No Content to be delivered
            r.status_code = 204

        except:
            # Catching all exceptions.

            r = make_response(error_json(*INTERNAL_SERVER_ERROR))
            r.status_code = 500


    elif request.method == "PUT":
        # Logic if PUT/PATCH -> UPDATE
        try:

            # Getting JSON arguments.
            data = request.json
            password = data["senha"]

            # Updating corresponding rows.
            sql = f"UPDATE utilizadores SET senha = '{password}' WHERE id = {id_user};"
            query_db(sql)

            # Status code 204: OK but No Content to be delivered
            r.status_code = 204

        except KeyError:
            # Catching KeyError if client fails to provide all required JSON arguments.
            r = make_response(error_json(400, "Wrong syntax. Make sure to include all JSON arguments."))

        except:
            # Catching all other exceptions.
            r = make_response(error_json(*INTERNAL_SERVER_ERROR))
            r.status_code = 500

    return r

# Albuns Route:
@app.route('/albuns', methods = ['POST', 'DELETE', 'GET'])
@app.route('/albuns/<int:id_album>', methods = ['GET', 'DELETE'])
@app.route('/albuns/avaliacoes', methods = ['POST', 'GET', 'PUT'])
@app.route('/albuns/avaliacoes/<int:id_avaliacao>', methods = ['GET', 'DELETE'])
@app.route('/albuns/utilizadores/<int:id_user>', methods = ['GET', 'DELETE'])
@app.route('/albuns/artistas/<int:id_artista>', methods = ['GET', 'DELETE'])

def albuns(id_avaliacao = None, id_album = None, id_user = None, id_artista = None):
    """
    Handles requests for route /albuns and all subroutes (albuns and avaliacoes).
    Supports POST, GET, DELETE and PUT
    """
    r = make_response()

    if request.method == "GET":
        try:
            if "avaliacoes" in request.path:
                # If subroute involves ratings
                if id_avaliacao:
                    # Getting all albums rated with specified rating
                    sql = f"""SELECT DISTINCT A.id, A.id_spotify, A.nome, A.id_artista
                              FROM albuns AS A, listas_albuns as LA
                              WHERE A.id == LA.id_album AND LA.id_avaliacao = {id_avaliacao}"""
                else:
                    # Getting all ratings if no rating is specified
                    sql = f"SELECT * FROM listas_albuns"

            # If subroute involves users
            elif "utilizadores" in request.path:

                # Getting all albuns rated by specified user
                sql = f"""SELECT DISTINCT A.id, A.id_spotify, A.nome, A.id_artista
                          FROM albuns AS A, listas_albuns as LA
                          WHERE A.id == LA.id_album AND LA.id_user = {id_user}"""

            # If subroute involves artists
            elif "artistas" in request.path:
                # Getting all albuns by specified artist
                sql = f"SELECT id, id_spotify, nome, id_artista FROM albuns WHERE id_artista = {id_artista}"

            # If it's the main route (/albuns)
            else:
                if id_album:
                    # Getting specified album
                    sql = f"SELECT id, id_spotify, nome, id_artista FROM albuns WHERE id = {id_album}"
                else:
                    # Getting all albums if id_album isn't specified
                    sql = "SELECT id, id_spotify, nome, id_artista FROM albuns"

            # Querying database with previously decided criteria
            results = query_db(sql)

            # Processing results: Adding Spotify data to local data about albums
            processed_results = []

            # (Unless the current request is about ratings (listas_albuns))
            if not ("avaliacoes" in request.path and not id_avaliacao):
                for album in results:
                    spotify_details = query_spotify(album["id_spotify"], type="album")

                    print(spotify_details)

                    # Redirect user to login page if access token is invalid
                    if spotify_details == "INVALID":
                        return redirect(url_for('.login'))

                    # Merging both dictionaries and appending to results
                    processed_results.append({**album, **spotify_details})

            # Creating response
            r = make_response(jsonify(processed_results))

            # Setting status codes based on query results
            if len(results) > 0 or not any((id_avaliacao, id_user, id_artista, id_album)):
                r.status_code = 200

            else:
                # Sending 404 error message if no albums fitting criteria are found
                if id_avaliacao:
                    # If criteria is albums rated with rating (id_avaliacao)
                    description = f"No albums with rating {id_avaliacao} were found."
                elif id_user:
                    # If criteria is albums rated by user (id_user)
                    description = f"No albums rated by user {id_user} were found."
                elif id_artista:
                    # If criteria is albums by artist (id_artista)
                    description = f"No albums by artist {id_artista} were found."
                elif id_album:
                    # If criteria is album with id id_album
                    description = f"Album {id_album} could not be found."

                r = make_response(error_json(404, description))
                r.status_code = 404

        except Exception:
            # Catching all other exceptions
            r = make_response(error_json(*INTERNAL_SERVER_ERROR))
            r.status_code = 500


    elif request.method == "POST":
        # Logic if POST -> CREATE

        try:
            # If we're dealing with a new rating instead of a new album
            if "avaliacoes" in request.path:
                data = request.json

                # Getting JSON arguments
                id_user = data["id_user"]
                id_album = data["id_album"]
                id_avaliacao = data["id_avaliacao"]

                # Inserting new rating into database
                sql = f"INSERT INTO listas_albuns (id_user, id_album, id_avaliacao) VALUES ('{id_user}', '{id_album}', {id_avaliacao})"

            # If we're dealing with a new album
            else:
                data = request.json

                # Getting JSON arguments
                id_spotify = data["id_spotify"]

                # Obtaining info about album and its author

                spotify_details = query_spotify(id_spotify, type="album", keys=["name", "artists"])

                # Redirect user to login page if access token is invalid
                if spotify_details == "INVALID":
                    redirect(url_for('.login'))

                name, info_spotify_artista = spotify_details

                # Selecting the artist's spotify ID
                id_spotify_artista = info_spotify_artista[0]["id"]

                # Checking if, internally, there is any registered artist with such a spotify ID
                search_artist = f"SELECT id FROM artistas WHERE id_spotify = '{id_spotify_artista}'"
                id_artista = query_db(search_artist)

                # If there is, continue with album insertion
                # In case there isn't, insert artist into database and obtain it's internal ID
                if not id_artista:
                    insert_artist(id_spotify_artista)
                    id_artista = query_db(search_artist)[0].get("id")
                else:
                    id_artista = id_artista[0]["id"]

                sql = f'INSERT INTO albuns (id_spotify, nome, id_artista) VALUES ("{id_spotify}", "{name}", {id_artista})'

            # Executing previously decided instructions
            query_db(sql)

            # Status code 201: Created Successfully
            r.status_code = 201

        except KeyError:
            # Catching KeyError if client fails to provide all required JSON arguments.
            r = make_response(error_json(400, "Wrong syntax. Make sure to include all JSON arguments."))

        # Handling database IntegrityError exceptions
        except sqlite3.IntegrityError as e:
            # Catching FOREIGN KEY errors and reporting to client.
            if "FOREIGN KEY" in e.__str__():
                r = make_response(error_json(400, "This request violates policy. Please check if the mentioned artist/album/user is already registered."))
                r.status_code = 400

            # Catching UNIQUE errors and reporting to client.
            if "UNIQUE" in e.__str__():
                r = make_response(error_json(409, "This request violates policy. This resource has already been registered"))
                # Status code 409: Conflict
                r.status_code = 409

        except KeyError:
            # Catching KeyError if client fails to provide all required JSON arguments
            r = make_response(error_json(400, "Wrong syntax. Make sure to include all JSON arguments."))

        except:
            # Catching all other exceptions
            r = make_response(error_json(*INTERNAL_SERVER_ERROR))
            r.status_code = 500


    elif request.method == "DELETE":
        # Logic if DELETE -> DELETE
        try:
            # If subroute involves avaliacoes
            if "avaliacoes" in request.path:
                # Checking for albums rated with rating id_avaliacao
                sql_count = f"""SELECT A.id
                                FROM albuns AS A, listas_albuns AS LA
                                WHERE A.id = LA.id_album AND LA.id_avaliacao = {id_avaliacao}"""

                # Deleting corresponding rows
                sql = f"""DELETE
                          FROM albuns AS A
                          WHERE A.id in ({sql_count})"""

            # If subroute involves utilizadores
            elif "utilizadores" in request.path:

                # Checking for albums rated by user id_user
                sql_count = f"""SELECT A.id
                                FROM albuns AS A, listas_albuns AS LA
                                WHERE A.id = LA.id_album AND LA.id_user = {id_user}"""

                # Deleting corresponding rows
                sql = f"""DELETE
                          FROM albuns AS A
                          WHERE A.id in ({sql_count})"""

            # If subroute involves artistas
            elif "artistas" in request.path:

                # Deleting albums by artista id_artista
                sql = f"DELETE FROM albuns WHERE id_artista = {id_artista}"

            # If it's the main route (/album)
            else:
                # If an album is specified
                if id_album:

                    # Deleting specific album
                    sql = f"DELETE FROM albuns WHERE id = {id_album}"

                # If no albums are specified
                else:

                    # Deleting all rows
                    sql = "DELETE FROM albuns"

            query_db(sql)

            # Status code 204: OK but No Content to be delivered.
            r.status_code = 204

        except:
            # Catching all exceptions
            r = make_response(error_json(*INTERNAL_SERVER_ERROR))
            r.status_code = 500



    elif request.method == "PUT":
        # Logic if PUT/PATCH -> UPDATE
        try:
            data = request.json

            # Getting JSON arguments
            id_album = data["id_album"]
            id_user = data["id_user"]
            id_avaliacao = data["id_avaliacao"]

            # Checking for results to decide response status code since SQLite UPDATE
            # does not return number of deleted rows.
            sql = f"""SELECT * FROM listas_albuns
                      WHERE id_album = {id_album} AND id_user = {id_user};"""
            results = query_db(sql)

            # Updating corresponding ratings.
            sql = f"""UPDATE listas_albuns
                      SET id_avaliacao = {id_avaliacao}
                      WHERE id_user = {id_user} AND id_album = {id_album};"""

            query_db(sql)

            if len(results) > 0:
                r.status_code = 204
            else:
                # If no ratings were updated, meaning the specified rating does not exist deliver status code 404
                r = make_response(error_json(404, f"The mentioned user ({id_user}) has not reviewed album {id_album}."))
                r.status_code = 404

        except KeyError:
            # Catching KeyError if client fails to provide all required JSON arguments
            r = make_response(error_json(400, "Wrong syntax. Make sure to include all JSON arguments."))

        except:
            # Catching all other exceptions
            r = make_response(error_json(*INTERNAL_SERVER_ERROR))
            r.status_code = 500

    return r


# Artistas Route:
@app.route('/artistas', methods = ['POST', 'DELETE', 'GET'])
@app.route('/artistas/<int:id_artista>', methods = ["GET", "DELETE"])
def artistas(id_artista = None):

    if request.method == "GET":
        try:
            # Logic if GET -> READ or READ ALL

            # If id_artista is specified
            if id_artista:
                sql = f"SELECT id, id_spotify, nome FROM artistas WHERE id = {id_artista}"
            # If no artist is specified, deliver all artists
            else:
                sql = "SELECT id, id_spotify, nome FROM artistas"

            # Executing previously decided instructions
            results = query_db(sql)

            # Processing results: Adding Spotify data to local data about artists
            processed_results = []

            for artist in results:

                spotify_details = query_spotify(artist["id_spotify"], type="artist")

                # Redirect user to login page
                if spotify_details == "INVALID":
                    return redirect(url_for('.login'))

                # Merging both dictionaries (local data and spotify data) and appending to results
                processed_results.append({**artist, **spotify_details})

            # Creating response
            r = make_response(jsonify(processed_results))

            # Setting status codes based on query results
            if len(results) > 0 or id_artista == None:
                r.status_code = 200
            else:
                r = make_response(error_json(404,
                                             f"The requested artist ({id_artista}) could not be found."))
                r.status_code = 404

        except:
            # Catching all exceptions
            r = make_response(error_json(*INTERNAL_SERVER_ERROR))
            r.status_code = 500


    elif request.method == "POST":
        # Logic if POST -> CREATE

        r = make_response()

        try:

            data = request.json

            # Getting JSON arguments

            id_spotify = data["id_spotify"]

            # Inserting new artist

            insert_artist(id_spotify)

            r.status_code = 201

        except KeyError:
            # Catching KeyError if client fails to provide all required JSON arguments
            r = make_response(error_json(400, "Wrong syntax. Make sure to include all JSON arguments."))


        except sqlite3.IntegrityError as e:
            # Handling database IntegrityError exceptions

            # Catching UNIQUE errors and reporting to client.
            if "UNIQUE" in e.__str__():
                r = make_response(error_json(409, "This request violates policy. This artist has already been registered"))
                # Status code 409: Conflict
                r.status_code = 409

        except:
            # Catching all other exceptions
            r = make_response(error_json(*INTERNAL_SERVER_ERROR))
            r.status_code = 500


    elif request.method == "DELETE":
        # Logic if DELETE -> DELETE

        r = make_response()

        try:
            # If id_artista is specified
            if id_artista:
                # Deleting corresponding rows.
                sql = f"DELETE FROM artistas WHERE id = {id_artista}"

            # If not, delete all artists
            else:
                # Deleting corresponding rows.
                sql = f"DELETE FROM artistas"

            # Executing previously decided instructions
            query_db(sql)

            r.status_code = 204

        except:
            # Catching all exceptions
            r = make_response(error_json(*INTERNAL_SERVER_ERROR))
            r.status_code = 500

    return r

# Helper functions

def insert_artist(id_spotify):
    """
    Wrapper for artist insertion. Used when album author isn't registed in database
    and when new new artist is created.
    """

    name = query_spotify(id_spotify, type="artist", keys=["name"])[0]

    sql = f"INSERT INTO artistas (id_spotify, nome) VALUES ('{id_spotify}', '{name}')"

    query_db(sql)


def error_json(code, description):
    """
    Creation of JSONified message describing error in detail.
    """

    URLs = {500:"https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/500",
            404:"https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404",
            400:"https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400",
            409:"https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/409"}

    titles = {500:"Internal Server Error",
              404:"Resource Not Found",
              400:"Bad Request",
              409:"Conflict"}

    return jsonify({"describedBy":URLs[code],
                    "httpStatus":code,
                    "title":titles[code],
                    "detail":description})

# Database related functions

def get_db():
    """
    Getting access to database
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db(DATABASE)

    # Foreign key support must be activated for every connection
    db.execute("PRAGMA foreign_keys = ON;")
    return db

def query_db(query, args=(), one=False):
    """
    Executing queries and instructions
    """
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
    """
    Safely closing connection when closing server.
    """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_SERVER)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations(cafile=CERT_PATH + 'root.pem')
    context.load_cert_chain(certfile=CERT_PATH + 'serv.crt',keyfile=CERT_PATH + 'serv.key')
    app.run('localhost', ssl_context=context, debug = True)
