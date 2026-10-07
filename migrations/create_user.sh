#!/bin/bash
set -e

# Executa o comando SQL injetando as variáveis $DB_USER e $DB_PASSWORD do .env
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "pokemon" <<-EOSQL
    CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
    GRANT CONNECT ON DATABASE pokemon TO $DB_USER;
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE pokedex TO $DB_USER;
EOSQL