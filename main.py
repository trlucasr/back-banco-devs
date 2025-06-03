from typing import Union
from fastapi import FastAPI
from clientes import router as clientes_router

app = FastAPI( 
    title="Banco Devs",
    description="Banco Financeiro que realiza transações bancárias entre contas cadastradas",
    version="1.0.0")

@app.get("/")
def welcome_banco_devs():
    return {"Banco Devs": "Servidor Rodando"}

app.include_router(clientes_router, prefix="/api")