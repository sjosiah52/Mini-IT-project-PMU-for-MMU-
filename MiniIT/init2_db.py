import sqlite3

DATABASE = 'rides.db'

INITIALIZE_SQL = '''
CREATE TABLE IF NOT EXISTS ride (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pickup TEXT NOT NULL,
    destination TEXT NOT NULL,
    price REAL NOT NULL,
    user_name TEXT NOT NULL
    phone_number INTEGER NOT NULL
);  
'''

def initialize_database():
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.executescript(INITIALIZE_SQL)
            conn.commit()
        
        print("Database initialized successfully.")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

if __name__ == "__main__":
    initialize_database()
