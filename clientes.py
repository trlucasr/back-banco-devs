from typing import Union, Optional
from fastapi import Depends, Body, APIRouter
from pydantic import BaseModel
from db import Database

router = APIRouter()
db = Database()

class Cliente(BaseModel):
    id: int = None
    id_conta: int = None
    nome_completo: str
    cgc: str
    senha: str
    endereco: str
    numero: str
    cidade: str
    uf: str
    telefone: str
    email: str
    status: str = None


def validaRequest(body, endpoint):

    """
    Validates the request body based on the specified endpoint.

    Args:
    - body: The request body containing client information.
    - endpoint (str): The endpoint for which the validation is being performed. 
      Expected values are "create_cliente" and "alterar_cliente".

    Returns:
    - dict: A dictionary containing the status code and a message.
      - For "create_cliente", if `id_conta` or `id` is provided and greater than 0, 
        it resets them and returns status 4001 with a message indicating that `id` 
        should not be sent in the request.
      - For "alterar_cliente", currently does not perform any validation.
      - If validation passes, returns status 2000 with message "OK".
    """

    if endpoint == "create_cliente":
        if body.id_conta is not None and body.id_conta > 0:
            body.id_conta = 0

        if body.id is not None and body.id > 0:
            body.id = 0
            return {"status": 4001, "mensagem": "id não deve ser enviado na requisição."}

    if endpoint == "alterar_cliente":
        pass

    return {"status": 2000, "mensagem": "OK"}

    

@router.post("/cliente/", tags=["Clientes"])
async def criar_cliente(body: Cliente):

    """
    Cria um novo cliente.

    Args:
    - body (Cliente): Informações do novo cliente.

    Returns:
    - dict: Resultado da query.
    """
    r_valid = validaRequest(body, "create_cliente")

    print(r_valid)

    if r_valid["status"] > 4000:
        return {"status": r_valid["status"], "mensagem": r_valid["mensagem"]} 

    body.status = "R"
        
    query = """INSERT INTO clientes
    (id_conta, nome_completo, cgc, senha, endereco, numero, cidade, uf, telefone, email, status)
    VALUES ( {},'{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(
        0,
        body.nome_completo,
        body.cgc,
        body.senha,
        body.endereco,
        body.numero,
        body.cidade,
        body.uf,
        body.telefone,
        body.email,
        body.status
    )

    result = db.query(
        query=query,
        autoCommit=True,
    )

    print(result)

    return {"result": result}

@router.get("/cliente/", tags=["Clientes"])
async def buscar_clientes(id: Optional[int] = None):

    """
    Busca um ou todos os clientes.

    Args:
    - id (Optional[int]): ID do cliente a ser buscado. Se None, retorna todos os clientes.

    Returns:
    - dict: Resultado da query.
    """
    if id is None:
        return db.query(query=f"SELECT * FROM clientes;")
    else:
        return db.query(query=f"SELECT * FROM clientes WHERE id = {id};")
    
@router.delete("/cliente/", tags=["Clientes"])
async def deletar_cliente(id: int):
    """
    Deleta um cliente.

    Args:
    - id (int): ID do cliente a ser deletado.
    """
    return db.query(query=f"DELETE FROM clientes WHERE id = {id};", autoCommit=True)

@router.put("/cliente/", tags=["Clientes"])
async def atualizar_cliente(body: Cliente):
    
    """
    Atualiza um cliente existente.

    Args:
    - body (Cliente): Conteúdo da requisição com as informações do cliente.

    Returns:
    - dict: Contendo o status da operação e uma mensagem de erro,
      caso haja algum problema na requisição.
    """

    r_valid = validaRequest(body, "alterar_cliente")

    print(r_valid)

    if r_valid["status"] > 4000:
        return {"status": r_valid["status"], "mensagem": r_valid["mensagem"]} 

    