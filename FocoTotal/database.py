from databases import Database
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "focototal.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

database = Database(DATABASE_URL)


def init_sqlite_db() -> None:
	"""Cria o arquivo e as tabelas no SQLite, caso ainda não existam."""

	DB_PATH.parent.mkdir(parents=True, exist_ok=True)

	conn = sqlite3.connect(DB_PATH)
	try:
		cursor = conn.cursor()

		cursor.executescript(
			"""
			CREATE TABLE IF NOT EXISTS usuarios (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				username VARCHAR(50) NOT NULL UNIQUE,
				email VARCHAR(100) NOT NULL UNIQUE,
				senha_hash VARCHAR(200) NOT NULL
			);

			CREATE TABLE IF NOT EXISTS materias (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				nome_materia VARCHAR(100) NOT NULL,
				nome_professor VARCHAR(100),
				usuario_id INTEGER,
				FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
				UNIQUE(nome_materia, usuario_id)
			);

			CREATE TABLE IF NOT EXISTS recursos (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				titulo VARCHAR(200) NOT NULL,
				link_url VARCHAR(500) NOT NULL,
				tipo_recurso VARCHAR(50),
				materia_id INTEGER,
				FOREIGN KEY (materia_id) REFERENCES materias(id) ON DELETE CASCADE
			);

			CREATE TABLE IF NOT EXISTS sessoes_estudo (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				duracao_minutos INTEGER NOT NULL,
				data_sessao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
				descricao TEXT,
				materia_id INTEGER,
				FOREIGN KEY (materia_id) REFERENCES materias(id) ON DELETE CASCADE
			);

			CREATE TABLE IF NOT EXISTS tarefas (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				descricao VARCHAR(200) NOT NULL,
				concluida BOOLEAN DEFAULT 0,
				materia_id INTEGER,
				FOREIGN KEY (materia_id) REFERENCES materias(id) ON DELETE CASCADE
			);

			CREATE TABLE IF NOT EXISTS metas (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				horas_alvo INTEGER NOT NULL,
				periodo VARCHAR(20) DEFAULT 'semanal',
				materia_id INTEGER,
				FOREIGN KEY (materia_id) REFERENCES materias(id) ON DELETE CASCADE
			);

			CREATE TABLE IF NOT EXISTS anotacoes (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				conteudo TEXT NOT NULL,
				data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
				materia_id INTEGER,
				FOREIGN KEY (materia_id) REFERENCES materias(id) ON DELETE CASCADE
			);
			"""
		)

		conn.commit()
	finally:
		conn.close()
