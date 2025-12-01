from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..database import database
from ..models import MetaIn, MetaOut, UsuarioOut
from .auth import get_current_user

router = APIRouter(
    prefix="/metas",
    tags=["Metas"]
)

@router.post("/", response_model=MetaOut)
async def criar_meta(meta: MetaIn, materia_id: int, current_user: UsuarioOut = Depends(get_current_user)):
    query = """
        INSERT INTO metas (horas_alvo, periodo, materia_id)
        VALUES (:horas_alvo, :periodo, :materia_id)
    """
    values = {**meta.dict(), "materia_id": materia_id}
    last_record_id = await database.execute(query=query, values=values)
    return {**values, "id": last_record_id}

@router.get("/", response_model=List[MetaOut])
async def listar_metas(materia_id: int, current_user: UsuarioOut = Depends(get_current_user)):
    query = "SELECT * FROM metas WHERE materia_id = :materia_id"
    return await database.fetch_all(query=query, values={"materia_id": materia_id})
