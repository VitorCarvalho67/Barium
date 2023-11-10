import sys
import os
projeto_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(projeto_dir)

from modules import mouse
import cv2
import mediapipe as mp
import math
import numpy as np
from PIL import Image, ImageDraw
import time
import datetime
import pytz
import pandas as pd
from keras.models import load_model
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import QTimer, QThread, Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QApplication, QMainWindow, QLabel, QPushButton
import networkx as nx
import matplotlib.pyplot as plt


class VideoCaptureThread(QThread):
    frameCaptured = pyqtSignal(QImage)  # Change the signal type to QImage

    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        

    def run(self):
        while True:
            sucesso, frame = self.cap.read()
            if not sucesso:
                continue

            frame = cv2.flip(frame, 1)

            frame = self.__aumentar_contraste(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            height, width, channel = frame.shape
            step = channel * width
            qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
            self.frameCaptured.emit(qImg)

    def __aumentar_contraste(self, frame):
        alpha = 2
        beta = 0

        imagem = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

        mp_maos = mp.solutions.hands
        maos = mp_maos.Hands(max_num_hands=1)

        coordenadas =[]
        for a in range (21):
            coordenadas.append([0, 0])

        resultados = maos.process(cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB))

        lista_pontos = []

        if resultados.multi_hand_landmarks:
            for pontos_mao in resultados.multi_hand_landmarks:
                for idx, ponto in enumerate(pontos_mao.landmark):
                    altura, largura, _ = frame.shape
                    cx, cy = int(ponto.x * largura), int(ponto.y * altura)
                    lista_pontos.append((cx, cy))

                if lista_pontos:
                    x, y, w, h = cv2.boundingRect(np.array(lista_pontos))
                    tamanho_max = max(w, h)

                    centro_x = x + w // 2
                    centro_y = y + h // 2

                    x = centro_x - tamanho_max // 2
                    y = centro_y - tamanho_max // 2

                    x, y, w, h = x - 10, y - 10, tamanho_max + 20, tamanho_max + 20

                    cv2.rectangle(imagem, (x, y), (x + w, y + h), (0, 255, 0), 2)

                mp.solutions.drawing_utils.draw_landmarks(imagem, pontos_mao, mp_maos.HAND_CONNECTIONS)

        return imagem

    # def getCoordinates(self, frame):
    #     mp_maos = mp.solution.hands
    #     maos = mp_maos.Hans(max_num_hands=1)

    #     coordenadas =[]
    #     for a in range (21):
    #         coordenadas.append([0, ])
    

        # resultados = maos.process(cv2.cvtColor(self.__aumentar_contraste)frame)), cv2.COLOR_BGR2RGB)

class UI():
    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)
        self.window = QMainWindow()
        self.central_widget = QLabel(self.window)
        self.button = QPushButton("", self.window)
        self.label = QLabel(self.window)

        self.btn1 = QPushButton("Mouse", self.window)
        self.btn2 = QPushButton("Teclado", self.window)
        self.btn3 = QPushButton("Configurações", self.window)
        self.btn4 = QPushButton("Movimentos", self.window)
        self.btn5 = QPushButton("Jogos", self.window)
        self.Texto = QLabel("Movimento:",self.window)
        self.label2 = QLabel("Mão", self.window)

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
        self.button.clicked.connect(self.__on_button_click, QtCore.Qt.UniqueConnection)

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
        self.btn1.clicked.connect(self.__on_button_click)

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

        self.video_thread = VideoCaptureThread()
        self.video_thread.frameCaptured.connect(self.SetVideo)
        self.video_thread.start()


    def __on_button_click(self):
        self.app.quit()

    def SetVideo(self, frame):
        max_width = 380
        self.label.setGeometry(20, 70, max_width, int(frame.height() / (frame.width()/max_width)))
        self.label.setPixmap(QPixmap.fromImage(frame))
        

# class ProcessMotion(Thread):
#     def __init__(self):
#         self.model = load_model('../../models/modelTest.keras')
#         self.intervalo = 100
#         self.numberFrames = 20
#         self.exibir_conexoes = False
#         self.mostrar_numeros = False
        

def main():
    ui = UI()
    sys.exit(ui.app.exec_())

if __name__ == "__main__":
    main()
