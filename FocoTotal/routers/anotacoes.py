from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..database import database
from ..models import AnotacaoIn, AnotacaoOut, UsuarioOut
from .auth import get_current_user
from datetime import datetime

router = APIRouter(
    prefix="/anotacoes",
    tags=["Anotações"]
)

@router.post("/", response_model=AnotacaoOut)
async def criar_anotacao(anotacao: AnotacaoIn, materia_id: int, current_user: UsuarioOut = Depends(get_current_user)):
    query = """
        INSERT INTO anotacoes (conteudo, materia_id)
        VALUES (:conteudo, :materia_id)
    """
    values = {"conteudo": anotacao.conteudo, "materia_id": materia_id}
    last_record_id = await database.execute(query=query, values=values)
    
    # Fetch created to get timestamp
    query_get = "SELECT * FROM anotacoes WHERE id = :id"
    return await database.fetch_one(query=query_get, values={"id": last_record_id})

@router.get("/", response_model=List[AnotacaoOut])
async def listar_anotacoes(materia_id: int, current_user: UsuarioOut = Depends(get_current_user)):
    query = "SELECT * FROM anotacoes WHERE materia_id = :materia_id"
    return await database.fetch_all(query=query, values={"materia_id": materia_id})
