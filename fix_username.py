import sqlite3
from pathlib import Path

DB_PATH = Path("focototal.db").resolve()

try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET username = 'Gustavo' WHERE username = 'Gustavo '")
    conn.commit()
    print("Updated 'Gustavo ' to 'Gustavo'")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
