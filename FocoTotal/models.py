from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

# Modelos para Matérias
class MateriaIn(BaseModel):
    nome_materia: str = Field(max_length=100)
    nome_professor: str | None = Field(default=None, max_length=100)

class MateriaOut(MateriaIn):
    id: int
    tempo_total: int = 0

# Modelos para Recursos
class RecursoIn(BaseModel):
    titulo: str = Field(max_length=200)
    link_url: str = Field(max_length=500)
    tipo_recurso: str | None = Field(default=None, max_length=50)

class RecursoOut(RecursoIn):
    id: int
    materia_id: int

# Modelos para Sessões de Estudo
class SessaoEstudoIn(BaseModel):
    duracao_minutos: int = Field(gt=0)
    descricao: str | None = None
    data_sessao: datetime | None = None

class SessaoEstudoOut(SessaoEstudoIn):
    id: int
    data_sessao: datetime
    materia_id: int

# Modelo para Resposta de Sumário
class SumarioEstudoOut(BaseModel):
    total_minutos: int
    total_pontos_foco: int
    sessoes: List[SessaoEstudoOut]

# Modelo para Respostas Simples
class MensagemSimples(BaseModel):
    detail: str

# Modelos para Usuários
class UsuarioIn(BaseModel):
    username: str
    email: str
    password: str

class UsuarioOut(BaseModel):
    id: int
    username: str
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

# Modelos para Tarefas
class TarefaIn(BaseModel):
    descricao: str
    concluida: bool = False

class TarefaOut(TarefaIn):
    id: int
    materia_id: int

# Modelos para Metas
class MetaIn(BaseModel):
    horas_alvo: int
    periodo: str = "semanal"

class MetaOut(MetaIn):
    id: int
    materia_id: int

# Modelos para Anotações
class AnotacaoIn(BaseModel):
    conteudo: str

class AnotacaoOut(AnotacaoIn):
    id: int
    data_criacao: datetime
    materia_id: int
