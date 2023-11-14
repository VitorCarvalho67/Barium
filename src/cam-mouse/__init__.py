#!/usr/bin/env python3

import cv2
import mediapipe as mp
import logging
from controller import GestureManager

logging.basicConfig(level=logging.DEBUG)

manager = GestureManager()

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
logging.info("[OK]: Cam Mouse inicialized")

while True:
    ret, frame = cap.read()

    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgbFrame)

    if results.multi_hand_landmarks:
        if len(results.multi_hand_landmarks) == 1:
            manager.hand_Landmarks = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, manager.hand_Landmarks, mp_hands.HAND_CONNECTIONS)
        manager.update_fingers_status()
        manager.cursor_moving()
        manager.detect_scrolling()
        manager.detect_zoomming()
        manager.detect_clicking()
        manager.detect_dragging()
        cv2.imshow('Hand Tracking', frame)
        if cv2.waitKey(5) & 0xff == 27:
            break

    cv2.imshow('Hand Tracking', frame)
    if cv2.waitKey(10) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

