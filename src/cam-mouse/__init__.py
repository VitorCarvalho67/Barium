import cv2
import mediapipe as mp
import logging
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
import pyautogui

logging.basicConfig(level=logging.DEBUG)

class CamMouse(QtCore.QThread):
    image_signal = QtCore.pyqtSignal(QtGui.QImage)
    summary = QtCore.pyqtSignal(str)

    def __init__(self, mp_config=None, parent=None):
        super(CamMouse, self).__init__(parent)
        self.status = False
        self.mp_config = mp_config or {}
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.screen_width, self.screen_height = pyautogui.size()
        self.hand_Landmarks = None
        self.prev_hand = None
        self.right_clicked = False
        self.left_clicked = False
        self.double_clicked = False
        self.dragging = False
        self.little_finger_down = None
        self.little_finger_up = None
        self.index_finger_down = None
        self.index_finger_up = None
        self.middle_finger_down = None
        self.middle_finger_up = None
        self.ring_finger_down = None
        self.ring_finger_up = None
        self.Thump_finger_down = None
        self.Thump_finger_up = None
        self.all_fingers_down = None
        self.all_fingers_up = None
        self.index_finger_within_Thumb_finger = None
        self.middle_finger_within_Thumb_finger = None
        self.little_finger_within_Thumb_finger = None
        self.ring_finger_within_Thumb_finger = None

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
                        self.hand_Landmarks = results.multi_hand_landmarks[0]
                    self.mp_draw.draw_landmarks(image, self.hand_Landmarks, self.mp_hands.HAND_CONNECTIONS)
                    self.update_fingers_status()
                    self.cursor_moving()
                    self.detect_scrolling()
                    self.detect_zoomming()
                    self.detect_clicking()
                    self.detect_dragging()

                height, width, _ = image.shape
                bytesPerLine = 3 * width
                qImg = QtGui.QImage(image.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888).rgbSwapped()
                self.image_signal.emit(qImg)
        self.cap.release()

    def update_fingers_status(self):
        self.little_finger_down = self.hand_Landmarks.landmark[20].y > self.hand_Landmarks.landmark[17].y
        self.little_finger_up = self.hand_Landmarks.landmark[20].y < self.hand_Landmarks.landmark[17].y
        self.index_finger_down = self.hand_Landmarks.landmark[8].y > self.hand_Landmarks.landmark[5].y
        self.index_finger_up = self.hand_Landmarks.landmark[8].y < self.hand_Landmarks.landmark[5].y
        self.middle_finger_down = self.hand_Landmarks.landmark[12].y > self.hand_Landmarks.landmark[9].y
        self.middle_finger_up = self.hand_Landmarks.landmark[12].y < self.hand_Landmarks.landmark[9].y
        self.ring_finger_down = self.hand_Landmarks.landmark[16].y > self.hand_Landmarks.landmark[13].y
        self.ring_finger_up = self.hand_Landmarks.landmark[16].y < self.hand_Landmarks.landmark[13].y
        self.Thump_finger_down = self.hand_Landmarks.landmark[4].y > self.hand_Landmarks.landmark[13].y
        self.Thump_finger_up = self.hand_Landmarks.landmark[4].y < self.hand_Landmarks.landmark[13].y
        self.all_fingers_down = self.index_finger_down and self.middle_finger_down and self.ring_finger_down and self.little_finger_down
        self.all_fingers_up = self.index_finger_up and self.middle_finger_up and self.ring_finger_up and self.little_finger_up
        self.index_finger_within_Thumb_finger = self.hand_Landmarks.landmark[8].y > self.hand_Landmarks.landmark[4].y and self.hand_Landmarks.landmark[8].y < self.hand_Landmarks.landmark[2].y
        self.middle_finger_within_Thumb_finger = self.hand_Landmarks.landmark[12].y > self.hand_Landmarks.landmark[4].y and self.hand_Landmarks.landmark[12].y < self.hand_Landmarks.landmark[2].y
        self.little_finger_within_Thumb_finger = self.hand_Landmarks.landmark[20].y > self.hand_Landmarks.landmark[4].y and self.hand_Landmarks.landmark[20].y < self.hand_Landmarks.landmark[2].y
        self.ring_finger_within_Thumb_finger = self.hand_Landmarks.landmark[16].y > self.hand_Landmarks.landmark[4].y and self.hand_Landmarks.landmark[16].y < self.hand_Landmarks.landmark[2].y

    def get_position(self, hand_x_position, hand_y_position):
        old_x, old_y = pyautogui.position()
        current_x = int(hand_x_position * self.screen_width)
        current_y = int(hand_y_position * self.screen_height)

        ratio = 1
        self.prev_hand = (current_x, current_y) if self.prev_hand is None else self.prev_hand
        delta_x = current_x - self.prev_hand[0]
        delta_y = current_y - self.prev_hand[1]
        
        self.prev_hand = [current_x, current_y]
        current_x , current_y = old_x + delta_x * ratio , old_y + delta_y * ratio

        threshold = 5
        if current_x < threshold:
            current_x = threshold
        elif current_x > self.screen_width - threshold:
            current_x = self.screen_width - threshold
        if current_y < threshold:
            current_y = threshold
        elif current_y > self.screen_height - threshold:
            current_y = self.screen_height - threshold

        return (current_x,current_y)
    
    def cursor_moving(self):
        point = 9
        current_x, current_y = self.hand_Landmarks.landmark[point].x ,self.hand_Landmarks.landmark[point].y
        x, y = self.get_position(current_x, current_y)
        cursor_freezed = self.all_fingers_up and self.Thump_finger_down
        if not cursor_freezed:
            pyautogui.moveTo(x, y, duration = 0)

    def detect_scrolling(self):
        scrolling_up =  self.little_finger_up and self.index_finger_down and self.middle_finger_down and self.ring_finger_down
        if scrolling_up:
            pyautogui.scroll(120)
            self.summary.emit("Rolando para cima")

            # print("Scrolling UP")
            # mandar para a Gui o texto em portugues "Rolando para cima"

        scrolling_down = self.index_finger_up and self.middle_finger_down and self.ring_finger_down and self.little_finger_down
        if scrolling_down:
            pyautogui.scroll(-120)
            self.summary.emit("Rolando para baixo")

            # print("Scrolling DOWN")
            # mandar para a Gui o texto em portugues "Rolando para baixo"
    

    def detect_zoomming(self):
        zoomming = self.index_finger_up and self.middle_finger_up and self.ring_finger_down and self.little_finger_down
        window = .05
        index_touches_middle = abs(self.hand_Landmarks.landmark[8].x - self.hand_Landmarks.landmark[12].x) <= window
        zoomming_out = zoomming and index_touches_middle
        zoomming_in = zoomming and not index_touches_middle
        
        if zoomming_out:
            pyautogui.keyDown('ctrl')
            pyautogui.scroll(-50)
            pyautogui.keyUp('ctrl')

            self.summary.emit("Diminuindo Zoom")

            # print("Zooming Out")
            # mandar para a Gui o texto em portugues "Diminuindo Zoom" no label da Gui no ARQUIVO __init__.py
            


        if zoomming_in:
            pyautogui.keyDown('ctrl')
            pyautogui.scroll(50)
            pyautogui.keyUp('ctrl')
            self.summary.emit("Aumentando Zoom")

            # print("Zooming In")
            # mandar para a Gui o texto em portugues "Aumentando Zoom"


    def detect_clicking(self):
        left_click_condition = self.index_finger_within_Thumb_finger and self.middle_finger_up and self.ring_finger_up and self.little_finger_up and not self.middle_finger_within_Thumb_finger and not self.ring_finger_within_Thumb_finger and not self.little_finger_within_Thumb_finger
        if not self.left_clicked and left_click_condition:
            pyautogui.click()
            self.left_clicked = True
            self.summary.emit("Clicando com o botão esquerdo")


            # print("Left Clicking")
            # mandar para a Gui o texto em portugues "Clicando com o botao esquerdo"
        elif not self.index_finger_within_Thumb_finger:
            self.left_clicked = False

        right_click_condition = self.middle_finger_within_Thumb_finger and self.index_finger_up and self.ring_finger_up and self.little_finger_up and not self.index_finger_within_Thumb_finger and not self.ring_finger_within_Thumb_finger and not self.little_finger_within_Thumb_finger
        if not self.right_clicked and right_click_condition:
            pyautogui.rightClick()
            self.right_clicked = True
            self.summary.emit("Clicando com o botão direito")


            # print("Right Clicking")
            # mandar para a Gui o texto em portugues "Clicando com o botao direito"
        elif not self.middle_finger_within_Thumb_finger:
            self.right_clicked = False

        double_click_condition = self.ring_finger_within_Thumb_finger and self.index_finger_up and self.middle_finger_up and self.little_finger_up and not self.index_finger_within_Thumb_finger and not self.middle_finger_within_Thumb_finger and not self.little_finger_within_Thumb_finger
        if not self.double_clicked and  double_click_condition:
            pyautogui.doubleClick()
            self.double_clicked = True
            self.summary.emit("Clicando duas vezes")

            # print("Double Clicking")
            # mandar para a Gui o texto em portugues "Clicando duas vezes"
        elif not self.ring_finger_within_Thumb_finger:
            self.double_clicked = False
    
    def detect_dragging(self):
        if not self.dragging and self.all_fingers_down:
            pyautogui.mouseDown(button = "left")
            self.dragging = True
            self.summary.emit("Arrastando")
            
            # print("Dragging")
            # mandar para a Gui o texto em portugues "Arrastando"
        elif not self.all_fingers_down:
            pyautogui.mouseUp(button = "left")
            self.dragging = False

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

    def setImage(self, frame):
        max_width = 380
        self.label.setGeometry(20, 70, max_width, int(frame.height() / (frame.width()/max_width)))
        self.label.setPixmap(QPixmap.fromImage(frame))

    def setSummary(self, string):
        self.Texto.setText(string)

if __name__ == '__main__':
    app = QApplication([])
    window = UI()
    app.exec_()

