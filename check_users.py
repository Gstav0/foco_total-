import sqlite3
from pathlib import Path

DB_PATH = Path("focototal.db").resolve()
print(f"Checking DB at: {DB_PATH}")

try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email FROM usuarios")
    users = cursor.fetchall()
    print("Users found:")
    for u in users:
        print(u)
    
    print("-" * 20)
    cursor.execute("SELECT * FROM usuarios WHERE username = 'Gustavo'")
    g = cursor.fetchone()
    print(f"User 'Gustavo': {g}")
    
    conn.close()
except Exception as e:
    print(f"Error: {e}")
