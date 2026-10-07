-- 1. Cria o banco de dados pokemon
CREATE DATABASE pokemon;

-- 2. Conecta no banco de dados que acabou de ser criado
\c pokemon;

-- 3. Cria a tabela pokedex dentro do banco pokemon
CREATE TABLE pokedex (
    nome_pokemon VARCHAR(100),
    tipo_pokemon VARCHAR(50),
    nivel_pokemon INTEGER,
    forca_pokemon INTEGER
);

-- 4. Insere exatamente os seus registros
INSERT INTO pokedex (nome_pokemon, tipo_pokemon, nivel_pokemon, forca_pokemon)
VALUES
('pikachu', 'eletrico', '1', '10'), 
('charmander', 'fogo', '2', '10'),
('bulbassaur', 'planta', '1', '8'),
('squirtle', 'agua', '1', '9');