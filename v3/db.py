import sqlite3
from os.path import isfile

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


### TESTING LINES

# if __name__ == '__main__':
#     conn = connect_db('data.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#     cursor.execute("SELECT * FROM avaliacoes;")
#     print(cursor.fetchall())
