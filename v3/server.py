from flask import Flask, g, request, make_response, jsonify
import sqlite3
from db import connect_db
from os.path import isfile
import requests # To interact with Spotify API

app = Flask(__name__)
DATABASE = "data.db"

# Routes...

@app.route('/utilizadores', methods = ['POST', 'PUT', 'PATCH', 'DELETE'])
@app.route('/utilizadores/<int:id_user>', methods = ["GET"])
# Check reference server for individual functions and arguments...
def utilizadores(id_user = None):

    if request.method == "GET":
        # Logic if GET -> READ
        pass

    elif request.method == "POST":
        # Logic if POST -> CREATE
        pass

    elif request.method == "DELETE":
        # Logic if DELETE -> DELETE
        pass

    elif request.method in ["PUT", "PATCH"]:
        # Logic if PUT/PATCH -> UPDATE
        pass


@app.route('/albuns', methods = ['POST', 'PUT', 'PATCH', 'DELETE'])
@app.route('/albuns/<int:id_album>', methods = ["GET"])
# Check reference server for individual functions and arguments...
def albuns(id_albuns = None):
    
    if request.method == "GET":
        # Logic if GET -> READ
        pass

    elif request.method == "POST":
        # Logic if POST -> CREATE
        pass

    elif request.method == "DELETE":
        # Logic if DELETE -> DELETE
        pass

    elif request.method in ["PUT", "PATCH"]:
        # Logic if PUT/PATCH -> UPDATE
        pass



@app.route('/artistas', methods = ['POST', 'DELETE'])
@app.route('/artistas/<int:id_artista>', methods = ["GET"])
# Check reference server for individual functions and arguments...
def artistas(id_artista = None):
    
    if request.method == "GET":
        # Logic if GET -> READ
        pass

    elif request.method == "POST":
        # Logic if POST -> CREATE
        pass

    elif request.method == "DELETE":
        # Logic if DELETE -> DELETE
        pass


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
