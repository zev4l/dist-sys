import requests # To interact with Spotify API
import sqlite3
from db import connect_db
from os.path import isfile
from flask import Flask, g, request, make_response, jsonify

app = Flask(__name__)
DATABASE = "data.db"

# Routes...

@app.route('/utilizadores', methods = ['POST', 'PUT', 'DELETE', 'GET'])
@app.route('/utilizadores/<int:id_user>', methods = ["GET"])
# Check reference server for individual functions and arguments...
def utilizadores(id_user = None):

    r = make_response()

    if request.method == "GET":
        # Logic if GET -> READ or READ ALL
        if id_user:
            sql = f"SELECT id, sigla, designacao FROM avaliacoes WHERE id = {id_user}"
            results = query_db(sql)
            print(results)
            r = make_response(jsonify(results))
            # TODO: This may not always be true, sort it out later
            r.status_code = 200

    elif request.method == "POST":
        # Logic if POST -> CREATE
        pass

    elif request.method == "DELETE":
        # Logic if DELETE -> DELETE
        pass

    elif request.method == "PUT":
        # Logic if PUT/PATCH -> UPDATE
        pass

    return r

@app.route('/albuns', methods = ['POST', 'PUT', 'DELETE', 'GET'])
@app.route('/albuns/<int:id_album>', methods = ["GET"])
# Check reference server for individual functions and arguments...
def albuns(id_albuns = None):

    r = make_response()

    if request.method == "GET":
        # Logic if GET -> READ or READ ALL

        pass

    elif request.method == "POST":
        # Logic if POST -> CREATE
        pass

    elif request.method == "DELETE":
        # Logic if DELETE -> DELETE
        pass

    elif request.method == "PUT":
        # Logic if PUT/PATCH -> UPDATE
        pass

    return r

@app.route('/artistas', methods = ['POST', 'DELETE', 'GET'])
@app.route('/artistas/<int:id_artista>', methods = ["GET"])
# Check reference server for individual functions and arguments...
def artistas(id_artista = None):

    r = make_response()

    if request.method == "GET":
        # Logic if GET -> READ or READ ALL

        pass

    elif request.method == "POST":
        # Logic if POST -> CREATE
        pass

    elif request.method == "DELETE":
        # Logic if DELETE -> DELETE
        pass

    return r

# Database related functions

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cursor = get_db().execute(query, args)
    rv = cursor.fetchall()
    cursor.close()
    return (rv[0] if rv else None) if one else rv

## Closing database connection

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(debug = True)
