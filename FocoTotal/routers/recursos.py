from fastapi import APIRouter, HTTPException
from typing import List
from .. import database, models
from .materias import get_materia_or_404

router = APIRouter(
    prefix="/recursos",
    tags=["recursos"],
)


@router.post("/materias/{materia_id}/recursos", response_model=models.RecursoOut)
async def create_recurso_for_materia(materia_id: int, recurso: models.RecursoIn):
    _ = await get_materia_or_404(materia_id)

    limite_recursos = 20
    count_query = """
        SELECT COUNT(1) AS total
        FROM recursos
        WHERE materia_id = :materia_id;
    """
    total_recursos = await database.database.fetch_one(
        query=count_query,
        values={"materia_id": materia_id},
    )
    if total_recursos and int(total_recursos["total"]) >= limite_recursos:
        raise HTTPException(
            status_code=400,
            detail=f"Cada matéria pode ter no máximo {limite_recursos} recursos. Apague algum antes de adicionar novos.",
        )

    insert_query = """
        INSERT INTO recursos (titulo, link_url, tipo_recurso, materia_id)
        VALUES (:titulo, :link_url, :tipo_recurso, :materia_id)
        RETURNING id, titulo, link_url, tipo_recurso, materia_id;
    """
    values = {**recurso.model_dump(), "materia_id": materia_id}
    row = await database.database.fetch_one(query=insert_query, values=values)
    return row


@router.get("/materias/{materia_id}/recursos", response_model=List[models.RecursoOut])
async def get_recursos_for_materia(materia_id: int):
    _ = await get_materia_or_404(materia_id)

    query_recursos = """
        SELECT id, titulo, link_url, tipo_recurso, materia_id
        FROM recursos
        WHERE materia_id = :materia_id;
    """
    recursos_list = await database.database.fetch_all(
        query=query_recursos,
        values={"materia_id": materia_id},
    )
    return recursos_list


@router.delete("/{recurso_id}", response_model=models.MensagemSimples)
async def delete_recurso(recurso_id: int):
    select_query = "SELECT * FROM recursos WHERE id = :id;"
    recurso_existente = await database.database.fetch_one(
        query=select_query,
        values={"id": recurso_id},
    )

    if recurso_existente is None:
        raise HTTPException(status_code=404, detail="Recurso não encontrado.")

    delete_query = "DELETE FROM recursos WHERE id = :id;"
    await database.database.execute(query=delete_query, values={"id": recurso_id})

    return {"detail": "Recurso apagado com sucesso."}
