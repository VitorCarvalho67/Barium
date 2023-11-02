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
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
import networkx as nx
import matplotlib.pyplot as plt

def on_button_click():
    app.quit()

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
button.setGeometry(650, 20, 30, 30)
button.clicked.connect(on_button_click, QtCore.Qt.UniqueConnection)


btn1 = QPushButton("Mouse", window)
btn2 = QPushButton("Teclado", window)
btn3 = QPushButton("Configurações", window)
btn4 = QPushButton("Movimentos", window)
btn5 = QPushButton("Jogos", window)
Texto = QLabel("Movimento:",window)
label = QLabel("Image", window)
label2 = QLabel("Mão", window)


# ##########

# central_layout = QVBoxLayout()
# central_widget.setLayout(central_layout)
# window.setCentralWidget(central_widget)

# ##########

Texto.setGeometry(20, 400, 200, 25)
btn1.setGeometry(240, 400, 70, 25)
btn2.setGeometry(320, 400, 70, 25)
btn3.setGeometry(400, 400, 100, 25)
btn4.setGeometry(510, 400, 100, 25)
btn5.setGeometry(620, 400, 70, 25)
label.setGeometry(0, 0, 0, 0)
label2.setGeometry(0, 0, 0, 0)

Texto.setStyleSheet("color: #CDD6F4; font-size: 14px;")
btn1.setStyleSheet("background-color: #EE4740; border-radius: 10px; color: #CDD6F4; font-size: 14px;")
btn1.setGeometry(240, 400, 70, 25)
btn1.clicked.connect(on_button_click)


btn2.setStyleSheet("background-color: #EE4740; border-radius: 10px; color: #CDD6F4; font-size: 14px;")
btn3.setStyleSheet("background-color: #EE4740; border-radius: 10px; color: #CDD6F4; font-size: 14px;")
btn4.setStyleSheet("background-color: #EE4740; border-radius: 10px; color: #CDD6F4; font-size: 14px;")
btn5.setStyleSheet("background-color: #EE4740; border-radius: 10px; color: #CDD6F4; font-size: 14px;")
label.setStyleSheet("border-radius: 10px; color: #CDD6F4; font-size: 14px; background-color: #1e1e5e;")
label.setStyleSheet("border-radius: 10px; color: #CDD6F4; font-size: 14px; background-color: #1e1e5e;")


label.setGeometry(20, 70, 350, 300)
label.setAlignment(QtCore.Qt.AlignCenter)
label.setScaledContents(True)

label2.setGeometry(430, 100, 240, 240)
label2.setAlignment(QtCore.Qt.AlignCenter)
label2.setScaledContents(True)


window.show()

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

def aumentar_contraste(frame):

    alpha = 2
    beta = 0

    imagem = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

    return imagem

def calcular_distancia(ponto1, ponto2):
    return math.sqrt(((ponto2[0] - ponto1[0]) ** 2) + ((ponto2[1] - ponto1[1]) ** 2))

modo_mouse = False

cap = cv2.VideoCapture(0)
mp_maos = mp.solutions.hands
maos = mp_maos.Hands(max_num_hands=1)

