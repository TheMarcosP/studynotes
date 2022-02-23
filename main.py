from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QRect
from PIL import ImageQt
import sys

import capture
import FlashCardsWindow
from screencropper import ScreencropperModule
from capture import CaptureWindow


# condicionales para guardar las preguntas y respuestas
# count_preguntas = 0
# count_respuestas = 0
# turno_pregunta = True


class MainWindow(FlashCardsWindow.FlashCardWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.capturebotton.clicked.connect(self.pushButton_2_was_clicked)
        self.CaptureWindowObj = CaptureWindowMain(self)
    def pushButton_2_was_clicked(self):
        MainWindow.hide()
        self.CaptureWindowObj.show()

class CaptureWindowMain(capture.CaptureWindow):
    def __init__(self,MainWindowObj):
        super(CaptureWindowMain, self).__init__()
        self.MainWindowObj = MainWindowObj

    def CloseEvent(self):
        self.close()
        self.MainWindowObj.showMaximized()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.showMaximized()
    sys.exit(app.exec())
