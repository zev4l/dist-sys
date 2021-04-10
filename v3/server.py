import requests # To interact with Spotify API
import sqlite3
from db import connect_db
from os.path import isfile
from flask import Flask, g, request, make_response, jsonify

# TODO: remove these imports
import traceback as t
from pprint import pprint

app = Flask(__name__)
DATABASE = "data.db"

# TODO: In every exception include JSON description of error instead of error 500 (Slide 4 TP07)

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

        except:
            r.status_code = 500



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
            sql = f"SELECT * FROM utilizadores WHERE id = {id_user};"
            results = query_db(sql)

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

@app.route('/albuns', methods = ['POST', 'PUT', 'DELETE', 'GET'])
@app.route('/albuns/<int:id_album>', methods = ["GET", "DELETE"])
@app.route('/albuns/avaliacoes', methods = ["POST"])
@app.route('/albuns/avaliacoes/<int:id_avaliacao>', methods = ["GET", "DELETE"])
@app.route('/albuns/utilizadores/<int:id_user>', methods = ["GET", "DELETE"])
@app.route('/albuns/artistas/<int:id_artista>', methods = ["GET", "DELETE"])
# Check reference server for individual functions and arguments...
def albuns(id_avaliacao = None, id_album = None, id_user = None, id_artista = None):

    r = make_response()

    if request.method == "GET":
        # Logic if GET -> READ or READ ALL
        if id_album:
            # TODO: Talvez join do nome do artista?
            sql = f"SELECT id, id_spotify, nome, id_artista FROM albuns WHERE id = {id_album}"
        else:
            sql = "SELECT id, id_spotify, nome, id_artista FROM albuns"

        results = query_db(sql)

        # Creating response
        r = make_response(jsonify(results))

        # Setting status codes based on query results
        if len(results) > 0:
            r.status_code = 200
        else:
            # TODO: perhaps 404?
            r.status_code = 400


    elif request.method == "POST":
        # Logic if POST -> CREATE

        try:
            # If we're dealing with a new rating
            if "avaliacoes" in request.path:
                data = request.json
                print(data)
                id_user = data["id_user"]
                id_album = data["id_album"]
                id_avaliacao = data["id_avaliacao"]

                sql = f"INSERT INTO listas_albuns (id_user, id_album, id_avaliacao) VALUES ('{id_user}', '{id_album}', {id_avaliacao})"

            else:
                data = request.json
                id_spotify = data["id_spotify"]
                name = data["nome"]
                id_artista = data["id_artista"]

                sql = f"INSERT INTO albuns (id_spotify, nome, id_artista) VALUES ('{id_spotify}', '{name}', {id_artista})"

            query_db(sql)

            r.status_code = 200

        except Exception as e:
            print(e)
            r.status_code = 500


    elif request.method == "DELETE":
        # Logic if DELETE -> DELETE
        pass

    elif request.method == "PUT":
        # Logic if PUT/PATCH -> UPDATE
        pass

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

        # Creating response
        r = make_response(jsonify(results))

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
            name = data["nome"]

            sql = f"INSERT INTO artistas (id_spotify, nome) VALUES ('{id_spotify}', '{name}')"

            query_db(sql)

            r.status_code = 200

        except:
            r.status_code = 500


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

# Database related functions

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db(DATABASE)
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
