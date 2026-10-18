import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from src.vision.face_detector import FaceDetectorWorker

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Опознование человека")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Виджет камеры
        self.camera_label = QLabel()
        self.camera_label.setMinimumSize(640, 480)
        self.camera_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.camera_label.setStyleSheet("background-color: black;")

        # Имя распознанного пользователя
        self.user_label = QLabel("Ожидание камеры...")
        self.user_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Сообщения о регистрации
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Кнопка регистрации
        self.register_button = QPushButton("Добавить пользователя")
        self.register_button.clicked.connect(self.register_user)

        layout.addWidget(self.camera_label)
        layout.addWidget(self.user_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.register_button)

        self.worker = FaceDetectorWorker()

        # Подключаем сигналы
        self.worker.frame_ready.connect(self.update_frame)
        self.worker.name_ready.connect(self.update_name)
        self.worker.message.connect(self.status_label.setText)
        self.worker.error.connect(self.show_error)

        self.worker.start()

    def update_frame(self, image):
        pixmap = QPixmap.fromImage(image)
        pixmap = pixmap.scaled(
            self.camera_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.camera_label.setPixmap(pixmap)

    def update_name(self, name):
        self.user_label.setText(name)

    def register_user(self):
        firstname, ok = QInputDialog.getText(
            self,
            "Регистрация",
            "Введите имя:"
        )

        if not ok or not firstname.strip():
            return

        lastname, ok = QInputDialog.getText(
            self,
            "Регистрация",
            "Введите фамилию:"
        )

        if not ok or not lastname.strip():
            return

        self.worker.register_user(
            firstname.strip(),
            lastname.strip()
        )

    def show_error(self, error):
        QMessageBox.critical(self, "Ошибка", error)

    def closeEvent(self, event):
        self.worker.stop()
        self.worker.wait()

        event.accept()

