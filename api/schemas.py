from typing import Optional

from pydantic import BaseModel, Field


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
