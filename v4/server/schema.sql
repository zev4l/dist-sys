PRAGMA foreign_keys = ON;

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