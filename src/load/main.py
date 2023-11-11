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
    frameCaptured = pyqtSignal(QImage)
    handImage = pyqtSignal(str)
    predictMove = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        self.mp_maos = mp.solutions.hands
        self.maos = self.mp_maos.Hands(max_num_hands=1)

        self.model = self.load_model()

        self.video_record_run = False
        self.video_frame = -1
        self.tempo_atual = 0
        self.tempo_anterior = 0

        self.intervalo = 100
        self.intervalo_inicial = 500

        self.video = []

    def run(self):
        while True:
            sucesso, frame = self.cap.read()
            if not sucesso:
                continue

            frame = cv2.flip(frame, 1)

            frame = self.__getCoordinates(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            height, width, channel = frame.shape
            step = channel * width
            qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
            self.frameCaptured.emit(qImg)

    def __getCoordinates(self, frame):
        alpha = 2
        beta = 0

        imagem = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

        x, y, w, h = 0, 0, 0, 0
        
        resultados = self.maos.process(cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB))

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

                mp.solutions.drawing_utils.draw_landmarks(imagem, pontos_mao, self.mp_maos.HAND_CONNECTIONS)
        
        coordenadas = self.ProcessarCoordenadas(lista_pontos, x, y, w, h)

        handImage = self.drawHand(coordenadas)
        self.handImage.emit(handImage)

        
        self.tempo_atual = time.time() * 1000

        if self.video_record_run == True:
            if self.video_frame == 0:
                if self.tempo_atual - self.tempo_anterior > self.intervalo_inicial:
                    self.video.append(coordenadas)
                    self.video_frame = 1

                    self.tempo_anterior = time.time() * 1000

            elif self.video_frame > 0 and self.video_frame < 20:
                if self.tempo_atual - self.tempo_anterior > self.intervalo:
                    self.video.append(coordenadas)
                    self.video_frame += 1

                    self.tempo_anterior = time.time() * 1000

            elif self.video_frame > 0 and self.video_frame == 20:
                if self.tempo_atual - self.tempo_anterior > self.intervalo:
                    self.video.append(coordenadas)
                    self.video_frame = -1
                    self.video_record_run = False

                    self.video = np.array(self.video)
                    self.predict(self.video)

                    self.video = []
        else:
            self.searchOrder(coordenadas)

        return imagem
    
    def ProcessarCoordenadas(self, lista_pontos, x, y, w, h):
        coordenadas = []
        
        self.a = 0

        for self.a in range(21):
            coordenadas.append([0, 0])
        
        matriz = np.full((100, 100), -1, dtype=int)
        
        if lista_pontos:
            for idx, ponto in enumerate(lista_pontos):
                y_rel = (ponto[1] - y) * 100 // h
                x_rel = (ponto[0] - x) * 100 // w
            
                matriz[y_rel][x_rel] = idx

        for linha in range(matriz.shape[0]):
            for coluna in range(matriz.shape[1]):
                elemento = matriz[coluna, linha]
                if elemento != -1:
                    coordenadas[elemento] = [linha, coluna]

        return coordenadas

    def searchOrder(self, coordenadas):
        pontos_ass = []

        zeros = True

        for idx, ponto in enumerate(coordenadas):
            if [ponto[1], ponto[1]] != [0, 0]:
                zeros = False
            if(idx == 4 or idx == 8 or idx == 12 or idx == 16 or idx == 20):
                pontos_ass.append([ponto[1], ponto[1]])
            
        factor = 25

        ds = []

        for i in range(len(pontos_ass)):
            if i == 4:
                ds.append(self.calcular_distancia(pontos_ass[0], pontos_ass[i]))
            else:
                ds.append(self.calcular_distancia(pontos_ass[i], pontos_ass[i + 1]))

        if not zeros:
            if (ds[0] < factor and ds[1] < factor and ds[2] < factor and ds[3] < factor and ds[4] < factor):
                self.video_record_run = True
                self.video_frame = 1
                self.tempo_anterior = time.time() * 1000
    
    def predict(self, dados):
        dados = (dados).reshape((1, 840))
    
        with open(os.devnull, 'w') as fnull:
            sys.stdout = fnull
            previsoes = self.model.predict(dados)
            sys.stdout = sys.__stdout__ 

        self.moves = [
            'Fechar Telas',
            'Print screen',
            'Ativar modo mouse virtual',
            'Aumentar o volume',
            'Ir para o canal predileto',
            'Abrir o explorador de arquivos',
            'Diminuir o volume',
            'Aumentar o brilho',
            'Diminuir o brilho',
            'Abrir a netflix',
            'Abrir o disney plus',
            'Confirmar'
        ]

        previsoes_tratadas = []
        maior = 0

        for i, previsao in enumerate(previsoes[0]):
            if previsao > previsoes[0][maior]:
                maior = i

            previsoes_tratadas.append(f"{previsao * 100:.2f}%")
        
        previsao = np.argmax(previsoes)
        
        texto = "Movimento: " + self.moves[previsao] + " - " + str(previsoes_tratadas[previsao])
        self.predictMove.emit(texto)

        previsoes_tratadas = []

    def load_model(self):
        model = load_model('../../models/modelTest.keras')

        return model
    
    def drawHand(self, nodes):
        edges = [[0, 1], 
        [1, 2], 
        [2, 3], 
        [3, 4], 
        [0, 5], 
        [5, 6], 
        [6, 7], 
        [7, 8], 
        [0, 17], 
        [5, 9], 
        [9, 13], 
        [13, 17], 
        [9, 10], 
        [10, 11], 
        [11, 12], 
        [13, 14], 
        [14, 15], 
        [15, 16], 
        [17, 18],
        [18, 19],
        [19, 20]]
    

        image_mao = nx.DiGraph()
        
        pos = {}
        node_colors = {}

        pos['pa'] = (0, 0)
        pos['pb'] = (100, 100)

        image_mao.add_node('pa')
        image_mao.add_node('pb')

        node_colors['pa'] = "#1e1e2e"
        node_colors['pb'] = "#1e1e2e"

        max_x = max(nodes, key=lambda x: x[0])[0]
        max_y = max(nodes, key=lambda x: x[1])[1]


        for i in range(21):
            image_mao.add_node(f'p{i}')

            pos[f'p{i}'] = (nodes[i][0], 100 - (nodes[i][1]))
            node_colors[f'p{i}'] = "#EE4740"
            

        for i in range(21):
            for j in range(21):
                if [i, j] in edges:
                    image_mao.add_edge(f'p{i}', f'p{j}')


        plt.figure(figsize=(10, 10))
        nx.draw(image_mao, pos, node_size=150, node_color=list(node_colors.values()), edge_color="#EE4740", arrows=False, with_labels=False)
        # nx.draw(image_mao, pos, node_size=150, node_color="#007FFF", edge_color="#003566", arrows=False, with_labels=False)
        plt.savefig("../../img/mao.png", transparent=True, dpi=300)
        
        return "Image"

    
    def calcular_distancia(self, ponto1, ponto2):
        return math.sqrt(((ponto2[0] - ponto1[0]) ** 2) + ((ponto2[1] - ponto1[1]) ** 2))

    
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
        self.video_thread.predictMove.connect(self.SetText)
        self.video_thread.handImage.connect(self.SetHand)
        self.video_thread.start()

    def __on_button_click(self):
        self.app.quit()

    def SetVideo(self, frame):
        max_width = 380
        self.label.setGeometry(20, 70, max_width, int(frame.height() / (frame.width()/max_width)))
        self.label.setPixmap(QPixmap.fromImage(frame))

    def SetText(self, texto):
        self.Texto.setText(texto)

    def SetHand(self, img):
        pixmap = QPixmap("../../img/mao.png")
        self.label2.setPixmap(pixmap)

def main():
    ui = UI()
    sys.exit(ui.app.exec_())

if __name__ == "__main__":
    main()
