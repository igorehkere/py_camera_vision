import sqlite3

db = sqlite3.connect('users.db')

c = db.cursor()
c.execute("""CREATE TABLE user (
    first_name text,
    last_name text,
    vector_face text
)""")

db.commit()

db.close()