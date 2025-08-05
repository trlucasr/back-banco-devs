from typing import Union, Optional
from fastapi import Depends, Body, APIRouter
from pydantic import BaseModel
from db import Database
from datetime import date, time

router = APIRouter()
db = Database()

class TransferenciaPost(BaseModel):
    id: int = None
    id_origem: int
    id_destino: str
    valor: str
    date: date
    hora: time
    tipo: str
    status: str

class TransferenciaPut(BaseModel):
    id: int
    status: str = None


def validaRequest(body, endpoint):

    if endpoint == "create_transferencia":
        if body.id_origem is None or body.id_origem == 0:
            body.id_origem = 0

        if body.id_destino is None or body.id_destino == 0:
            body.id_destino = 0

        if body.id is not None and body.id > 0:
            body.id = 0
            return {"status": 4001, "mensagem": "id não deve ser enviado na requisição."}

    if endpoint == "alterar_transferencia":
        if body["id"] is None or body["id"] == 0:
            body["id"] = 0
            return {"status": 4002, "mensagem": "id é obrigatório e não pode ser zerado para executar essa requisição."}

    return {"status": 2000, "mensagem": "OK"}

    
@router.post("/transferencia/", tags=["Transferencias"])
async def criar_transferencia(body: TransferenciaPost):

    """
    Cria uma nova transferencia.

    Args:
    - body (Transferencia): Informações da nova transferencia.

    Returns:
    - dict: Resultado da query.
    """
    r_valid = validaRequest(body, "create_transferencia")

    print(r_valid)

    if r_valid["status"] > 4000:
        return {"status": r_valid["status"], "mensagem": r_valid["mensagem"]} 

    body.status = "T"
        
    query = """INSERT INTO transferencia
    (id_origem, id_destino, valor, date, hora, tipo, status)
    VALUES ( {}, {}, {}, '{}', '{}', '{}', '{}')""".format(
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

@router.get("/transferencia/", tags=["Transferencias"])
async def buscar_transferencia(id: Optional[int] = None):

    """
    Busca um ou todos as Transferencias.

    Args:
    - id (Optional[int]): ID da transferencia a ser buscado. Se None, retorna todas as transferencias.

    Returns:
    - dict: Resultado da query.
    """
    if id is None:
        return db.query(query=f"SELECT * FROM transferencias;")
    else:
        return db.query(query=f"SELECT * FROM transferencias WHERE id = {id};")
    
@router.delete("/transferencia/", tags=["Transferencias"])
async def deletar_transferencia(id: int):
    """
    Deleta uma transferencia.

    Args:
    - id (int): ID da transferencia a ser deletado.
    """
    return db.query(query=f"DELETE FROM transferencias WHERE id = {id};", autoCommit=True)

@router.put("/transferencia/", tags=["Transferencias"])
async def atualizar_transferencia(body: TransferenciaPut):
    
    """
    Atualiza uma transferencia existente.

    Args:
    - body (Conta): Conteúdo da requisição com as informações da transferencia.

    Returns:
    - dict: Contendo o status da operação e uma mensagem de erro,
      caso haja algum problema na requisição.
    """    

    body = body.dict() 

    r_valid = validaRequest(body, "alterar_transferencia")

    print(r_valid)

    if r_valid["status"] > 4000:
        return {"status": r_valid["status"], "mensagem": r_valid["mensagem"]}

    query = """UPDATE transferencias SET """

    if body.get("status"):
        query += "status = '{}', ".format(body["status"])

    query = query.rstrip(", ") + " WHERE id = {}".format(body["id"])

    return db.query(
        query=query,
        autoCommit=True,
    )