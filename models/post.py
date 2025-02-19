import sqlite3

conn = sqlite3.connect('post.db')
cursor = conn.cursor()


conn.execute("""
        CREATE TABLE IF NOT EXISTS post(
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             title TEXT NOT NULL UNIQUE,
             description TEXT NOT NULL UNIQUE,
             price INTEGER
        )
""")

conn.commit()
conn.close()
