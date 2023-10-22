import cv2
import mediapipe as mp
import math
import numpy as np
import pyautogui

def mouse_virtual():
    cx = cy = 0
    
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    sensitivity_factor = 1.5
    captura = cv2.VideoCapture(0)
    maos = mp_hands.Hands(max_num_hands=1)

    def calcular_distancia(ponto1, ponto2):
        return math.sqrt(((ponto2[0] - ponto1[0]) ** 2) + ((ponto2[1] - ponto1[1]) ** 2))

    while True:
        sucesso, frame = captura.read()
        if not sucesso:
            continue

        frame = cv2.flip(frame, 1)

        resultados = maos.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        list_hand_joints = []

        if resultados.multi_hand_landmarks:
            for handLms in resultados.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h, w, _ = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)

                    list_hand_joints.append((cx, cy))


                    if id == 8:
                        if abs(pyautogui.position()[0] - cx * sensitivity_factor) < 20 and abs(pyautogui.position()[1] - cy * sensitivity_factor) < 20:
                            pyautogui.moveTo(cx * sensitivity_factor, cy * sensitivity_factor)
                        else:
                            print(abs(cx0 - cx), abs(cy0 - cy))

                        cx0 = cx
                        cy0 = cy

                mp_drawing.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

        if list_hand_joints:
            clickESegura = calcular_distancia(list_hand_joints[8], list_hand_joints[4])
            clickBtnDireito = calcular_distancia(list_hand_joints[12], list_hand_joints[4])
            clickSimples = calcular_distancia(list_hand_joints[20], list_hand_joints[4])

            n1 = list_hand_joints[8][1] - list_hand_joints[7][1]
            n2 = list_hand_joints[12][1] - list_hand_joints[11][1]
            n3 = list_hand_joints[16][1] - list_hand_joints[15][1]

            if clickESegura < 20:
                pyautogui.mouseDown()
            else:
                pyautogui.mouseUp()

            if clickSimples < 20:
                pyautogui.click()
            if clickBtnDireito < 20:
                pyautogui.click(button='right')

            if n1 > 0 and n2 > 0 and n3 > 0:
                print(n1, n2, n3)
                break

    captura.release()
    cv2.destroyAllWindows()
    
mouse_virtual()