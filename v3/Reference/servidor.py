from flask import Flask, request, make_response, jsonify
import sqlite3
from os.path import isfile

app = Flask(__name__)
dbname = "notas.db"

@app.route('/aluno', methods = ["PUT"])
@app.route('/aluno/<int:id>', methods = ["GET"])
def aluno(id = None):
    if request.method == "GET":
        # Ler dados do aluno com id na base de dados

        aluno = id

        sql = f"SELECT * FROM aluno WHERE numero = {aluno}"
        print(sql)

        results = query(sql)

        r = make_response(jsonify(results))
        r.status_code = 200
        return r

    if request.method == "PUT":
        # Ler dados do aluno no pedido e inserir na base de dados
        # Em caso de sucesso responder com a localização do novo recurso

        dados = request.json

        numero = dados["numero"]
        nome = dados["nome"]
        idade = dados["idade"]

        sql = f"INSERT INTO aluno VALUES ({numero}, '{nome}', '{idade}')"

        query(sql)

        r = make_response()
        r.headers['location'] = f'/alunos/{numero}'
        return r

@app.route('/notas', methods = ["POST", "GET"])
def notas():
    if request.method == "POST":
        #ler dados no pedido e inserir na base de dados

        dados = request.json

        numero_aluno = dados["numero_aluno"]
        ano = dados["ano"]
        cadeira = dados["cadeira"]
        nota = dados["nota"]

        sql = f"INSERT INTO notas VALUES ({numero_aluno}, '{ano}', '{cadeira}', {nota})"

        query(sql)

        r = make_response("")
        r.status_code = 200
        return r

    if request.method == "GET":
        dados = request.json
        ano = dados["ano"]
        cadeira = dados["cadeira"]

        sql = f"SELECT * FROM notas WHERE ano = '{ano}' AND cadeira = '{cadeira}'"
        print(sql)

        results = query(sql)
        r = make_response(jsonify(results))
        r.status_code = 200
        return r

# Database
def query(sql):
    conn, cursor = connect_db()

    cursor.execute(sql)
    conn.commit()

    results = cursor.fetchall()

    conn.close()

    print(results)

    return results

def connect_db():
    db_is_created = isfile(dbname) # Existe ficheiro da base de dados?
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    if not db_is_created:
        cursor.execute("CREATE TABLE notas (numero_aluno INTEGER, \
            ano TEXT, cadeira TEXT, nota INTEGER);")
        cursor.execute("CREATE TABLE aluno (numero INTEGER, \
            nome TEXT, idade INTEGER);")
        connection.commit()
    return connection, cursor

if __name__ == '__main__':
    app.run(debug = True)
