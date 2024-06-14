import sqlite3

def init2_db():
    with sqlite3.connect("driver.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS drivers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mmu_id TEXT NOT NULL UNIQUE,
            ic_number TEXT NOT NULL,
            vehicle_registration_number TEXT NOT NULL,
            password TEXT NOT NULL
        )
        """)
        conn.commit()

if __name__== "__main__":
    init2_db()
