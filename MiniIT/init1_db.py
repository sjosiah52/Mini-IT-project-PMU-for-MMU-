import sqlite3

# Database file
DATABASE = 'drivers.db'

# SQL statements to initialize the database
INITIALIZE_SQL = '''
CREATE TABLE IF NOT EXISTS drivers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mmu_id TEXT UNIQUE NOT NULL,
    ic_number TEXT NOT NULL,
    vehicle_registration_number TEXT NOT NULL,
    password TEXT NOT NULL
);
'''

# Function to initialize the database
def initialize_database():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.executescript(INITIALIZE_SQL)
        conn.commit()

if __name__ == '__main__':
    initialize_database()
    print(f'Database {DATABASE} initialized successfully.')
