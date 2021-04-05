from flask import Flask, g, request, make_response, jsonify
import sqlite3
from db import connect_db
from os.path import isfile
import requests # To interact with Spotify API

app = Flask(__name__)
DATABASE = "data.db"

# Routes...

@app.route('/utilizadores', methods = ["GET"])
# Check reference server for individual functions and arguments...
def utilizadores():
    #### TEST LINES - PROOF OF CONCEPT
    results = query_db("SELECT * FROM avaliacoes;")

    r = make_response(jsonify(results)) 
    r.status_code = 200
    return r

    ####


@app.route('/artistas', methods = ["TODO: :)"])
# Check reference server for individual functions and arguments...



@app.route('/albuns', methods = ["TODO: :)"])
# Check reference server for individual functions and arguments...


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
