import sys
import os
projeto_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(projeto_dir)

from modules import mouse
import csv
import cv2
import mediapipe as mp
import math
import numpy as np
import time
import datetime
import pytz
import pandas as pd
from keras.models import load_model
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

def on_button_click():
    app.quit()

app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("Barium")
window.setGeometry(100, 100, 700, 500)
window.setFixedSize(700, 500)
window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
window.setWindowIcon(QIcon("../../img/LOGO.ico"))
window.setStyleSheet("background-color: #1e1e2e;")

central_widget = QLabel(window)
central_widget.setPixmap(QPixmap("../../img/LogoApp.png").scaled(200, 40))
# central_widget.setGeometry(0, 0, 700, 500) Aqui as coisas ficaram no centro, mas não sei se é o melhor jeito
central_widget.setGeometry(0, 0, 250, 80)
central_widget.setAlignment(QtCore.Qt.AlignCenter)

button = QPushButton("", window)
button.setStyleSheet("background-color: #077208; border-radius: 15px;")
button.setGeometry(650, 80, 30, 30)
button.clicked.connect(on_button_click, QtCore.Qt.UniqueConnection)


btn1 = QPushButton("Mouse", window)
btn2 = QPushButton("Teclado", window)
btn3 = QPushButton("Configurações", window)
btn4 = QPushButton("Movimentos", window)
btn5 = QPushButton("Jogos", window)
Texto = QLabel("Movimento:",window)
label = QLabel("Image", window)


##########

central_layout = QVBoxLayout()
central_widget.setLayout(central_layout)
window.setCentralWidget(central_widget)

#############

Texto.setGeometry(20, 400, 100, 25)
btn1.setGeometry(200, 400, 70, 25)
btn2.setGeometry(290, 400, 70, 25)
btn3.setGeometry(380, 400, 100, 25)
btn4.setGeometry(500, 400, 100, 25)
btn5.setGeometry(620, 400, 70, 25)
label.setGeometry(0, 0, 0, 0)

Texto.setStyleSheet("color: #CDD6F4; font-size: 14px;")
btn1.setStyleSheet("background-color: #EE4740; border-radius: 10px; color: #CDD6F4; font-size: 14px;")
btn2.setStyleSheet("background-color: #EE4740; border-radius: 10px; color: #CDD6F4; font-size: 14px;")
btn3.setStyleSheet("background-color: #EE4740; border-radius: 10px; color: #CDD6F4; font-size: 14px;")
btn4.setStyleSheet("background-color: #EE4740; border-radius: 10px; color: #CDD6F4; font-size: 14px;")
btn5.setStyleSheet("background-color: #EE4740; border-radius: 10px; color: #CDD6F4; font-size: 14px;")
label.setStyleSheet("border-radius: 10px")

window.show()

tempo_previsao = time.time() * 1000

certezas = []

model = load_model("../../models/modelTest.keras")

salvar_videos = False

fusoHorario = pytz.timezone('America/Sao_Paulo')
dia_atual = (datetime.datetime.now(fusoHorario)).strftime('%Y-%m-%d %H-%M-%S')

if salvar_videos:
    diretorio = f"../video/video_{dia_atual}"
    os.makedirs(diretorio)

intervalo = 100
quantidade_de_frames = 20

exibir_conexoes = True
mostrar_numeros = True
dataset = "../../data/test.csv"

frames_gravados = 0

def aumentar_contraste(frame):

    alpha = 2
    beta = 0

    imagem = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

    return imagem

def calcular_distancia(ponto1, ponto2):
    return math.sqrt(((ponto2[0] - ponto1[0]) ** 2) + ((ponto2[1] - ponto1[1]) ** 2))

modo_mouse = False

tempo_anterior = time.time() * 1000

cap = cv2.VideoCapture(0)
mp_maos = mp.solutions.hands
maos = mp_maos.Hands(max_num_hands=1)

dados = np.zeros((1, 20, 21, 2))
matrizes = np.zeros((20, 21, 2))

