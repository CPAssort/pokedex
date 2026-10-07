from fastapi import FastAPI

from api.routes import router

app = FastAPI(
    title="Pokédex Batalha",
    description="API para cadastrar, editar, excluir e combater Pokémons.",
    version="1.0.0",
)

app.include_router(router)
