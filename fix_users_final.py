import sqlite3
from pathlib import Path

DB_PATH = Path("focototal.db").resolve()

try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Delete id 4
    cursor.execute("DELETE FROM usuarios WHERE id = 4")
    print("Deleted user id 4")
    
    # Update id 2
    cursor.execute("UPDATE usuarios SET username = 'Gustavo' WHERE id = 2")
    print("Updated user id 2 to 'Gustavo'")
    
    conn.commit()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
