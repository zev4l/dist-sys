import sqlite3
from pprint import pprint
from os.path import isfile

def connect_db(dbname):
    db_is_created = isfile(dbname) # Existe ficheiro da base de dados?
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    if not db_is_created:
        cursor.execute("CREATE TABLE notas (numero_aluno INTEGER, \
            ano TEXT, cadeira TEXT, nota INTEGER);")
        connection.commit()
    return connection, cursor

if __name__ == '__main__':
    conn, cursor = connect_db('notas.db')

    cursor.execute("SELECT * FROM notas")
    notas = cursor.fetchall() 
    print("Estado atual da base de dados:\n ALUNO,   ANO,   CADEIRA,   NOTA")
    pprint(notas)

    print("\nNÚMERO,   ANO,   IDADE")
    cursor.execute("SELECT * FROM aluno")
    alunos = cursor.fetchall()
    pprint(alunos)


