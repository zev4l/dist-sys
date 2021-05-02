"""
Aplicações distribuídas - Projeto 4 - db.py
Grupo: 77
Alunos: José Almeida - 55373, Augusto Gouveia - 55371
"""

import sqlite3
from os.path import isfile
from pprint import pprint

def connect_db(dbname):
    db_is_created = isfile(dbname)
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
                        id_spotify            TEXT UNIQUE,
                        nome                  TEXT,
                        id_artista            INTEGER,
                        FOREIGN KEY(id_artista) REFERENCES artistas(id) ON DELETE CASCADE
                    );

                    CREATE TABLE artistas (
                        id                     INTEGER PRIMARY KEY,
                        id_spotify             TEXT UNIQUE,
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
                        FOREIGN KEY(id_user) REFERENCES utilizadores(id) ON DELETE CASCADE,
                        FOREIGN KEY(id_album) REFERENCES albuns(id) ON DELETE CASCADE,
                        FOREIGN KEY(id_avaliacao) REFERENCES avaliacoes(id) ON DELETE CASCADE
                    );

                    INSERT INTO avaliacoes (id, sigla, designacao) VALUES
                        (1, "M", "Medíocre"),
                        (2, "m", "Mau"),
                        (3, "S", "Suficiente"),
                        (4, "B", "Bom"),
                        (5, "MB", "Muito Bom");

                """

        cursor.executescript(query)
        connection.commit()


    return connection


def printDB():
        conn = connect_db('data.db')
        cursor = conn.cursor()

        insts = ["SELECT * FROM utilizadores;",
                "SELECT * FROM albuns;",
                "SELECT * FROM artistas;",
                "SELECT * FROM listas_albuns;",
                "SELECT * FROM avaliacoes;"]

        for inst in insts:
            print("\n" + str(inst.split()[3]).upper())
            cursor.execute(inst)

            pprint(cursor.fetchall())

        cursor.close()

### TESTING LINES

if __name__ == '__main__':
    printDB()
