import sqlite3
from typing import Union

import cv2
import numpy as np


def find_user(vector, faceRecognizer) -> Union[None, tuple[int, str, str]]:
    best_similarity = -1.0
    best_user = None
    with sqlite3.connect("../database/users.db") as db:
        users = db.execute("""
            SELECT id, first_name, last_name, vector_face
            FROM user
        """).fetchall()

    vector = np.asarray(vector, dtype=np.float32).reshape(1, -1)

    for user in users:
        user_id, firstname, lastname, vector_bytes = user

        saved_vector = np.frombuffer(vector_bytes, dtype=np.float32).reshape(1, -1)

        similarity = faceRecognizer.match(
            vector,
            saved_vector,
            cv2.FaceRecognizerSF_FR_COSINE
        )

        if similarity > best_similarity:
            best_similarity = similarity
            best_user = (user_id, firstname, lastname)

    if best_similarity >= 0.363:
        return best_user

    return None