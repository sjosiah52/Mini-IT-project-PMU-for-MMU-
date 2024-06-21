import sqlite3

def init_db():
  with sqlite3.connect("users.db") as conn:
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mmu_id TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """)
    conn.commit()

if __name__== "__main__":
    init_db()

