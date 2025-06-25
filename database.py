# database.py

import sqlite3

DATABASE_URL = "bitespeed_raw.db"

def get_db_connection():
    """
    Creates a database connection.
    We configure it to return rows that can be accessed by column name (like a dict).
    We also disable the thread check for compatibility with FastAPI.
    """
    # The fix is adding check_same_thread=False
    conn = sqlite3.connect(DATABASE_URL, check_same_thread=False) ### THIS IS THE FIX ###
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database and creates the Contact table if it doesn't exist."""
    # We should also add the fix here to be consistent.
    conn = sqlite3.connect(DATABASE_URL, check_same_thread=False) ### ADD FIX HERE TOO ###
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phoneNumber TEXT,
            email TEXT,
            linkedId INTEGER,
            linkPrecedence TEXT NOT NULL CHECK(linkPrecedence IN ('primary', 'secondary')),
            createdAt DATETIME NOT NULL,
            updatedAt DATETIME NOT NULL,
            deletedAt DATETIME,
            FOREIGN KEY (linkedId) REFERENCES contact(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized.")