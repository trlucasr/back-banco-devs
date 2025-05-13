from typing import Union
from fastapi import FastAPI
from clientes import router as clientes_router

app = FastAPI()

@app.get("/")
def welcome_banco_devs():
    return {"Banco Devs": "Servidor Rodando"}

app.include_router(clientes_router, prefix="/api")