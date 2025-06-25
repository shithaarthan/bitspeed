# To add some data to the dp for testing

import sqlite3
import os
from datetime import datetime, timezone

DATABASE_FILE = "bitespeed_raw.db"

def seed():
    # --- 1. Clean up old database ---
    if os.path.exists(DATABASE_FILE):
        os.remove(DATABASE_FILE)
        print(f"Removed old database file: {DATABASE_FILE}")

    # --- 2. Connect and create table ---
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # We can reuse the init_db logic, but for a standalone script, it's fine to have it here.
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
    print("Database table 'contact' is ready.")

    # --- 3. Insert the initial data for testing the merge scenario ---
    
    # First primary contact (created earlier in time)
    contact1 = (
        "919191",
        "george@hillvalley.edu",
        "primary",
        None, # linkedId
        # Let's make this one older
        datetime(2023, 4, 11, 12, 0, 0, tzinfo=timezone.utc),
        datetime(2023, 4, 11, 12, 0, 0, tzinfo=timezone.utc)
    )

    # Second primary contact (created later in time)
    contact2 = (
        "717171",
        "biffsucks@hillvalley.edu",
        "primary",
        None, # linkedId
        # This one is newer
        datetime(2023, 4, 21, 10, 30, 0, tzinfo=timezone.utc),
        datetime(2023, 4, 21, 10, 30, 0, tzinfo=timezone.utc)
    )

    insert_query = """
        INSERT INTO contact (phoneNumber, email, linkPrecedence, linkedId, createdAt, updatedAt)
        VALUES (?, ?, ?, ?, ?, ?)
    """

    cursor.execute(insert_query, contact1)
    print(f"Inserted primary contact 1: {contact1[1]}, {contact1[0]}")
    cursor.execute(insert_query, contact2)
    print(f"Inserted primary contact 2: {contact2[1]}, {contact2[0]}")

    # --- 4. Commit and close ---
    conn.commit()
    conn.close()
    print("\nDatabase has been seeded successfully!")
    print("Ready to run the web server and test.")

if __name__ == "__main__":
    seed()