while True:
    coordenadas = []
    for a in range(21):
        coordenadas.append([0, 0])

    sucesso, frame = cap.read()
    if not sucesso:
        continue

    frame = cv2.flip(frame, 1)
    

    resultados = maos.process(cv2.cvtColor(aumentar_contraste(frame), cv2.COLOR_BGR2RGB))

    lista_pontos = []

    if resultados.multi_hand_landmarks:
        for pontos_mao in resultados.multi_hand_landmarks:
            for idx, ponto in enumerate(pontos_mao.landmark):
                altura, largura, _ = frame.shape
                cx, cy = int(ponto.x * largura), int(ponto.y * altura)
                if mostrar_numeros:
                    cv2.putText(frame, str(idx), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                lista_pontos.append((cx, cy))

            if lista_pontos:
                x, y, w, h = cv2.boundingRect(np.array(lista_pontos))
                tamanho_max = max(w, h)

                centro_x = x + w // 2
                centro_y = y + h // 2

                x = centro_x - tamanho_max // 2
                y = centro_y - tamanho_max // 2

                x, y, w, h = x - 10, y - 10, tamanho_max + 20, tamanho_max + 20

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            if exibir_conexoes:
                mp.solutions.drawing_utils.draw_landmarks(frame, pontos_mao, mp_maos.HAND_CONNECTIONS)


    tempo_atual = time.time() * 1000

    if tempo_atual - tempo_anterior >= intervalo:            
        tempo_anterior = tempo_atual

        matriz = np.full((100, 100), -1, dtype=int)
        if lista_pontos:
            for idx, ponto in enumerate(lista_pontos):
                x_rel = (ponto[0] - x) * 100 // w
                y_rel = (ponto[1] - y) * 100 // h
                valor = idx
                matriz[y_rel][x_rel] = valor    

        numero = -1


    if matriz is not None:
        for linha in range(matriz.shape[0]):
            for coluna in range(matriz.shape[1]):
                elemento = matriz[coluna, linha]
                if elemento != -1:
                    coordenadas[elemento] = [linha, coluna]

        # diagonal = calcular_distancia((x, y), (x + w, y + h))
        # referencial = ((x + w, y + h))

        linha = []

        for [x, y] in coordenadas:
            linha.append([x, y])
        
        for i, video in enumerate(matrizes):
            if i > 0:
                matrizes[i - 1] = video

        matrizes[19] = linha


        dados = (np.array(matrizes)).reshape(1, 20, 21, 2)

    # cv2.imshow("Câmera", aumentar_contraste(frame))

    frame = cv2.cvtColor(aumentar_contraste(frame), cv2.COLOR_BGR2RGB)
    height_frame, width_frame, channels = frame.shape
    step = channels * width_frame
    qImg = QImage(frame.data, width_frame, height_frame, step, QImage.Format_RGB888)
    pixmap = QPixmap.fromImage(qImg)
    central_widget.setPixmap(pixmap)
    label.setScaledContents(True)

    video = (dados).reshape((1, 840))
    previsoes = model.predict(video, verbose=False)

    movimentos = ['Fechar Telas', 'Print screen', 'Ativar modo mouse virtual', 'Aumentar o volume', 'Salvar', 'Abrir o explorador de arquivos', 'Diminuir o volume', 'Aumentar o brilho', 'Diminuir o brilho', 'Control + Z', 'Control + Y', 'Confirmar']

    max_move = max(len(x) for x in movimentos)

    previsoes_tratadas = []

    maior = 0

    for i, previsao in enumerate(previsoes[0]):
        if previsao > previsoes[0][maior]:
            maior = i

        previsoes_tratadas.append(f"{previsao * 100:.2f}%")

    
    max_pred = max(len(x) for x in previsoes_tratadas)

    printar = False

    if printar:

        print( "┌" + "─" * (max_move + 2) + "┬" + "─" * (max_pred + 2) + "┐")
        for i, previsao in enumerate(previsoes_tratadas):
            if i != maior:
                if (previsoes[0][i] * 100) > 10:
                    print(f"│ {movimentos[i]}" + " " * (max_move - len(movimentos[i]) + 1) + "│" + f" \033[34m{previsao}\033[0m" + " " *  (max_pred - len(previsao) + 1) + "│")
                else:
                    print(f"│ {movimentos[i]}" + " " * (max_move - len(movimentos[i]) + 1) + "│" + f" {previsao}" + " " *  (max_pred - len(previsao) + 1) + "│")
            else:
                print(f"│ \033[32m{movimentos[i]}\033[0m" + " " * (max_move - len(movimentos[i]) + 1) + "│" + f" \033[32m{previsao}\033[0m" + " " *  (max_pred - len(previsao) + 1) + "│")

            if i < (len(previsoes_tratadas) - 1):
                print( "├" + "─" * (max_move + 2) + "┼" + "─" * (max_pred + 2) + "┤")

        
        print( "└" + "─" * (max_move + 2) + "┴" + "─" * (max_pred + 2) + "┘")

    previsao = np.argmax(previsoes)

    certeza = previsoes[0][previsao]

    certezas.append(certeza)

    if(certeza > .9):
        if time.time() * 1000 - tempo_previsao > 2000:
            print(f"{movimentos[previsao]}, {certeza*100:.2f}%")
            tempo_previsao = time.time() * 1000

    input_v = cv2.waitKey(1)

    if input_v == ord("e"):
        break


cap.release()
cv2.destroyAllWindows()

sys.exit(app.exec_())