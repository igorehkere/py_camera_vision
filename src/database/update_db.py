import sqlite3
from pathlib import Path

import numpy as np


def add_user(firstname, lastname, vector) -> None:
    vector_bytes = np.asarray(vector, dtype=np.float32).tobytes()

    with sqlite3.connect("../database/users.db") as db:
        c = db.cursor()

        c.execute("""
            INSERT INTO user (first_name, last_name, vector_face) VALUES (?, ?, ?)
        """, (firstname, lastname, vector_bytes)
        )

        print("DONE!")
