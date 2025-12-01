from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from .database import database, init_sqlite_db
from .routers import materias, recursos, sessoes, auth, tarefas, metas, anotacoes
from . import models
from .auth_utils import get_password_hash

app = FastAPI(
    title="FocoTotal API",
    description="API para gerir sessões de estudo e recursos.",
    version="0.1.0"
)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    init_sqlite_db()
    await database.connect()
    
    # Criar usuário admin padrão se não existir
    query = "SELECT * FROM usuarios WHERE username = :username"
    user = await database.fetch_one(query=query, values={"username": "admin"})
    if not user:
        hashed_password = get_password_hash("admin")
        query = "INSERT INTO usuarios(username, email, senha_hash) VALUES (:username, :email, :senha_hash)"
        values = {"username": "admin", "email": "admin@example.com", "senha_hash": hashed_password}
        await database.execute(query=query, values=values)

    # Criar matérias de exemplo se não existirem
    query_materias = "SELECT COUNT(*) as total FROM materias"
    result = await database.fetch_one(query=query_materias)
    if result["total"] == 0:
        materias_demo = [
            {"nome_materia": "Design de Interfaces", "nome_professor": "Prof. Gustavo"},
            {"nome_materia": "Desenvolvimento Web", "nome_professor": "Prof. Silva"},
            {"nome_materia": "Gestão de Projetos", "nome_professor": "Prof. Mendes"}
        ]
        query_insert = "INSERT INTO materias (nome_materia, nome_professor) VALUES (:nome_materia, :nome_professor)"
        await database.execute_many(query=query_insert, values=materias_demo)

@app.on_event("shutdown")
async def shutdown_db_client():
    await database.disconnect()

# @app.get("/")
# def read_root():
#     return {"status": "online", "projeto": "FocoTotal API"}

app.include_router(materias.router)
app.include_router(recursos.router)
app.include_router(sessoes.router)
app.include_router(auth.router)
app.include_router(tarefas.router)
app.include_router(metas.router)
app.include_router(anotacoes.router)

# Montar arquivos estáticos (Frontend)
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")