import sqlite3

db = sqlite3.connect('users.db')

c = db.cursor()
c.execute("""CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    vector_face BLOB NOT NULL
)""")

db.commit()

db.close()