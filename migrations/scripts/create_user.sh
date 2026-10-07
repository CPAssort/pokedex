#!/bin/sh
set -eu

export PGPASSWORD="$POSTGRES_PASSWORD"

psql -v ON_ERROR_STOP=1 \
    --host "$DB_HOST" \
    --username "$POSTGRES_USER" \
    --dbname "$DB_NAME" \
    --set=db_user="$DB_USER" \
    --set=db_password="$DB_PASSWORD" <<EOSQL
SELECT format(
    'ALTER ROLE %I WITH LOGIN PASSWORD %L',
    :'db_user',
    :'db_password'
)
WHERE EXISTS (SELECT 1 FROM pg_roles WHERE rolname = :'db_user') \
\gexec

SELECT format(
    'CREATE ROLE %I LOGIN PASSWORD %L',
    :'db_user',
    :'db_password'
)
WHERE NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = :'db_user') \
\gexec

GRANT CONNECT ON DATABASE "$DB_NAME" TO :"db_user";
GRANT USAGE ON SCHEMA public TO :"db_user";
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE pokedex TO :"db_user";
EOSQL
