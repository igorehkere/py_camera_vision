import cv2

from pathlib import Path
from queue import Queue, Empty
from threading import Event

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QImage

from src.database.find_user import find_user
from src.database.update_db import add_user


BASE_DIR = Path(__file__).resolve().parents[1]


class FaceDetectorWorker(QThread):

    frame_ready = pyqtSignal(QImage)
    name_ready = pyqtSignal(str)
    message = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.running = Event()
        self.running.set()

        self.registration_queue = Queue()

        self.previous_names = None

    def register_user(self, firstname, lastname):
        self.registration_queue.put((firstname, lastname))

    def stop(self):
        self.running.clear()

    def run(self):
        camera = None

        try:
            # Модель обнаружения лиц
            faceDetector = cv2.FaceDetectorYN.create(
                str(BASE_DIR / "models/face_detection_yunet_2023mar.onnx"),
                "",
                (320, 320),
                0.9,
                0.3,
                5000
            )

            # Модель распознавания лиц
            faceRecognizer = cv2.FaceRecognizerSF.create(
                str(BASE_DIR / "models/face_recognition_sface_2021dec.onnx"),
                ""
            )

            camera = cv2.VideoCapture(0)

            if not camera.isOpened():
                raise RuntimeError("Не удалось открыть камеру")

            while self.running.is_set():
                good, img = camera.read()

                if not good:
                    break

                h, w = img.shape[:2]
                faceDetector.setInputSize((w, h))
                _, faces = faceDetector.detect(img)

                # Кадр для отображения
                display_frame = img.copy()

                names = []
                embeddings = []

                if faces is not None:
                    for face in faces:

                        # Получаем вектор лица
                        alignedFace = faceRecognizer.alignCrop(img, face)
                        embedding = faceRecognizer.feature(alignedFace)
                        embeddings.append(embedding)

                        # Ищем пользователя в базе данных
                        user = find_user(embedding, faceRecognizer)

                        if user is not None:
                            user_id, firstname, lastname = user

                            name = f"{firstname} {lastname}"
                            color = (0, 255, 0)

                        else:
                            name = "Unknown"
                            color = (0, 0, 255)

                        names.append(name)

                        # Координаты лица
                        x, y, width, height = face[:4].astype(int)

                        cv2.rectangle(
                            display_frame,
                            (x, y),
                            (x + width, y + height),
                            color,
                            2
                        )

                        cv2.putText(
                            display_frame,
                            name,
                            (x, max(y - 10, 20)),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            color,
                            2
                        )

                # Проверяем запрос на регистрацию
                try:
                    firstname, lastname = self.registration_queue.get_nowait()

                    if len(embeddings) == 1:
                        add_user(firstname, lastname, embeddings[0])
                        self.message.emit(
                            f"Пользователь {firstname} {lastname} сохранён"
                        )

                    else:
                        self.message.emit("Для регистрации в кадре должно быть одно лицо")

                except Empty:
                    pass

                # Передаём информацию о пользователях
                current_names = (
                    ", ".join(names)
                    if names
                    else "Лицо не обнаружено"
                )

                if current_names != self.previous_names:
                    self.name_ready.emit(current_names)
                    self.previous_names = current_names

                # Преобразуем кадр OpenCV в QImage
                rgb = cv2.cvtColor(display_frame,cv2.COLOR_BGR2RGB)
                height, width, channels = rgb.shape
                qimage = QImage(rgb.data, width, height, rgb.strides[0], QImage.Format.Format_RGB888).copy()

                # Передаём кадр в интерфейс
                self.frame_ready.emit(qimage)

        except Exception as err:
            self.error.emit(str(err))

        finally:
            if camera is not None:
                camera.release()