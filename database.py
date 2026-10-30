import sqlite3

connection = sqlite3.connect("students.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    python_marks INTEGER,
    sql_marks INTEGER,
    dsa_marks INTEGER,
    total INTEGER,
    percentage REAL,
    grade TEXT
)
""")

connection.commit()

connection.close()

print("Database created successfully!")