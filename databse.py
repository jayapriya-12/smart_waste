import sqlite3

conn = sqlite3.connect("waste.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT,
    email TEXT,
    username TEXT,
    password TEXT
)
""")

conn.commit()
conn.close()

print("Database Created Successfully!")