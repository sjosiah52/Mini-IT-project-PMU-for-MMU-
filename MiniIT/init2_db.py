import sqlite3 

def init_db():
    with sqlite3.connect(drivers.db) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS drivers (
            id INTEGER PRIMARY KEYAUTOINCREMENT,
            mmu_id TEXT NOT NULL UNIQUE,
            ic_number TEXT NOT NULL,
            vehicle_registration_number TEXT NOT NULL,
            password TEXT NOT NULL
        )
        """)
        conn.commit()

if __name__== "__main__":
       init_db()
