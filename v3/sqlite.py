import sqlite3
from pprint import pprint
from os.path import isfile

def connect_db(dbname):
    db_is_created = isfile(dbname) # Existe ficheiro da base de dados?
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    if not db_is_created:
        query = """ PRAGMA foreign_keys = ON;

                    CREATE TABLE utilizadores (
                        id                     INTEGER PRIMARY KEY,
                        nome                   TEXT,
                        senha                  TEXT
                    );

                    CREATE TABLE albuns (
                        id                    INTEGER PRIMARY KEY,
                        id_spotify            TEXT,
                        nome                  TEXT,
                        id_artista            INTEGER,
                        FOREIGN KEY(id_artista) REFERENCES artistas(id)
                    );
                    CREATE TABLE artistas (
                        id                     INTEGER PRIMARY KEY,
                        id_spotify             TEXT,
                        nome                   TEXT
                    );

                    CREATE TABLE avaliacoes (
                        id                     INTEGER PRIMARY KEY,
                        sigla                  TEXT,
                        designacao             TEXT
                    );


                    CREATE TABLE listas_albuns (
                        id_user               INTEGER,
                        id_album              INTEGER,
                        id_avaliacao          INTEGER,
                        PRIMARY KEY (id_user, id_album),
                        FOREIGN KEY(id_user) REFERENCES utilizadores(id),
                        FOREIGN KEY(id_album) REFERENCES albuns(id)
                        FOREIGN KEY(id_avaliacao)REFERENCES avaliacoes(id)
                    );"""

        cursor.execute(query)
        connection.commit()
    return connection, cursor

if __name__ == '__main__':
    conn, cursor = connect_db('data.db')

    # cursor.execute("SELECT * FROM notas")
    # notas = cursor.fetchall() 
    # print("Estado atual da base de dados:\n ALUNO,   ANO,   CADEIRA,   NOTA")
    # pprint(notas)

    # print("\nNÚMERO,   ANO,   IDADE")
    # cursor.execute("SELECT * FROM aluno")
    # alunos = cursor.fetchall()
    # pprint(alunos)


