from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..database import database
from ..models import TarefaIn, TarefaOut, UsuarioOut
from .auth import get_current_user

router = APIRouter(
    prefix="/tarefas",
    tags=["Tarefas"]
)

@router.post("/", response_model=TarefaOut)
async def criar_tarefa(tarefa: TarefaIn, materia_id: int, current_user: UsuarioOut = Depends(get_current_user)):
    # Verifica se a matéria existe
    query_materia = "SELECT * FROM materias WHERE id = :materia_id"
    materia = await database.fetch_one(query=query_materia, values={"materia_id": materia_id})
    if not materia:
         raise HTTPException(status_code=404, detail="Matéria não encontrada.")

    query = """
        INSERT INTO tarefas (descricao, concluida, materia_id)
        VALUES (:descricao, :concluida, :materia_id)
    """
    values = {**tarefa.dict(), "materia_id": materia_id}
    last_record_id = await database.execute(query=query, values=values)
    return {**values, "id": last_record_id}

@router.get("/", response_model=List[TarefaOut])
async def listar_tarefas(materia_id: int, current_user: UsuarioOut = Depends(get_current_user)):
    query = "SELECT * FROM tarefas WHERE materia_id = :materia_id"
    return await database.fetch_all(query=query, values={"materia_id": materia_id})

@router.put("/{tarefa_id}", response_model=TarefaOut)
async def atualizar_tarefa(tarefa_id: int, tarefa: TarefaIn, current_user: UsuarioOut = Depends(get_current_user)):
    query = """
        UPDATE tarefas
        SET descricao = :descricao, concluida = :concluida
        WHERE id = :id
    """
    values = {**tarefa.dict(), "id": tarefa_id}
    await database.execute(query=query, values=values)
    
    # Recuperar para retornar com materia_id correto
    query_get = "SELECT * FROM tarefas WHERE id = :id"
    return await database.fetch_one(query=query_get, values={"id": tarefa_id})
