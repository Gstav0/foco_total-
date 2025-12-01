from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
from .. import database, models
from .materias import get_materia_or_404

router = APIRouter(
    prefix="/sessoes",
    tags=["sessões de estudo"],
)


MINUTOS_MINIMOS_SESSAO = 1
LIMITE_MINUTOS_SESSAO_SEM_DESCRICAO = 90


@router.post("/materias/{materia_id}/sessoes", response_model=models.SessaoEstudoOut)
async def create_sessao_for_materia(materia_id: int, sessao: models.SessaoEstudoIn):
    _ = await get_materia_or_404(materia_id)

    if sessao.duracao_minutos < MINUTOS_MINIMOS_SESSAO:
        raise HTTPException(
            status_code=400,
            detail=f"A duração mínima de uma sessão é de {MINUTOS_MINIMOS_SESSAO} minutos.",
        )

    if sessao.duracao_minutos > LIMITE_MINUTOS_SESSAO_SEM_DESCRICAO and not (
        sessao.descricao and sessao.descricao.strip()
    ):
        raise HTTPException(
            status_code=400,
            detail=f"Sessões com mais de {LIMITE_MINUTOS_SESSAO_SEM_DESCRICAO} minutos devem ter uma descrição.",
        )

    agora = datetime.now(timezone.utc)
    
    if sessao.data_sessao is not None:
        sessao_dt = sessao.data_sessao
        # Se vier sem fuso horário (naive), assumimos UTC para comparação
        if sessao_dt.tzinfo is None:
            sessao_dt = sessao_dt.replace(tzinfo=timezone.utc)
            
        if sessao_dt > agora:
            raise HTTPException(
                status_code=400,
                detail="Não é permitido registrar sessões de estudo em data/hora futura.",
            )

    insert_query = """
        INSERT INTO sessoes_estudo (duracao_minutos, descricao, data_sessao, materia_id)
        VALUES (:duracao_minutos, :descricao, COALESCE(:data_sessao, CURRENT_TIMESTAMP), :materia_id)
        RETURNING id, duracao_minutos, descricao, data_sessao, materia_id;
    """
    values = {**sessao.model_dump(), "materia_id": materia_id}
    row = await database.database.fetch_one(query=insert_query, values=values)
    return row


@router.get("/materias/{materia_id}/sumario", response_model=models.SumarioEstudoOut)
async def get_sumario_for_materia(materia_id: int):
    _ = await get_materia_or_404(materia_id)

    query_sessoes = """
        SELECT id, duracao_minutos, descricao, data_sessao, materia_id
        FROM sessoes_estudo
        WHERE materia_id = :materia_id
        ORDER BY data_sessao DESC;
    """
    sessoes_list = await database.database.fetch_all(
        query=query_sessoes,
        values={"materia_id": materia_id},
    )

    total_minutos = sum(sessao["duracao_minutos"] for sessao in sessoes_list)
    total_pontos_foco = total_minutos // 10

    return {
        "total_minutos": total_minutos,
        "total_pontos_foco": total_pontos_foco,
        "sessoes": sessoes_list,
    }
