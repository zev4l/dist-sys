import requests # To interact with Spotify API
import sqlite3
from db import connect_db
from os.path import isfile
from flask import Flask, g, request, make_response, jsonify
import traceback as t

app = Flask(__name__)
DATABASE = "data.db"

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
                results = query_db(sql)

                r = make_response(jsonify(results))

                if len(results) > 0:
                    r.status_code = 200
                else:
                    r.status_code = 400
            else:
                sql = f"SELECT id, nome FROM utilizadores"
                results = query_db(sql)

                r = make_response(jsonify(results))

                if len(results) > 0:
                    r.status_code = 200
                else:
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

        except TypeError:
            r.status_code = 500



    elif request.method == "DELETE":
        # Logic if DELETE -> DELETE

        try:
            if id_user:
                # Checking for results to decide response status code since SQLite DELETE
                # does not return number of deleted rows.
                sql = f"SELECT * FROM utilizadores WHERE id = {id_user};"
                results = query_db(sql)

                # Deleting corresponding rows.
                sql = f"DELETE FROM utilizadores WHERE id = {id_user}"
                query_db(sql)

                if len(results) > 0:
                    r.status_code = 200
                else:
                    r.status_code = 400

            else:
                # Checking for results to decide response status code since SQLite DELETE
                # does not return number of deleted rows.

                sql = f"SELECT * FROM utilizadores"
                results = query_db(sql)

                sql = f"DELETE FROM utilizadores"

                query_db(sql)

                if len(results) > 0:
                    r.status_code = 200
                else:
                    r.status_code = 400




        except:
            # If no rows were updated, set status code 400.
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
    conn = get_db()
    cursor = conn.execute(query, args)
    conn.commit()
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
