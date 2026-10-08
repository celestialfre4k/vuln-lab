import sqlite3

conn = sqlite3.connect("database/users.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

cursor.execute("""
INSERT INTO users (username, password)
VALUES
('admin', 'admin123'),
('test', 'password')
""")

conn.commit()

conn.close()

print("Database created successfully")