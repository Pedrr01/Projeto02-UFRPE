import sqlite3
import os


db_path = os.path.join('database', 'users.db')

connection = sqlite3.connect(db_path)
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')


cursor.execute("PRAGMA table_info(users)")
columns = [column[1] for column in cursor.fetchall()]


if 'faculdade' not in columns:
    cursor.execute("ALTER TABLE users ADD COLUMN faculdade TEXT")
    print("Coluna 'faculdade' adicionada com sucesso.")

if 'curso' not in columns:
    cursor.execute("ALTER TABLE users ADD COLUMN curso TEXT")
    print("Coluna 'curso' adicionada com sucesso.")

if 'periodo' not in columns:
    cursor.execute("ALTER TABLE users ADD COLUMN periodo TEXT")
    print("Coluna 'periodo' adicionada com sucesso.")

connection.commit()
connection.close()
