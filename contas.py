from typing import Union, Optional
from fastapi import Depends, Body, APIRouter
from pydantic import BaseModel
from db import Database

router = APIRouter()
db = Database()

class ContaPost(BaseModel):
    id: int = None
    id_cliente: int = None
    banco: str
    agencia: str
    cc: str
    status: str = None

class ContaPut(BaseModel):
    id: int 
    banco: str = None
    agencia: str = None
    cc: str = None
    status: str = None


def validaRequest(body, endpoint):

    if endpoint == "create_conta":
        if body.id_cliente is None or body.id_cliente == 0:
            body.id_cliente = 0

        if body.id is not None and body.id > 0:
            body.id = 0
            return {"status": 4001, "mensagem": "id não deve ser enviado na requisição."}

    if endpoint == "alterar_conta":
        if body["id"] is None or body["id"] == 0:
            body["id"] = 0
            return {"status": 4002, "mensagem": "id é obrigatório e não pode ser zerado para executar essa requisição."}

    return {"status": 2000, "mensagem": "OK"}

    
@router.post("/conta/", tags=["Contas"])
async def criar_conta(body: ContaPost):

    """
    Cria uma nova conta.

    Args:
    - body (Conta): Informações da nova conta.

    Returns:
    - dict: Resultado da query.
    """
    r_valid = validaRequest(body, "create_conta")

    print(r_valid)

    if r_valid["status"] > 4000:
        return {"status": r_valid["status"], "mensagem": r_valid["mensagem"]} 

    body.status = "R"
        
    query = """INSERT INTO contas
    (id_cliente, banco, agencia, cc, status)
    VALUES ( {},'{}', '{}', '{}', '{}')""".format(
        body.id_cliente,
        body.banco,
        body.agencia,
        body.cc,
        body.status
    )

    result = db.query(
        query=query,
        autoCommit=True,
    )

    print(result)

    return {"result": result}

@router.get("/conta/", tags=["Contas"])
async def buscar_contas(id: Optional[int] = None):

    """
    Busca um ou todos as Contas.

    Args:
    - id (Optional[int]): ID da conta a ser buscado. Se None, retorna todas as contas.

    Returns:
    - dict: Resultado da query.
    """
    if id is None:
        return db.query(query=f"SELECT * FROM contas;")
    else:
        return db.query(query=f"SELECT * FROM contas WHERE id = {id};")
    
@router.delete("/conta/", tags=["Contas"])
async def deletar_conta(id: int):
    """
    Deleta uma conta.

    Args:
    - id (int): ID da conta a ser deletado.
    """
    return db.query(query=f"DELETE FROM contas WHERE id = {id};", autoCommit=True)

@router.put("/conta/", tags=["Contas"])
async def atualizar_conta(body: ContaPut):
    
    """
    Atualiza uma conta existente.

    Args:
    - body (Conta): Conteúdo da requisição com as informações da conta.

    Returns:
    - dict: Contendo o status da operação e uma mensagem de erro,
      caso haja algum problema na requisição.
    """    

    body = body.dict() 

    r_valid = validaRequest(body, "alterar_conta")

    print(r_valid)

    if r_valid["status"] > 4000:
        return {"status": r_valid["status"], "mensagem": r_valid["mensagem"]}

    body["status"] = "R"

    query = """UPDATE contas SET """

    if body.get("banco"):
        query += "banco = '{}', ".format(body["banco"])
    if body.get("agencia"):
        query += "agencia = '{}', ".format(body["agencia"])
    if body.get("cc"):
        query += "cc = '{}', ".format(body["cc"])
    if body.get("status"):
        query += "status = '{}', ".format(body["status"])

    query = query.rstrip(", ") + " WHERE id = {}".format(body["id"])

    return db.query(
        query=query,
        autoCommit=True,
    )