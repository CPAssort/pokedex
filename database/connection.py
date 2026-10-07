import os

import psycopg2
from psycopg2.extensions import connection


def get_connection() -> connection:
    password = os.getenv("DB_PASSWORD")
    if not password:
        raise RuntimeError("DB_PASSWORD não está configurado")

    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        dbname=os.getenv("DB_NAME", "pokemon"),
        user=os.getenv("DB_USER", "postgres"),
        password=password,
    )
