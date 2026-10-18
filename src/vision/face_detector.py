from pathlib import Path
import cv2

from src.database.find_user import find_user
from src.database.update_db import add_user

BASE_DIR = Path(__file__).resolve().parent

faceDetector = cv2.FaceDetectorYN.create(
    str(BASE_DIR / "../models/face_detection_yunet_2023mar.onnx"),
    "",
    (320, 320),
    0.9,
    0.3,
    5000
)
faceRecognizer = cv2.FaceRecognizerSF.create(
    str(BASE_DIR / "../models/face_recognition_sface_2021dec.onnx"),
    ""
)

camera = cv2.VideoCapture(0)

while True:
    good, img = camera.read()
    rgbImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    h, w, c = img.shape
    faceDetector.setInputSize((w, h))
    _, faces = faceDetector.detect(img)
    if faces is not None:
        for face in faces:
            x, y, width, height = face[:4].astype(int)
            cv2.rectangle(
                img,
                (x, y),
                (x + width, y + height),
                (0, 255, 0),
                2
            )

            alignedFace = faceRecognizer.alignCrop(img, faces[0])
            embedding = faceRecognizer.feature(alignedFace)  # Вектор признаков лица
            user = find_user(embedding, faceRecognizer)
            if user is not None:
                user_id, firstname, lastname = user
                print("Name:", firstname)
                print("LName:", lastname)
            else:
                print("Not found")

    cv2.imshow('IMG', img)

    if cv2.waitKey(1) & 0xFF == ord("s"):
        if faces is None or len(faces) != 1:
            print("Для сохранения должно быть только одно лицо в кадре!")
            break

        alignedFace = faceRecognizer.alignCrop(img, faces[0])
        embedding = faceRecognizer.feature(alignedFace)  # Вектор признаков лица
        try:
            add_user('TESTName', 'TESTLastName', embedding)
            print('User saved')
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise


    elif cv2.waitKey(1) & 0xFF == ord("q"):
        break