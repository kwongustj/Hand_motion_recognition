from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from test2 import Ui_OtherWindow
import threading
import cv2
import mediapipe as mp
import numpy as np
import time
from test3 import Ui_thirdWindow
from PyQt5 import QtCore, QtGui, QtWidgets

class Imageviewer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Imageviewer, self).__init__(parent)
        self.image = QtGui.QImage()
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()

    def initUI(self):
        self.setWindowTitle('Test')

    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        if image.isNull():
            print("Viewer Dropped frame!")

        self.image = image
        if image.size() != self.size():
            self.setFixedSize(image.size())
        self.update()

class Ui_MainWindow(object):

     def oppenWindow(self):
         self.window= QtWidgets.QMainWindow()
         self.ui = Ui_thirdWindow()
         self.ui.setupUi(self.window)
         self.window.show()

     def openWindow(self,a,b):
         self.window= QtWidgets.QMainWindow()
         self.ui =Ui_OtherWindow(a,b)
         self.ui.setupUi(self.window)
         self.window.show()
         self.hide()

     def hideWindow(self):
        self.show()
        self.window.hide()

     def __init__(self):
        self.sum1 = 0
        self.z=0

     def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(819, 625)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        font = QtGui.QFont()
        font.setFamily("타이포_쌍문동 B")
        font.setBold(True)
        font.setWeight(75)
        self.centralwidget.setFont(font)
        self.centralwidget.setObjectName("centralwidget")
        self.result = QtWidgets.QLabel(self.centralwidget)
        self.result.setGeometry(QtCore.QRect(30, 520, 721, 121))
        self.image_viewer1 = Imageviewer(self.centralwidget)
        self.image_viewer1.setGeometry(QtCore.QRect(210, 30, 351, 161))
        font = QtGui.QFont()
        font.setFamily("타이포_쌍문동 B")
        font.setPointSize(16)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.result.setFont(font)
        self.result.setAlignment(QtCore.Qt.AlignCenter)
        self.result.setObjectName("result")
        self.result_2 = QtWidgets.QLabel(self.centralwidget)
        self.result_2.setGeometry(QtCore.QRect(90, 206, 611, 71))
        font = QtGui.QFont()
        font.setFamily("타이포_쌍문동 B")
        font.setPointSize(16)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.result_2.setFont(font)
        self.result_2.setAlignment(QtCore.Qt.AlignCenter)
        self.result_2.setObjectName("result_2")
        self.num1 = QtWidgets.QPushButton(self.centralwidget)
        self.num1.setGeometry(QtCore.QRect(70, 296, 170, 28))
        self.num1.setObjectName("num1")
        self.num2 = QtWidgets.QPushButton(self.centralwidget)
        self.num2.setGeometry(QtCore.QRect(250, 296, 110, 28))
        self.num2.setObjectName("num2")
        self.num3 = QtWidgets.QPushButton(self.centralwidget)
        self.num3.setGeometry(QtCore.QRect(370, 296, 130, 28))
        self.num3.setObjectName("num3")
        self.num4 = QtWidgets.QPushButton(self.centralwidget)
        self.num4.setGeometry(QtCore.QRect(510, 296, 93, 28))
        self.num4.setObjectName("num4")
        self.num5 = QtWidgets.QPushButton(self.centralwidget)
        self.num5.setGeometry(QtCore.QRect(610, 296, 130, 28))
        self.num5.setObjectName("num5")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(160, 357, 271, 181))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(510, 427, 131, 41))
        self.textEdit_2.setObjectName("textEdit_2")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.num2.clicked.connect(MainWindow.start2)
        self.num3.clicked.connect(MainWindow.start3)
        self.num4.clicked.connect(MainWindow.start4)
        self.num5.clicked.connect(MainWindow.start5)
        self.num1.clicked.connect(MainWindow.start1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

     def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "손동작 인식 키오스크"))
        self.result.setText(_translate("MainWindow", "주문하실 메뉴를 손가락으로 표시해주세요 !"))
        self.result_2.setText(_translate("MainWindow", "menu"))
        self.num1.setText(_translate("MainWindow", "1. 아이스 아메리카노"))
        self.num2.setText(_translate("MainWindow", "2. 카페라떼"))
        self.num3.setText(_translate("MainWindow", "3. 아이스 초코"))
        self.num4.setText(_translate("MainWindow", "4. 스무디"))
        self.num5.setText(_translate("MainWindow", "5. 에스프레소"))



     def start2(self):
        pass
     def start1(self):
        pass
     def start3(self):
        pass
     def start4(self):
        pass
     def start5(self):
        pass


     @QtCore.pyqtSlot(int)
     def threadEventHandler(self, n):
        n_2 = n
        if n_2 == 1:
            self.textEdit.append("아메리카노 2500")
            self.sum1 = self.sum1 + 2500
            self.textEdit_2.clear()
            self.textEdit_2.append(str(self.sum1))
        elif n_2 == 2:
            self.textEdit.append("카페라떼 4500")
            self.sum1 = self.sum1 + 4500
            self.textEdit_2.clear()
            self.textEdit_2.append(str(self.sum1))
        elif n_2 == 3:
            self.textEdit.append("아이스초코 4000")
            self.sum1 = self.sum1 + 4000
            self.textEdit_2.clear()
            self.textEdit_2.append(str(self.sum1))
        elif n_2 == 4:
            self.textEdit.append("스무디 3000")
            self.sum1 = self.sum1 + 3000
            self.textEdit_2.clear()
            self.textEdit_2.append(str(self.sum1))
        elif n_2 == 5:
            self.textEdit.append("에스프레소 2500")
            self.sum1 = self.sum1 + 2500
            self.textEdit_2.clear()
            self.textEdit_2.append(str(self.sum1))
        elif n_2 == 7:
            if self.z == 0:
                self.z = self.z + 1
                m = self.textEdit.toPlainText()
                n = self.textEdit_2.toPlainText()
                self.openWindow(m, n)
            elif self.z == 1:
                self.z = 2
                self.oppenWindow()

        elif n_2 == 0:
            self.hideWindow()
            self.z = 0


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
