import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import threading
import cv2
import mediapipe as mp
import numpy as np
import time
from test1 import *


class ImageViewer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ImageViewer, self).__init__(parent)
        self.image = QtGui.QImage()
        self.setAttribute(Qt.WA_OpaquePaintEvent)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()

    def initUI(self):
        self.setWindowTitle('Test')

    @pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        if image.isNull():
            print("Viewer Dropped frame!")

        self.image = image
        if image.size() != self.size():
            self.setFixedSize(image.size())
        self.update()


class kinwriter(QMainWindow, Ui_MainWindow,):
    global n_2, img
    def __init__(self,parent=None):
        super().__init__()
        self.parent = parent
        self.setGeometry(700, 500, 300, 100)
        self.th = ThreadClass(self)
        self.th.threadEvent.connect(self.threadEventHandler)
        self.th.start()
        self.setupUi(self)
        # self.timer = QTimer(self)
        # self.timer.setSingleShot(False)
        # self.timer.setInterval(5000) # in milliseconds, so 5000 = 5 seconds
        # # self.timer.timeout.connect(self.start_Macro)
        # self.timer.start()i0nscn2kdlr2k

        # print(self.hasMouseTracking())

        self.show()

cap = cv2.VideoCapture(0)
max_num_hands = 1
gesture = {
    0:'NO', 1:'one',2:'two',3:'three', 4:'four', 5:'five',6:'right',7:'OK'
}
img = QtGui.QImage()
n_2 = 10

class ThreadClass(QThread):
    threadEvent = pyqtSignal(int)
    threadEvent2 = pyqtSignal(QtGui.QImage)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.n = 0
        self.isRun = False

    def run(self):
        mp_hands = mp.solutions.hands
        mp_drawing = mp.solutions.drawing_utils
        hands = mp_hands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)

        # Gesture recognition model
        file = np.genfromtxt('gesture_train.csv', delimiter=',')
        angle = file[:, :-1].astype(np.float32)
        label = file[:, -1].astype(np.float32)
        knn = cv2.ml.KNearest_create()
        knn.train(angle, cv2.ml.ROW_SAMPLE, label)

        pre_gesture = 8
        count = 0  # 동일 숫자 등장 횟수
        flag = 0  # 가장 처음 실행이냐 아니냐
        close_flag = 0  # 카메라 객체 해제를 위한 flag
        while cap.isOpened():
            ret, img = cap.read()
            if not ret:
                continue

            img = cv2.flip(img, 1)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            result = hands.process(img)

            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            if result.multi_hand_landmarks is not None:
                for res in result.multi_hand_landmarks:
                    joint = np.zeros((21, 3))
                    for j, lm in enumerate(res.landmark):
                        joint[j] = [lm.x, lm.y, lm.z]

                    # Compute angles between joints
                    v1 = joint[[0, 1, 2, 3, 0, 5, 6, 7, 0, 9, 10, 11, 0, 13, 14, 15, 0, 17, 18, 19], :]  # Parent joint
                    v2 = joint[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                         :]  # Child joint
                    v = v2 - v1  # [20,3]
                    # Normalize v
                    v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

                    # Get angle using arcos of dot product
                    angle = np.arccos(np.einsum('nt,nt->n',
                                                v[[0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16, 17, 18], :],
                                                v[[1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19], :]))  # [15,]

                    angle = np.degrees(angle)  # Convert radian to degree

                    # Inference gesture
                    data = np.array([angle], dtype=np.float32)
                    ret, results, neighbours, dist = knn.findNearest(data, 3)
                    idx = int(results[0][0])
                    print(idx)

                    # Draw gesture result
                    if idx in gesture.keys():
                        cv2.putText(img, text=gesture[idx].upper(), org=(
                        int(res.landmark[0].x * img.shape[1]), int(res.landmark[0].y * img.shape[0] + 20)),
                                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 255, 255), thickness=2)

                    mp_drawing.draw_landmarks(img, res, mp_hands.HAND_CONNECTIONS)
                    color_swapped_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    color_swapped_image = cv2.resize(color_swapped_image, dsize=(480, 200))
                    height, width = color_swapped_image.shape[:2]
                    #print("height: {} , width: {}".format(height, width))
                    #print("height = {0}, width = {1}".format(height, width)) --> debugging area
                    qt_img = QtGui.QImage(color_swapped_image.data,
                                          width,
                                          height,
                                          color_swapped_image.strides[0],
                                          QtGui.QImage.Format_RGB888)
                    self.threadEvent2.emit(qt_img)
                    if pre_gesture == 8:
                        pre_gesture = idx
                    elif pre_gesture == idx:
                        count = count + 1
                    else:
                        pre_gesture = idx
                        count = 0
            #cv2.imshow('Game', img)
            time.sleep(0.03)  # 0.5초 delay
            if count == 30:
                self.n = idx
                self.threadEvent.emit(self.n)
                count = 0



if __name__ == '__main__':
    app = QApplication([])
    sn = kinwriter()
    sn.th.threadEvent2.connect(sn.image_viewer1.setImage)
    app.processEvents()
    sys.exit(app.exec_())