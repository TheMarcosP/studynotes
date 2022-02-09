import time
import sys
import os

# mis archivos
from FlashCardsWindow_ui import Ui_Form

# pyqt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QRubberBand, QWidget
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


class FlashCardWindow(QtWidgets.QWidget, Ui_Form ):
    def __init__(self):
        super(FlashCardWindow, self).__init__()