while True:

    ponto_anterior = None
    matriz = None

    dados = []
    numero = -1
    iteracao = 0

    matrizes = []

    z = 0

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


    if not numero == -1 and iteracao < 20:

        pontos_ass = [] 

        tempo_atual = time.time() * 1000

        if tempo_atual - tempo_anterior >= intervalo or iteracao == 0:            
            tempo_anterior = tempo_atual

            matriz = np.full((100, 100), -1, dtype=int)
            if lista_pontos:
                for idx, ponto in enumerate(lista_pontos):
                    y_rel = (ponto[1] - y) * 100 // h
                    x_rel = (ponto[0] - x) * 100 // w
                    valor = idx

                    if(idx == 4 or idx == 8 or idx == 12 or idx == 16 or idx == 20):
                        pontos_ass.append([x_rel, y_rel])

                    matriz[y_rel][x_rel] = valor    

            iteracao += 1

    else:
        if iteracao == 20:

            dados.append(matrizes)
            iteracao = -1
            numero = -1
            matrizes = []

            valor_video = " "

            if salvar_videos:
                video.release()
                valor_video += "e vídeo "
            
            # print(f"Dados{valor_video}registrados!")

        nao_mexe_porque_assim_funciona = cv2.waitKey(1)

        nodes = []

        if len(lista_pontos) > 20:


            pontos_ass = []

            for idx, ponto in enumerate(lista_pontos):

                y_rel = (ponto[1] - y) * 100 // h
                x_rel = (ponto[0] - x) * 100 // w
                valor = idx

                if(idx == 4 or idx == 8 or idx == 12 or idx == 16 or idx == 20):
                    pontos_ass.append([x_rel, y_rel])
                
                nodes.append([x_rel, y_rel])

            factor = 25

            p4 = pontos_ass[0]
            p8 = pontos_ass[1]
            p12 = pontos_ass[2]
            p16 = pontos_ass[3]
            p20 = pontos_ass[4]

            d1 = calcular_distancia(p4, p8)
            d2 = calcular_distancia(p8, p12)
            d3 = calcular_distancia(p12, p16)
            d4 = calcular_distancia(p16, p20)
            d5 = calcular_distancia(p20, p4)


            if (d1 < factor and d2 < factor and d3 < factor and d4 < factor and d5 < factor):
                time.sleep(1)

                tempo_anterior = time.time() * 1000
                numero = 1

                z += 1
                print("Z: ",  z)

    if matriz is not None:
        for linha in range(matriz.shape[0]):
            for coluna in range(matriz.shape[1]):
                elemento = matriz[coluna, linha]
                if elemento != -1:
                    coordenadas[elemento] = [linha, coluna]
        
        foto = Image.new("RGB", (100, 100), "black")

        draw = ImageDraw.Draw(foto)

        for indice, (x,y) in enumerate(coordenadas):
            # draw.text((x,y), str(indice), fill="white")
            draw.text((x,y), str("."), fill="white")

        foto = np.array(foto)
        foto = cv2.resize(foto, (100, 100))
        
        if salvar_videos:
            video.write(foto)

        matriz = None
        diagonal = calcular_distancia((x, y), (x + w, y + h))
        referencial = ((x + w, y + h))

        linha = []

        for [x, y] in coordenadas:
            linha.append([x, y])
        
        # linha.append(referencial)
        # linha.append(diagonal)

        matrizes.append(linha)

    # cv2.imshow("Câmera", aumentar_contraste(frame))

    frame = cv2.cvtColor(aumentar_contraste(frame), cv2.COLOR_BGR2RGB)
    height_frame, width_frame, channels = frame.shape
    step = channels * width_frame
    qImg = QImage(frame.data, width_frame, height_frame, step, QImage.Format_RGB888)
    
    max_width = 380

    label.setGeometry(20, 70, max_width, int(height_frame / (width_frame/max_width)))
    label.setPixmap(QPixmap.fromImage(qImg))

    if len(nodes) > 20:

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

        print(max_x, max_y)

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

        pixmap = pixmap = QPixmap("../../img/mao.png")
        label2.setPixmap(pixmap)

    if iteracao == -1:
        iteracao = 0

        dados = np.array(dados)

        video = (dados).reshape((1, 840))

        previsoes = model.predict(video)

        movimentos = [
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
        
        max_move = max(len(x) for x in movimentos)

        previsoes_tratadas = []

        maior = 0

        for i, previsao in enumerate(previsoes[0]):
            if previsao > previsoes[0][maior]:
                maior = i

            previsoes_tratadas.append(f"{previsao * 100:.2f}%")

        
        max_pred = max(len(x) for x in previsoes_tratadas)


        # print( "┌" + "─" * (max_move + 2) + "┬" + "─" * (max_pred + 2) + "┐")
        
        # for i, previsao in enumerate(previsoes_tratadas):
        #     if i != maior:
        #         if (previsoes[0][i] * 100) > 10:
        #             print(f"│ {movimentos[i]}" + " " * (max_move - len(movimentos[i]) + 1) + "│" + f" \033[34m{previsao}\033[0m" + " " *  (max_pred - len(previsao) + 1) + "│")
        #         else:
        #             print(f"│ {movimentos[i]}" + " " * (max_move - len(movimentos[i]) + 1) + "│" + f" {previsao}" + " " *  (max_pred - len(previsao) + 1) + "│")
        #     else:
        #         print(f"│ \033[32m{movimentos[i]}\033[0m" + " " * (max_move - len(movimentos[i]) + 1) + "│" + f" \033[32m{previsao}\033[0m" + " " *  (max_pred - len(previsao) + 1) + "│")

        #     if i < (len(previsoes_tratadas) - 1):
        #         print( "├" + "─" * (max_move + 2) + "┼" + "─" * (max_pred + 2) + "┤")

        
        # print( "└" + "─" * (max_move + 2) + "┴" + "─" * (max_pred + 2) + "┘")

        previsao = np.argmax(previsoes)
        # print("\nMovimento previsto com maior certeza: ", movimentos[previsao])
        
        texto = "Movimento: " + movimentos[previsao] + " - " + str(previsoes_tratadas[previsao])
        # texto = f"Movimento: {movimentos[previsao]} - {previsoes_tratadas[previsao]}"

        Texto.setText(texto)

        # if (movimentos[previsao] == 'Fechar Telas'):
        #     print("tchau")
        #     pyautogui.hotkey('win', 'd')

        # elif(movimentos[previsao] == 'Print screen'):
        #     print("abrir a mão")
        #     pyautogui.hotkey('win', 'prtsc')
        #     pyautogui.hotkey('ctrl', 'a')
        #     pyautogui.hotkey('ctrl', 'c')

        # elif(movimentos[previsao] == 'Ativar modo mouse virtual'):
        #     print("Mouse Virtual")
        #     # mouse.mouse_virtual()
                
        # elif(movimentos[previsao] == 'Aumentar o volume'):
        #     print("para cima")
        #     devices = AudioUtilities.GetSpeakers()
        #     interface = devices.Activate(
        #         IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

        #     volume = cast(interface, POINTER(IAudioEndpointVolume))

        #     current_volume = volume.GetMasterVolumeLevelScalar()
        #     new_volume = min(1.0, current_volume + 0.1)
        #     if new_volume > 100:
        #         volume.SetMasterVolumeLevelScalar(100, None)
        #     else:
        #         volume.SetMasterVolumeLevelScalar(new_volume, None)

        # elif(movimentos[previsao] == 'Abrir o explorador de arquivos'):
        #     print("Mão reta para a esquerda")
        #     pyautogui.hotkey('win', 'e')
        
        # elif(movimentos[previsao] == 'Salvar'):
        #     pyautogui.hotkey('win', 's')
        # elif(movimentos[previsao] == 'Diminuir o volume'):
        #     devices = AudioUtilities.GetSpeakers()
        #     interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

        #     volume = cast(interface, POINTER(IAudioEndpointVolume))

        #     current_volume = volume.GetMasterVolumeLevelScalar()
        #     new_volume = min(1.0, current_volume - 0.1)
        #     if new_volume < 0:
        #         volume.SetMasterVolumeLevelScalar(0, None)
        #     else:
        #         volume.SetMasterVolumeLevelScalar(new_volume, None)
        # elif(movimentos[previsao] == 'Diminuir o volume'):
        #     print("Confirmar")
        # else:
        #     print("Movimento não reconhecido")

    input_v = 1

    if input_v == '0':
        exit

        cap.release()
        cv2.destroyAllWindows()
