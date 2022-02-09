from PyQt5 import QtCore, QtGui, QtWidgets
import sys

import screencropper_ui

import time
import sys
import os


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtWidgets import QRubberBand, QWidget
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor

# otras librerias
import pyautogui
from PIL import ImageQt


class ScreencropperModule(QtWidgets.QWidget, screencropper_ui.Ui_Form):

    def __init__(self):
        super(ScreencropperModule, self).__init__()
        self.setupUi(self)

        self.screenshot = pyautogui.screenshot()
        self.screenshot.save("temporal_screenshot.png")
        time.sleep(0.5)
        self.pixmap = QtGui.QPixmap("temporal_screenshot.png")
        self.fondo.setPixmap(self.pixmap)

        self.yellowpixmap = QtGui.QPixmap(1920, 1080)
        self.yellowpixmap.fill(QtCore.Qt.yellow)

        self.m_label = QtWidgets.QLabel()
        self.m_label.setPixmap(self.yellowpixmap)

        self.yellowtrans_pixmap = QtGui.QPixmap(self.yellowpixmap.size())
        self.yellowtrans_pixmap.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(self.yellowtrans_pixmap)
        #CAMBIAR SIGUIENTE LINEA A 0.5 0.4 PARA VER EL FRENTE CON OPACIDAD
        painter.setOpacity(0.4)
        painter.drawPixmap(QtCore.QPoint(), self.yellowpixmap)
        painter.end()
        self.m_label.setPixmap(self.yellowtrans_pixmap)
        self.frente.setPixmap(self.yellowtrans_pixmap)



        self.drawing = False
        self.origin, self.lastPoint = QPoint(), QPoint()
        self.screenshot = pyautogui.screenshot()


        # iniciar rubberband
        self.rubberband = QRubberBand(QRubberBand.Rectangle, self)
        self.blue_rubberband = QtGui.QPalette()
        self.blue_rubberband.setBrush(QtGui.QPalette.Highlight, QtGui.QBrush(QtCore.Qt.darkBlue))
        self.red_rubberband = QtGui.QPalette()
        self.red_rubberband.setBrush(QtGui.QPalette.Highlight, QtGui.QBrush(QtCore.Qt.darkRed))
        self.rubberband.setPalette(self.blue_rubberband)
        self.rubberband.setWindowOpacity(1.0)

        # condicion para painter = 1 borra, 2 rubberband, 0 answers pencil
        self.herramienta = 2


    # inicio window del lateral

        self.min_button.clicked.connect(self.min_button_was_clicked)
        self.config_button.clicked.connect(self.config_button_was_clicked)
        self.exit_button.clicked.connect(self.exit_button_was_clicked)
        self.answer_pencil_button.clicked.connect(self.answer_pencil_button_was_clicked)
        self.borrador_button.clicked.connect(self.borrador_button_was_clicked)
        self.rect_button.clicked.connect(self.rect_button_was_clicked)
        self.enter_button.clicked.connect(self.enter_button_was_clicked)

    def min_button_was_clicked(self):
        self.showMinimized()

    def config_button_was_clicked(self):
        pass

    def exit_button_was_clicked(self):
        self.CloseEvent()

    def answer_pencil_button_was_clicked(self):
        self.herramienta = 0

    def borrador_button_was_clicked(self):
        self.herramienta = 1

    def rect_button_was_clicked(self):
        self.herramienta = 2

    def enter_button_was_clicked(self):
        pass
    # fin window del lateral

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


        # Qt.Key_Return es el enter!!!
        # agregarr

        if event.key() == Qt.Key_Escape:
            self.CloseEvent()

    def paintEvent(self, event):
        painter1 = QPainter(self)
        painter1.drawPixmap(QPoint(), self.yellowtrans_pixmap)

    def mousePressEvent(self, event):
        # draw rectangles
        if event.button() == Qt.LeftButton and self.herramienta == 0:
            print("p1")
            self.drawing = True
            self.lastPoint = event.pos()

        # pintar con borrador
        if event.button() == Qt.LeftButton and self.herramienta == 1:
            print('her1 mousePressEvent')
            self.drawing = True
            self.lastPoint = event.pos()
        # crop
        if event.button() == Qt.LeftButton and self.herramienta == 2:
            print('adentro de mouse press')
            self.origin = event.pos()
            self.rubberband.setGeometry(QtCore.QRect(self.origin, QtCore.QSize()))
            self.rubberband.show()
            QWidget.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        # draw rectangles
        if event.buttons() and Qt.LeftButton and self.herramienta == 0:
            painter1 = QPainter(self.yellowtrans_pixmap)
            pen = QPen(QColor(72, 61, 20), 25, Qt.DashDotLine, Qt.RoundCap, Qt.RoundJoin)
            painter1.setPen(pen)
            painter1.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.frente.setPixmap(self.yellowtrans_pixmap)

        if event.buttons() and Qt.LeftButton and self.drawing and self.herramienta == 1:
            painter1 = QPainter(self.pixmap)
            pen = QPen(QColor(32, 31, 30), 25, Qt.DashDotLine, Qt.RoundCap, Qt.RoundJoin)
            painter1.setPen(pen)
            painter1.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.fondo.setPixmap(self.pixmap)

        if self.herramienta == 2:
            # print('adentro de mouse move')
            if self.rubberband.isVisible():
                self.rubberband.setGeometry(QtCore.QRect(self.origin, event.pos()).normalized())
            QWidget.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        # draw rectangles
        if event.button() == Qt.LeftButton and self.herramienta == 0:
            self.drawing = False

        if event.button == Qt.LeftButton and self.herramienta == 1:
            self.drawing = False

        if event.button() == Qt.LeftButton and self.herramienta == 2:
            if self.rubberband.isVisible():
                self.selRect = self.rubberband.geometry()

            QWidget.mouseReleaseEvent(self, event)
            time.sleep(1.0)

    def CloseEvent(self):
        print('event close')
        self.close()








if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    draw = ScreencropperModule()
    draw.showFullScreen()
    sys.exit(app.exec_())