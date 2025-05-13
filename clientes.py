from typing import Union
from fastapi import Depends, Body, APIRouter
from pydantic import BaseModel
from db import Database

router = APIRouter()
db = Database()

class Cliente(BaseModel):
    id: int
    id_conta: int
    nome_cliente: str
    cgc: str
    senha: str
    endereco: str
    numero: str
    cidade: str
    uf: str
    telefone: str
    email: str
    status: str


def clienteVld(body):

    print(body)

    if body.id_conta is None or body.id_conta == 0:
        return {"status": 4001, "mensagem": "id_conta não informado ou zerado."}
    

@router.post("/cliente/", tags=["Clientes"])
async def create_cliente(body: Cliente):

    r_valid = clienteVld(body)

    print(r_valid)

    if r_valid["status"] > 4000:
        return {"status": r_valid["status"], "mensagem": r_valid["mensagem"]}  

    # query = """INSERT INTO clientes
    # (nome_cliente, telefone, email, cgc, ativo, created_at, user_inc)
    # VALUES ('{}', '{}', '{}', '{}', {}, '{}', {})""".format(
    #     nome_cliente, telefone, email, cgc, ativo, created_at, user_inc
    # )

#    return {"result": body}
