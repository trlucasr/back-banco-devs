from typing import Union, Optional
from fastapi import Depends, Body, APIRouter
from pydantic import BaseModel
from db import Database
from datetime import date, time

router = APIRouter()
db = Database()

class SaldoPost(BaseModel):
    id: int = None
    id_cliente: int
    id_conta: int
    valor: float
    data: date

class SaldoPut(BaseModel):
    id: int
    valor: float
    data: date



def validaRequest(body, endpoint):

    if endpoint == "create_saldo":
        if body.id_cliente is None or body.id_cliente == 0:
            body.id_cliente = 0

        if body.id_conta is None or body.id_conta == 0:
            body.id_conta = 0

        if body.valor is None or body.valor < 0:
            body.valor = 0.0

        if body.id is not None and body.id > 0:
            body.id = 0
            return {"status": 4001, "mensagem": "id não deve ser enviado na requisição."}

        # # verifico se o id da conta existe no banco         
        # query=f"SELECT id_conta FROM saldo WHERE id_conta = {body.id_conta};"

        # result = db.query(
        #     query=query,
        #     autoCommit=True,
        # )

        # print(result)
        # return {"status": 4005, "mensagem": "OK"}

        # if result[0][0] > 0:
        #     return {"status": 4003, "mensagem": "ja existe saldo cadastrado para essa conta."}        

    if endpoint == "alterar_saldo":
        if body["id"] is None or body["id"] == 0:
            body["id"] = 0
            return {"status": 4002, "mensagem": "id é obrigatório e não pode ser zerado para executar essa requisição."}

    return {"status": 2000, "mensagem": "OK"}


@router.post("/saldo/", tags=["Saldos"])
async def criar_Saldo(body: SaldoPost):

    """
    Cria uma nova saldo.

    Args:
    - body (SaldoPost): Informações do novo saldo.

    Returns:
    - dict: Resultado da query.
    """
    r_valid = validaRequest(body, "create_saldo")

    print(r_valid)

    if r_valid["status"] > 4000:
        return {"status": r_valid["status"], "mensagem": r_valid["mensagem"]} 


    query = """INSERT INTO saldo
    (id_cliente, id_conta, valor, data)
    VALUES ( {}, {}, {}, '{}')""".format(
        body.id_cliente,
        body.id_conta,
        body.valor,
        body.data
    )

    result = db.query(
        query=query,
        autoCommit=True,
    )

    print(result)

    return {"result": result}

@router.get("/saldo/", tags=["Saldos"])
async def buscar_saldo(id_conta: Optional[int] = None):

    """
    Busca um ou todos as saldo.

    Args:
    - id (Optional[int]): ID da saldo a ser buscado. Se None, retorna todas os saldos.

    Returns:
    - dict: Resultado da query.
    """
    if id_conta is None or id_conta <= 0 :
        return {"status": 4004, "mensagem": "id_conta está inválido ou nulo, não é possível executar essa requisição."}
    else:
        return db.query(query=f"SELECT * FROM saldo WHERE id_conta = {id_conta};")

@router.delete("/saldo/", tags=["Saldos"])
async def deletar_saldo(id_conta: int):
    """
    Deleta uma saldo.

    Args:
    - id (int): ID da Saldo a ser deletado.
    """
    return db.query(query=f"DELETE FROM saldo WHERE id_conta = {id_conta};", autoCommit=True)

@router.put("/saldo/", tags=["Saldos"])
async def atualizar_saldo(body: SaldoPut):

    """
    Atualiza uma saldo existente.

    Args:
    - body (Conta): Conteúdo da requisição com as informações da saldo.

    Returns:
    - dict: Contendo o status da operação e uma mensagem de erro,
      caso haja algum problema na requisição.
    """    

    body = body.dict() 

    r_valid = validaRequest(body, "alterar_saldo")

    print(r_valid)

    if r_valid["status"] > 4000:
        return {"status": r_valid["status"], "mensagem": r_valid["mensagem"]}

    query = """UPDATE saldo SET """

    if body.get("valor"):
        query += "valor = {}, ".format(body["valor"])
  
    if body.get("data"):
        query += "data = '{}', ".format(body["data"])

    query = query.rstrip(", ") + " WHERE id = {}".format(body["id"])

    return db.query(
        query=query,
        autoCommit=True,
    )