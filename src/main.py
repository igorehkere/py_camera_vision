from ui.MainWindow import MainWindow
from PyQt6.QtWidgets import QApplication
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtGui import QIcon
import signal
import sys
import os

app_dir = os.path.dirname(os.path.abspath(__file__))
icons_dir = os.path.join(app_dir, 'icons')
icon_path = os.path.join(icons_dir, "detect_human_icon.svg")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    print("Qt platform:", app.platformName())
    app.setStyle("Fusion")
    app.setApplicationName("detect-human")
    app.setDesktopFileName("detect-human")
    app.setWindowIcon(QIcon(icon_path))
    wnd = MainWindow()
    wnd.setFixedSize(800, 600)
    wnd.show()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.exit(app.exec())
