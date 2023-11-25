import cv2
import mediapipe as mp
import logging
from controller import GestureManager
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton
from PyQt5.QtGui import QIcon, QPixmap

logging.basicConfig(level=logging.DEBUG)

class CamMouse(QtCore.QThread):
    image_signal = QtCore.pyqtSignal(QtGui.QImage)
    summary = QtCore.pyqtSignal(str)

    def __init__(self, mp_config=None, parent=None):
        super(CamMouse, self).__init__(parent)
        self.status = False
        self.mp_config = mp_config or {}
        self.body = GestureManager()
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

    def run(self):
        self.cap = cv2.VideoCapture(0)
        self.status = True
        with self.mp_hands.Hands(**self.mp_config) as hands:
            while self.status:
                ret, image = self.cap.read()
                if not ret:
                    continue
                image = cv2.flip(image, 1)
                rgbFrame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = hands.process(rgbFrame)
                if results.multi_hand_landmarks:
                    if len(results.multi_hand_landmarks) == 1:
                        self.body.hand_Landmarks = results.multi_hand_landmarks[0]
                    self.mp_draw.draw_landmarks(image, self.body.hand_Landmarks, self.mp_hands.HAND_CONNECTIONS)
                    self.body.update_fingers_status()
                    self.body.cursor_moving()
                    self.body.detect_scrolling()
                    self.body.detect_zoomming()
                    self.body.detect_clicking()
                    self.body.detect_dragging()

                height, width, _ = image.shape
                bytesPerLine = 3 * width
                qImg = QtGui.QImage(image.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888).rgbSwapped()
                self.image_signal.emit(qImg)
        self.cap.release()

    def stop(self):
        self.status = False


class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.app = QApplication([])
        self.window = QMainWindow()
        self.central_widget = QLabel(self.window)
        self.button = QPushButton("", self.window)
        self.label = QLabel(self.window)

        self.btn1 = QPushButton("Mouse", self.window)
        self.btn2 = QPushButton("Teclado", self.window)
        self.btn3 = QPushButton("Configurações", self.window)
        self.btn4 = QPushButton("Movimentos", self.window)
        self.btn5 = QPushButton("Jogos", self.window)
        self.Texto = QLabel("Movimento:", self.window)
        self.label2 = QLabel("", self.window)

        self.__windowBuild()

    def __windowBuild(self):
        self.window.setWindowTitle("Barium")
        self.window.setGeometry(100, 100, 700, 500)
        self.window.setFixedSize(700, 500)
        self.window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.window.setWindowIcon(QIcon("../../img/LOGO.ico"))
        self.window.setStyleSheet("background-color: #1e1e2e;")

        self.central_widget.setPixmap(QPixmap("../../img/LogoApp.png").scaled(200, 40))
        self.central_widget.setGeometry(0, 0, 250, 80)
        self.central_widget.setAlignment(QtCore.Qt.AlignCenter)

        self.button.setStyleSheet("background-color: #077208; border-radius: 15px;")
        self.button.setGeometry(650, 20, 30, 30)

        self.Texto.setGeometry(20, 400, 200, 25)
        self.btn1.setGeometry(240, 400, 70, 25)
        self.btn2.setGeometry(320, 400, 70, 25)
        self.btn3.setGeometry(400, 400, 100, 25)
        self.btn4.setGeometry(510, 400, 100, 25)
        self.btn5.setGeometry(620, 400, 70, 25)
        self.label.setGeometry(0, 0, 0, 0)
        self.label2.setGeometry(0, 0, 0, 0)

        self.Texto.setStyleSheet("color: #CDD6F4; font-size: 14px;")
        self.btn1.setStyleSheet("background-color: #EE4740; border-radius: 10px; color: #CDD6F4; font-size: 14px;")
        self.btn1.setGeometry(240, 400, 70, 25)

        self.btn2.setStyleSheet("background-color: #EE4740; border-radius: 10px; color: #CDD6F4; font-size: 14px;")
        self.btn3.setStyleSheet("background-color: #EE4740; border-radius: 10px; color: #CDD6F4; font-size: 14px;")
        self.btn4.setStyleSheet("background-color: #EE4740; border-radius: 10px; color: #CDD6F4; font-size: 14px;")
        self.btn5.setStyleSheet("background-color: #EE4740; border-radius: 10px; color: #CDD6F4; font-size: 14px;")
        self.label.setStyleSheet("border-radius: 10px; color: #CDD6F4; font-size: 14px; background-color: #1e1e5e;")
        self.label.setStyleSheet("border-radius: 10px; color: #CDD6F4; font-size: 14px; background-color: #1e1e5e;")

        self.label.setGeometry(20, 70, 350, 300)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setScaledContents(True)
        
        self.label2.setGeometry(430, 100, 240, 240)
        self.label2.setAlignment(QtCore.Qt.AlignCenter)
        self.label2.setScaledContents(True)

        self.window.show()    
            
        self.cam_mouse = CamMouse()
        self.cam_mouse.image_signal.connect(self.setImage)
        self.cam_mouse.summary.connect(self.setSummary)
        self.cam_mouse.start()

    def start_cam_mouse(self):
        if not self.cam_mouse.isRunning():
            self.cam_mouse.start()

    def stop_cam_mouse(self):
        self.cam_mouse.stop()

    def setImage(self, image):
        self.label.setPixmap(QtGui.QPixmap.fromImage(image))

    def setSummary(self, string):
        self.Texto.setText(string)



if __name__ == '__main__':
    app = QApplication([])
    window = UI()
    window.show()
    app.exec_()
