import time
import sys
import os
import shutil

# mis archivos
from ui import Ui_Form
from screencropper import ScreencropperModule

# pyqt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QRubberBand, QWidget, QFileDialog
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor

# otras librerias
import pyautogui
from PIL import ImageQt
import pyautogui

# variables para usar entre clases

# condicionales para guardar las preguntas y respuestas
count_preguntas = 0
count_respuestas = 0
turno_pregunta = True


class ScreenCropper(ScreencropperModule):
    def __init__(self, maincapturemenu):
        super(ScreenCropper, self).__init__()
        self.maincapturemenu = maincapturemenu

    def keyPressEvent(self, event):

        # condicionales para guardar las preguntas y respuestas
        global count_preguntas
        global count_respuestas
        global turno_pregunta

        # registro de keystrokes cuando la app esta en focus
        if event.key() == Qt.Key_0:
            self.herramienta = 0
            print('herramienta 0')
        if event.key() == Qt.Key_1:
            self.herramienta = 1
            print('herramienta 1')
        if event.key() == Qt.Key_2:
            self.herramienta = 2
            print('herramienta 2')

        # Qt.Key_Return es el enter!!! esto guarda la imagen como pregunta(n).png o respuesta(n).png
        if event.key() == Qt.Key_Return and self.rubberband.isVisible():
            self.rubberband.hide()
            code_pix = self.pixmap.copy(self.selRect.x(), self.selRect.y(), self.selRect.width(), self.selRect.height())
            recuadro_fondo = ImageQt.fromqpixmap(code_pix)
            if turno_pregunta:
                count_preguntas += 1
                recuadro_fondo.save('Carpetas FlashCards\TempFlashCards\pregunta-' + str(count_preguntas) + '-.png')
                self.maincapturemenu.answer_button.setDisabled(False)
                self.maincapturemenu.question_button.setDisabled(True)
                self.maincapturemenu.question_count_label.setText(str(count_preguntas))
            else:
                count_respuestas += 1
                recuadro_fondo.save(r'Carpetas FlashCards\TempFlashCards\respuestafondo-' + str(count_respuestas) + '-.png')

                code_pix = self.yellowtrans_pixmap.copy(self.selRect.x(), self.selRect.y(), self.selRect.width(), self.selRect.height())
                recuadro_frente = ImageQt.fromqpixmap(code_pix)
                recuadro_frente.save(r'Carpetas FlashCards\TempFlashCards\respuestafrente-' + str(count_respuestas) + '-.png')


                self.maincapturemenu.answer_count_label.setText(str(count_respuestas))
                self.maincapturemenu.answer_button.setDisabled(True)
                self.maincapturemenu.question_button.setDisabled(False)
            self.CloseEvent()

        if event.key() == Qt.Key_Escape:
            self.CloseEvent()

    def CloseEvent(self):
        print('event close')
        self.close()
        self.maincapturemenu.showNormal()

    def enter_button_was_clicked(self):
        pyautogui.press('enter')

class CaptureWindow(QtWidgets.QMainWindow, Ui_Form):

    def __init__(self):
        super(CaptureWindow, self).__init__()
        self.setupUi(self)
        self.question_button.clicked.connect(self.question_button_was_clicked)
        self.answer_button.clicked.connect(self.answer_button_was_clicked)
        self.undo_button.clicked.connect(self.undo_button_was_clicked)
        self.toanky_button.clicked.connect(self.upload)
        self.answer_count_label.setText('0')
        self.question_count_label.setText('0')
        self.answer_button.setDisabled(True)

        self.question_button.setShortcut('q')
        self.answer_button.setShortcut('a')


        self.pregunta_screencrop = None

        # visuales
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.move(1730, 700)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.CloseEvent()

    def question_button_was_clicked(self):
        global turno_pregunta
        turno_pregunta = True
        self.showMinimized()
        self.pregunta_screencrop = ScreenCropper(self)
        self.pregunta_screencrop.rubberband.setPalette(self.pregunta_screencrop.red_rubberband)
        self.pregunta_screencrop.showFullScreen()

    def answer_button_was_clicked(self):
        global turno_pregunta
        turno_pregunta = False
        self.showMinimized()
        self.pregunta_screencrop = ScreenCropper(self)
        self.pregunta_screencrop.rubberband.setPalette(self.pregunta_screencrop.blue_rubberband)
        self.pregunta_screencrop.showFullScreen()

    def undo_button_was_clicked(self):
        print('undo button')
        global count_preguntas, count_respuestas
        if count_preguntas == count_respuestas: # como siempre empieza por una pregunta cuando vayan por ej 2 2 borrar respuesta y por ej 2 1 borrar pregunta
            print('borrar respuesta')
            file_path_respuestafondo = r'Carpetas FlashCards\TempFlashCards\respuestafondo-' + str(count_respuestas) + '-.png'
            file_path_respuestafrente = r'Carpetas FlashCards\TempFlashCards\respuestafrente-' + str(count_respuestas) + '-.png'

            if os.path.exists(file_path_respuestafondo):
                os.remove(file_path_respuestafondo)
                if os.path.exists(file_path_respuestafrente):
                    os.remove(file_path_respuestafrente)
                print('volver a estado anterior')
                count_respuestas -= 1
                self.answer_button.setDisabled(False)
                self.question_button.setDisabled(True)
                self.answer_count_label.setText(str(count_respuestas))

            else:
                print("Can not delete the file as it doesn't exists")

        else:
            print('borrar pregunta')
            file_path_respuestafondo = 'Carpetas FlashCards\TempFlashCards\pregunta-' + str(count_preguntas) + '-.png'
            if os.path.exists(file_path_respuestafondo):
                os.remove(file_path_respuestafondo)
                print('volver a estado anterior')
                count_preguntas -= 1
                self.answer_button.setDisabled(True)
                self.question_button.setDisabled(False)
                self.question_count_label.setText(str(count_preguntas))

            else:
                print("Can not delete the file as it doesn't exists")


    def upload(self):
        print('upload')
        selectedfolder = QFileDialog.getExistingDirectory(self, 'select folder to save flashcards'.upper(), 'Carpetas FlashCards\StoredFlashCards')
        if selectedfolder:
            print(str(selectedfolder))
            # now move all files from 'Carpetas FlashCards\TempFlashCards\' to str(SelectedFolder)
            src = 'Carpetas FlashCards/TempFlashCards/'

            files = os.listdir(src)
            print(files)
            print(type(files))
            for f in files:
                shutil.move(src + f, str(selectedfolder))

    def CloseEvent(self):
        print('event close')
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = CaptureWindow()
    mainWindow.show()
    sys.exit(app.exec())
