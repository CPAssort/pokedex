import os
from typing import Optional

import psycopg2
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from psycopg2.extensions import connection

from battle import calculate_battle_score, determine_winner

app = FastAPI(title="Pokédex Batalha")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "pokemon")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "arthur@123")


def get_connection() -> connection:
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


class PokemonBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100)
    tipo: str = Field(..., min_length=1, max_length=50)
    nivel: int = Field(..., ge=0)
    forca: int = Field(..., ge=0)


class PokemonEdit(BaseModel):
    nome: Optional[str] = Field(default=None, min_length=1, max_length=100)
    tipo: Optional[str] = Field(default=None, min_length=1, max_length=50)
    nivel: Optional[int] = Field(default=None, ge=0)
    forca: Optional[int] = Field(default=None, ge=0)


class BattleRequest(BaseModel):
    primeiro: str
    segundo: str


@app.get("/pokemon")
def list_pokemon():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT nome_pokemon, tipo_pokemon, nivel_pokemon, forca_pokemon "
                "FROM pokedex ORDER BY nome_pokemon"
            )
            return [
                {
                    "nome": name,
                    "tipo": pokemon_type,
                    "nivel": level,
                    "forca": force,
                }
                for name, pokemon_type, level, force in cursor.fetchall()
            ]


@app.post("/insert", status_code=status.HTTP_201_CREATED)
def insert_pokemon(pokemon: PokemonBase):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO pokedex "
                "(nome_pokemon, tipo_pokemon, nivel_pokemon, forca_pokemon) "
                "VALUES (%s, %s, %s, %s) RETURNING nome_pokemon",
                (pokemon.nome, pokemon.tipo, pokemon.nivel, pokemon.forca),
            )
            name = cursor.fetchone()[0]
    return {"message": "Pokémon inserido", "nome": name}


@app.put("/edit/{nome}")
def edit_pokemon(nome: str, pokemon: PokemonEdit):
    if (
        pokemon.nome is None
        and pokemon.tipo is None
        and pokemon.nivel is None
        and pokemon.forca is None
    ):
        raise HTTPException(status_code=400, detail="Informe pelo menos um campo para editar")

    updates = {
        "nome_pokemon": pokemon.nome or nome,
        "tipo_pokemon": pokemon.tipo,
        "nivel_pokemon": pokemon.nivel,
        "forca_pokemon": pokemon.forca,
    }
    updates = {key: value for key, value in updates.items() if value is not None}
    set_clause = ", ".join(f"{key} = %s" for key in updates)
    values = list(updates.values()) + [nome]

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                f"UPDATE pokedex SET {set_clause} WHERE nome_pokemon = %s "
                "RETURNING nome_pokemon",
                values,
            )
            updated = cursor.fetchone()
            if updated is None:
                raise HTTPException(status_code=404, detail="Pokémon não encontrado")
    return {"message": "Pokémon atualizado", "nome": updated[0]}


@app.delete("/delete/{nome}")
def delete_pokemon(nome: str):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM pokedex WHERE nome_pokemon = %s RETURNING nome_pokemon",
                (nome,),
            )
            deleted = cursor.fetchone()
            if deleted is None:
                raise HTTPException(status_code=404, detail="Pokémon não encontrado")
    return {"message": "Pokémon deletado", "nome": deleted[0]}


@app.post("/battle")
def battle(request: BattleRequest):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT nome_pokemon, nivel_pokemon, forca_pokemon FROM pokedex "
                "WHERE nome_pokemon IN (%s, %s)",
                (request.primeiro, request.segundo),
            )
            rows = {name: (level, force) for name, level, force in cursor.fetchall()}

    if request.primeiro not in rows or request.segundo not in rows:
        raise HTTPException(status_code=404, detail="Um ou ambos os Pokémons não foram encontrados")

    first_level, first_force = rows[request.primeiro]
    second_level, second_force = rows[request.segundo]
    result = determine_winner(
        first_level, first_force, second_level, second_force
    )
    return {
        "primeiro": request.primeiro,
        "segundo": request.segundo,
        **result,
    }
