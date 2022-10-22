import os
import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication

from lib.untitled import Ui_MainWindow
from lib.manager import VadManager, get_text

model_path = os.path.join("gui/data/output_graph.tflite")


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.resize(800, 605)

        self.vad = VadManager(model_path=model_path)
        self.vad.start()

        self.timer = QTimer(self)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update_text)
        self.timer.start(200)

    def update_text(self):
        self.textEdit.setText(get_text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
