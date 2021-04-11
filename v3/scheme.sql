create table utilizadores
(
    id    INTEGER
        primary key,
    nome  TEXT,
    senha TEXT
);

INSERT INTO utilizadores (id, nome, senha) VALUES (1, 'Rudy', '31231231');
INSERT INTO utilizadores (id, nome, senha) VALUES (2, 'Amos', '31231231');
INSERT INTO utilizadores (id, nome, senha) VALUES (3, 'Alfredo', '31231231');
INSERT INTO utilizadores (id, nome, senha) VALUES (4, 'Everette', '31231231');
INSERT INTO utilizadores (id, nome, senha) VALUES (5, 'Rogelio', '31231231');
INSERT INTO utilizadores (id, nome, senha) VALUES (6, 'Zane', '31231231');
INSERT INTO utilizadores (id, nome, senha) VALUES (7, 'Caleb', '31231231');
INSERT INTO utilizadores (id, nome, senha) VALUES (8, 'Cyrus', '31231231');
INSERT INTO utilizadores (id, nome, senha) VALUES (9, 'Reed', '31231231');
INSERT INTO utilizadores (id, nome, senha) VALUES (10, 'Lenard', '31231231');
INSERT INTO utilizadores (id, nome, senha) VALUES (11, 'Lucas', '31231231');
INSERT INTO utilizadores (id, nome, senha) VALUES (12, 'Roberto', '31231231');
INSERT INTO utilizadores (id, nome, senha) VALUES (13, 'Art', '31231231');
INSERT INTO utilizadores (id, nome, senha) VALUES (14, 'Parker', '31231231');
INSERT INTO utilizadores (id, nome, senha) VALUES (15, 'Geoffrey', '31231231');

create table artistas
(
    id         INTEGER
        primary key,
    id_spotify TEXT
        unique,
    nome       TEXT
);

INSERT INTO artistas (id, id_spotify, nome) VALUES (1, '7Ln80lUS6He07XvHI8qqHH', 'Arctic Monkeys');
INSERT INTO artistas (id, id_spotify, nome) VALUES (2, '3Gm5F95VdRxW3mqCn8RPBJ', 'Aminé');
INSERT INTO artistas (id, id_spotify, nome) VALUES (3, '699OTQXzgjhIYAHMy9RyPD', 'Playboi Carti');
INSERT INTO artistas (id, id_spotify, nome) VALUES (4, '0WgyCbru4tXnMsbTmX4mFw', 'Atlanta Rhythm Section');
INSERT INTO artistas (id, id_spotify, nome) VALUES (5, '4tZwfgrHOc3mvqYlEYSvVi', 'Daft Punk');
INSERT INTO artistas (id, id_spotify, nome) VALUES (6, '0ndWKGm6Kl92RMNKdEsco1', 'Exodia');
INSERT INTO artistas (id, id_spotify, nome) VALUES (7, '360IAlyVv4PCEVjgyMZrxK', 'Miguel');
INSERT INTO artistas (id, id_spotify, nome) VALUES (8, '2h93pZq0e7k5yf4dywlkpM', 'Frank Ocean');
INSERT INTO artistas (id, id_spotify, nome) VALUES (9, '5RADpgYLOuS2ZxDq7ggYYH', 'Death Grips');

create table albuns
(
    id         INTEGER
        primary key,
    id_spotify TEXT
        unique,
    nome       TEXT,
    id_artista INTEGER
        references artistas
            on delete cascade
);

INSERT INTO albuns (id, id_spotify, nome, id_artista) VALUES (1, '78bpIziExqiI9qztvNFlQu', 'AM', 1);
INSERT INTO albuns (id, id_spotify, nome, id_artista) VALUES (2, '3lajefIuUk4SfzqVBSJy8p', 'Good For You', 2);
INSERT INTO albuns (id, id_spotify, nome, id_artista) VALUES (3, '493HYe7N5pleudEZRyhE7R', 'All I Want Is You', 7);
INSERT INTO albuns (id, id_spotify, nome, id_artista) VALUES (4, '3mH6qwIy9crq0I9YQbOuDf', 'Blonde', 8);
INSERT INTO albuns (id, id_spotify, nome, id_artista) VALUES (5, '5Y04ylQjDWsawOUJXzY4YO', 'The Powers That B', 9);

create table avaliacoes
(
    id         INTEGER
        primary key,
    sigla      TEXT,
    designacao TEXT
);

INSERT INTO avaliacoes (id, sigla, designacao) VALUES (1, 'M', 'Medíocre');
INSERT INTO avaliacoes (id, sigla, designacao) VALUES (2, 'm', 'Mau');
INSERT INTO avaliacoes (id, sigla, designacao) VALUES (3, 'S', 'Suficiente');
INSERT INTO avaliacoes (id, sigla, designacao) VALUES (4, 'B', 'Bom');
INSERT INTO avaliacoes (id, sigla, designacao) VALUES (5, 'MB', 'Muito Bom');

create table listas_albuns
(
    id_user      INTEGER
        references utilizadores
            on delete cascade,
    id_album     INTEGER
        references albuns
            on delete cascade,
    id_avaliacao INTEGER
        references avaliacoes
            on delete cascade,
    primary key (id_user, id_album)
);

INSERT INTO listas_albuns (id_user, id_album, id_avaliacao) VALUES (1, 1, 5);
INSERT INTO listas_albuns (id_user, id_album, id_avaliacao) VALUES (2, 4, 4);
INSERT INTO listas_albuns (id_user, id_album, id_avaliacao) VALUES (3, 1, 3);
INSERT INTO listas_albuns (id_user, id_album, id_avaliacao) VALUES (4, 2, 2);
INSERT INTO listas_albuns (id_user, id_album, id_avaliacao) VALUES (5, 3, 4);