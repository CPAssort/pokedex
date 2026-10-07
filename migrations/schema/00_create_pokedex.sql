CREATE TABLE IF NOT EXISTS pokedex (
    nome_pokemon VARCHAR(100),
    tipo_pokemon VARCHAR(50),
    nivel_pokemon INTEGER,
    forca_pokemon INTEGER
);

INSERT INTO pokedex (nome_pokemon, tipo_pokemon, nivel_pokemon, forca_pokemon)
SELECT 'pikachu', 'eletrico', 1, 10
WHERE NOT EXISTS (
    SELECT 1 FROM pokedex WHERE nome_pokemon = 'pikachu'
);

INSERT INTO pokedex (nome_pokemon, tipo_pokemon, nivel_pokemon, forca_pokemon)
SELECT 'charmander', 'fogo', 2, 10
WHERE NOT EXISTS (
    SELECT 1 FROM pokedex WHERE nome_pokemon = 'charmander'
);

INSERT INTO pokedex (nome_pokemon, tipo_pokemon, nivel_pokemon, forca_pokemon)
SELECT 'bulbassaur', 'planta', 1, 8
WHERE NOT EXISTS (
    SELECT 1 FROM pokedex WHERE nome_pokemon = 'bulbassaur'
);

INSERT INTO pokedex (nome_pokemon, tipo_pokemon, nivel_pokemon, forca_pokemon)
SELECT 'squirtle', 'agua', 1, 9
WHERE NOT EXISTS (
    SELECT 1 FROM pokedex WHERE nome_pokemon = 'squirtle'
);
