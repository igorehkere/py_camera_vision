from ui.MainWindow import MainWindow
from PyQt6.QtWidgets import QApplication
import signal
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    wnd = MainWindow()
    wnd.setFixedSize(800, 600)
    wnd.show()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.exit(app.exec())
