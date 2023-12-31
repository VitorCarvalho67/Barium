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

model = load_model("../../models/modelImage2.keras")

salvar_videos = False

fusoHorario = pytz.timezone('America/Sao_Paulo')
dia_atual = (datetime.datetime.now(fusoHorario)).strftime('%Y-%m-%d %H-%M-%S')

if salvar_videos:
    diretorio = f"../../video/video_{dia_atual}"
    os.makedirs(diretorio)

intervalo = 100
quantidade_de_frames = 20

exibir_conexoes = True
mostrar_numeros = True
dataset = "../../data/test.csv"

def aumentar_contraste(frane):

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

    while True:
        coordenadas = []
        for a in range(21):
            coordenadas.append((0, 0))

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

        cv2.imshow("Câmera", aumentar_contraste(frame))

        if not numero == -1 and iteracao < 20:
            tempo_atual = time.time() * 1000

            if tempo_atual - tempo_anterior >= intervalo or iteracao == 0:            
                tempo_anterior = tempo_atual

                matriz = np.full((100, 100), -1, dtype=int)
                if lista_pontos:
                    for idx, ponto in enumerate(lista_pontos):
                        x_rel = (ponto[0] - x) * 100 // w
                        y_rel = (ponto[1] - y) * 100 // h
                        valor = idx
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
                
            key = cv2.waitKey(1) & 0xFF


            if key in range(ord('0'), ord('9') + 1) and lista_pontos:
                numero = chr(key)

                tempo_anterior = time.time() * 1000 

                if salvar_videos:
                    m_video = f'{diretorio}/video_{z}.mp4'
                    duracao_frame = 10

                    pre = cv2.VideoWriter_fourcc(*'mp4v')
                    video = cv2.VideoWriter(m_video, pre, duracao_frame, (100, 100))


                z += 1

        if matriz is not None:
            for linha in range(matriz.shape[0]):
                for coluna in range(matriz.shape[1]):
                    elemento = matriz[coluna, linha]
                    if elemento != -1:
                        coordenadas[elemento] = ((linha, coluna))

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

            for (x, y) in coordenadas:
                linha.append(str((x, y)))
            
            linha.append(referencial)
            linha.append(diagonal)

            matrizes.append(linha)

        if iteracao == -1:
            iteracao = 0
            break

    file = dataset

    dados_tratados = []

    for linha in dados:
        linha = [item for sublista in linha for item in sublista]

        dados_tratados.append(linha)

    with open(file, mode='a', newline='') as arquivo:
        escrever = csv.writer(arquivo, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for linha in dados_tratados:
            escrever.writerow(linha)


    def texto_array(text):
        x, y = map(int, text.strip('()').split(', '))
        return [x, y]

    dataset = "../../data/test.csv"
    dados = pd.read_csv(dataset)

    # Mudei aqui
    colunas_referencial = dados.filter(like='referencial', axis=1).columns
    colunas_diagonal = dados.filter(like='diagonal', axis=1).columns

    colunas_para_remover = colunas_referencial.union(colunas_diagonal)
    x = dados.drop(columns=colunas_para_remover)
    # Até aqui

    x = np.array(x)

    videos = np.zeros((x.shape[0], 20, 21, 2))

    count_videos = 0

    for video in x:

        count_coord = 0
        count_img = 0

        imagens = np.zeros((20, 21, 2))

        imagem = np.zeros((21, 2))
        for coordenada in video:

            array = texto_array(coordenada)
            imagem[count_coord][0], imagem[count_coord][1] = array[0], array[1] 
            
            if count_coord <= 19:
                count_coord += 1

            else:
                imagens[count_img] = imagem
                imagem = np.zeros((21, 2))
                count_img += 1
                count_coord = 0
                
        videos[count_videos] = imagens
        count_videos += 1

    saida = np.zeros((videos.shape[0], 20, 100, 100), dtype=int)

    for a in range(x.shape[0]):
        video = videos[a]
        video_imagem = np.zeros((20, 100, 100), dtype=int)
        for im in range(video.shape[0]):
            coordenadas = video[im]
            imagem = np.full((100, 100), -1, dtype=int)
            for i, [x_c, y_c] in enumerate(coordenadas):
                if 0 <= x_c < 100 and 0 <= y_c < 100:
                    imagem[int(x_c),int(y_c)] = (1 + i) / 22
            video_imagem[im] = imagem
        saida[a] = video_imagem

    video = (saida[(saida.shape[0]) - 1]).reshape((1, 20, 100, 100))

    previsoes = model.predict(video)

    movimentos = ['Fechar Telas', 'Print screen', 'Ativar modo mouse virtual', 'Aumentar o volume', 'Salvar', 'Abrir o explorador de arquivos', 'Diminuir o volume', 'Aumentar o brilho', 'Diminuir o brilho', 'Control + Z', 'Control + Y', 'Confirmar']

    dc = {}

    for i, probabilidade in enumerate(np.array(previsoes)[0]):
        dc[f'{i}'] = (probabilidade * 100)

    pc_ord = [(movimento, porcentagem) for movimento, porcentagem in dc.items()]

    movimentos_ordenados = sorted(pc_ord, key=lambda x: x[1], reverse=True)
    
    strs = []

    for (a, b) in movimentos_ordenados:
        strs.append(f"| {movimentos[a]} | {b:.2f} |s")

    print(strs)

    previsao = np.argmax(previsoes)
    print("\nMovimento previsto com maior certeza: ", movimentos[previsao])

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
