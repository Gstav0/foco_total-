from fastapi import APIRouter, HTTPException
from sqlite3 import IntegrityError as SQLiteIntegrityError
from databases.interfaces import Record
from typing import List
from .. import database, models

router = APIRouter(
    prefix="/materias",
    tags=["matérias"],
)


async def get_materia_or_404(materia_id: int):
    query = "SELECT * FROM materias WHERE id = :id;"
    materia = await database.database.fetch_one(query=query, values={"id": materia_id})
    if materia is None:
        raise HTTPException(status_code=404, detail="Matéria não encontrada.")
    return materia


@router.post("/", response_model=models.MateriaOut)
async def create_materia(materia: models.MateriaIn):
    if (
        ("avançado" in materia.nome_materia.lower() or "projeto final" in materia.nome_materia.lower())
        and not (materia.nome_professor and materia.nome_professor.strip())
    ):
        raise HTTPException(
            status_code=400,
            detail="Matérias avançadas ou de Projeto Final devem ter um professor definido.",
        )

    query = """
        INSERT INTO materias (nome_materia, nome_professor)
        VALUES (:nome_materia, :nome_professor)
        RETURNING id, nome_materia, nome_professor;
    """

    try:
        row: Record | None = await database.database.fetch_one(
            query=query,
            values=materia.model_dump(),
        )
    except Exception as exc:  # databases encapsula a IntegrityError original
        message = str(exc)
        if "UNIQUE constraint failed" in message or "unique" in message.lower():
            raise HTTPException(
                status_code=400,
                detail="Já existe uma matéria com esse nome.",
            )
        raise

    if row is None:
        raise HTTPException(status_code=500, detail="Falha ao criar matéria.")

    return row


@router.get("/", response_model=List[models.MateriaOut])
async def get_all_materias():
    query = """
        SELECT 
            m.id, 
            m.nome_materia, 
            m.nome_professor,
            COALESCE(SUM(s.duracao_minutos), 0) as tempo_total
        FROM materias m
        LEFT JOIN sessoes_estudo s ON m.id = s.materia_id
        GROUP BY m.id
        ORDER BY m.id DESC;
    """
    materias_list = await database.database.fetch_all(query=query)
    return materias_list


@router.get("/{materia_id}", response_model=models.MateriaOut)
async def get_one_materia(materia_id: int):
    materia = await get_materia_or_404(materia_id)
    return materia


@router.put("/{materia_id}", response_model=models.MateriaOut)
async def update_materia(materia_id: int, materia_update: models.MateriaIn):
    _ = await get_materia_or_404(materia_id)

    if (
        ("avançado" in materia_update.nome_materia.lower() or "projeto final" in materia_update.nome_materia.lower())
        and not (materia_update.nome_professor and materia_update.nome_professor.strip())
    ):
        raise HTTPException(
            status_code=400,
            detail="Matérias avançadas ou de Projeto Final devem ter um professor definido.",
        )

    update_query = """
        UPDATE materias
        SET nome_materia = :nome_materia,
            nome_professor = :nome_professor
        WHERE id = :id
        RETURNING id, nome_materia, nome_professor;
    """
    values = {"id": materia_id, **materia_update.model_dump()}
    row = await database.database.fetch_one(query=update_query, values=values)
    return row


@router.delete("/{materia_id}", response_model=models.MensagemSimples)
async def delete_materia(materia_id: int):
    _ = await get_materia_or_404(materia_id)

    # Regra de negócio: impedir apagar matérias que tenham sessões de estudo
    sessoes_query = "SELECT COUNT(1) AS total FROM sessoes_estudo WHERE materia_id = :id;"
    sessoes = await database.database.fetch_one(
        query=sessoes_query,
        values={"id": materia_id},
    )

    if sessoes and int(sessoes["total"]) > 0:
        raise HTTPException(
            status_code=400,
            detail="Não é possível apagar uma matéria que possui sessões de estudo registradas.",
        )

    delete_query = "DELETE FROM materias WHERE id = :id;"
    await database.database.execute(query=delete_query, values={"id": materia_id})

    return {"detail": "Matéria apagada com sucesso."}
