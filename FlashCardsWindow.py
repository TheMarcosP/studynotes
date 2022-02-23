import time
import sys
import os
import random
# mis archivos
import FlashCardsWindow_ui

# pyqt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QRubberBand, QWidget, QFileDialog
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor

# otras librerias
import pyautogui
from PIL import ImageQt


class FlashCard():
    def __init__(self):
        self.pregunta = ''
        self.respuestafondo = ''
        self.respuestafrente = ''

# for file in Carpetas Flashcards:
#     for group of images create in file:
#         create flashcard object


class FlashCardWindow(QtWidgets.QWidget, FlashCardsWindow_ui.Ui_MainFrame):
    def __init__(self):
        super(FlashCardWindow, self).__init__()
        self.setupUi(self)

        self.pixmap = QtGui.QPixmap("fondo inicio.png")
        self.pregunta.setPixmap(self.pixmap)
        self.respuesta.setPixmap(QtGui.QPixmap('fondo inicio.png'))

        self.selectdeck.clicked.connect(self.selectthefolder)
        self.showanswer_nextquestion.clicked.connect(self.showanswer_nextquestion_was_clicked)
        self.managefolderbotton.clicked.connect(self.managefolderbotton_was_clicked)
        self.selectedfolder = False

        self.last_randomchoice = -1
        self.randomchoice = -1
        self.showanswer_or_nextquestion = 0

    def selectthefolder(self):
        self.selectedfolder = QFileDialog.getExistingDirectory(self, 'select folder to view flashcards'.upper(), 'Carpetas FlashCards\StoredFlashCards')
        if self.selectedfolder:
            # get list of files in selected folder
            self.files = os.listdir(str(self.selectedfolder))
            # now get a random pregunta and number
            bloque = int((len(self.files) / 3))
            # print('bloque: '+ str(bloque))
            randomchoice = random.randint(0, bloque-1)
            print('randomchoice: '+str(randomchoice))
            path_pregunta = (str(self.selectedfolder)+'/'+str(self.files[randomchoice]))
            print(path_pregunta)

            self.path_respuestafondo = (str(self.selectedfolder)+'/'+str(self.files[randomchoice+bloque]))
            print(self.path_respuestafondo)

            path_respuestafrente = (str(self.selectedfolder) + '/' + str(self.files[randomchoice + bloque*2]))
            print(path_respuestafrente)

            base_pixmap = QtGui.QPixmap(self.path_respuestafondo)
            overlay_pixmap = QtGui.QPixmap(path_respuestafrente)

            painter = QtGui.QPainter(base_pixmap)
            painter.drawPixmap(0,0, overlay_pixmap)

            painter.end()

            # then set label to pregunta and respuesta
            self.pregunta.setPixmap(QtGui.QPixmap(path_pregunta))

            self.respuesta.setPixmap(base_pixmap)

            #set to show answer next click
            self.showanswer_or_nextquestion = 1
            self.showanswer_nextquestion.setText('show answer')

    def showanswer_nextquestion_was_clicked(self):
        # get new question
        if self.selectedfolder and self.showanswer_or_nextquestion == 0:
            # get list of files in selected folder
            self.files = os.listdir(str(self.selectedfolder))
            # now get a random pregunta and number
            bloque = int((len(self.files) / 3))
            # print('bloque: ' + str(bloque))

            while self.randomchoice == self.last_randomchoice:
                self.randomchoice = random.randint(0, bloque - 1)
                print('while loop randomchoice: ' + str(self.randomchoice))
                print('while loop last random choice' + str(self.last_randomchoice))

            print('randomchoice '+ str(self.randomchoice))

            self.last_randomchoice = self.randomchoice
            print('last random choice '+ str(self.last_randomchoice))

            path_pregunta = (str(self.selectedfolder) + '/' + str(self.files[self.randomchoice]))
            # print(path_pregunta)

            self.path_respuestafondo = (str(self.selectedfolder) + '/' + str(self.files[self.randomchoice + bloque]))
            # print(path_respuestafondo)

            path_respuestafrente = (str(self.selectedfolder) + '/' + str(self.files[self.randomchoice + bloque * 2]))
            # print(path_respuestafrente)

            base_pixmap = QtGui.QPixmap(self.path_respuestafondo)

            overlay_pixmap = QtGui.QPixmap(path_respuestafrente)

            painter = QtGui.QPainter(base_pixmap)
            painter.drawPixmap(0, 0, overlay_pixmap)

            painter.end()

            # then set label to pregunta and respuesta
            self.pregunta.setPixmap(QtGui.QPixmap(path_pregunta))

            self.respuesta.setPixmap(base_pixmap)

            #set to show answer next click
            self.showanswer_or_nextquestion = 1
            self.showanswer_nextquestion.setText('show answer')
        # show answer
        elif self.selectedfolder and self.showanswer_or_nextquestion == 1:
            respuesta_fondo = QtGui.QPixmap(self.path_respuestafondo)

            self.respuesta.setPixmap(respuesta_fondo)
            # set to next question next click
            self.showanswer_nextquestion.setText('next question')
            self.showanswer_or_nextquestion = 0

    def managefolderbotton_was_clicked(self):
        os.startfile('Carpetas FlashCards\StoredFlashCards')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    FlashCardsmainWindow = FlashCardWindow()
    FlashCardsmainWindow.showMaximized()
    sys.exit(app.exec())
