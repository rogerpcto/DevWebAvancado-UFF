-- Tabela de usuários
CREATE TABLE Usuario (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    nome VARCHAR(255) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    perfil VARCHAR(50) NOT NULL
);

-- Tabela de diretores
CREATE TABLE Diretor (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL
);

-- Tabela de mídias
CREATE TABLE Midia (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    nota FLOAT,
    data_de_lancamento DATE NOT NULL,
    genero VARCHAR(100),
    id_diretor INTEGER,
    FOREIGN KEY (id_diretor) REFERENCES Diretor(id)
);

-- Tabela de reviews
CREATE TABLE Review (
    id_usuario INTEGER,
    id_midia INTEGER,
    comentario TEXT,
    nota FLOAT,
    PRIMARY KEY (id_usuario, id_midia),
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id),
    FOREIGN KEY (id_midia) REFERENCES Midia(id)
);

-- Tabela de filmes (especialização de mídia)
CREATE TABLE Filme (
    id_midia INTEGER PRIMARY KEY,
    duracao INTEGER NOT NULL,
    FOREIGN KEY (id_midia) REFERENCES Midia(id)
);

-- Tabela de temporadas (associada a séries)
CREATE TABLE Temporada (
    id_midia INTEGER,
    numero INTEGER,
    PRIMARY KEY (id_midia, numero),
    FOREIGN KEY (id_midia) REFERENCES Midia(id)
);

-- Tabela de episódios
CREATE TABLE Episodio (
    id_midia INTEGER PRIMARY KEY,
    duracao INTEGER NOT NULL,
    id_serie INTEGER,
    numero_temporada INTEGER,
    numero_episodio INTEGER,
    FOREIGN KEY (id_midia) REFERENCES Midia(id),
    FOREIGN KEY (id_serie, numero_temporada) REFERENCES Temporada(id_midia, numero)
);