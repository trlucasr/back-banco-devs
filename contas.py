from typing import Union, Optional
from fastapi import Depends, Body, APIRouter
from pydantic import BaseModel
from db import Database

router = APIRouter()
db = Database()

class Conta(BaseModel):
    id: int = None
    id_cliente: int = None
    banco: str
    agencia: str
    cc: str
    status: str = None


def validaRequest(body, endpoint):

    if endpoint == "create_conta":
        if body.id_cliente is not None and body.id_cliente > 0:
            body.id_conta = 0

        if body.id is not None and body.id > 0:
            body.id = 0
            return {"status": 4001, "mensagem": "id não deve ser enviado na requisição."}

    if endpoint == "alterar_conta":
        pass

    return {"status": 2000, "mensagem": "OK"}

    

@router.post("/conta/", tags=["Contas"])
async def criar_conta(body: Conta):

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
        0,
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
async def atualizar_conta(body: Conta):
    
    """
    Atualiza uma conta existente.

    Args:
    - body (Conta): Conteúdo da requisição com as informações da conta.

    Returns:
    - dict: Contendo o status da operação e uma mensagem de erro,
      caso haja algum problema na requisição.
    """

    r_valid = validaRequest(body, "alterar_conta")

    print(r_valid)

    if r_valid["status"] > 4000:
        return {"status": r_valid["status"], "mensagem": r_valid["mensagem"]} 

    