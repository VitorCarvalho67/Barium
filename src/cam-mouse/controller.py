#!/usr/bin/env python3

import pyautogui


class GestureManager:
    def __init__(self):
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
            print("Scrolling UP")

        scrolling_down = self.index_finger_up and self.middle_finger_down and self.ring_finger_down and self.little_finger_down
        if scrolling_down:
            pyautogui.scroll(-120)
            print("Scrolling DOWN")
    

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
            print("Zooming Out")

        if zoomming_in:
            pyautogui.keyDown('ctrl')
            pyautogui.scroll(50)
            pyautogui.keyUp('ctrl')
            print("Zooming In")

    def detect_clicking(self):
        left_click_condition = self.index_finger_within_Thumb_finger and self.middle_finger_up and self.ring_finger_up and self.little_finger_up and not self.middle_finger_within_Thumb_finger and not self.ring_finger_within_Thumb_finger and not self.little_finger_within_Thumb_finger
        if not self.left_clicked and left_click_condition:
            pyautogui.click()
            self.left_clicked = True
            print("Left Clicking")
        elif not self.index_finger_within_Thumb_finger:
            self.left_clicked = False

        right_click_condition = self.middle_finger_within_Thumb_finger and self.index_finger_up and self.ring_finger_up and self.little_finger_up and not self.index_finger_within_Thumb_finger and not self.ring_finger_within_Thumb_finger and not self.little_finger_within_Thumb_finger
        if not self.right_clicked and right_click_condition:
            pyautogui.rightClick()
            self.right_clicked = True
            print("Right Clicking")
        elif not self.middle_finger_within_Thumb_finger:
            self.right_clicked = False

        double_click_condition = self.ring_finger_within_Thumb_finger and self.index_finger_up and self.middle_finger_up and self.little_finger_up and not self.index_finger_within_Thumb_finger and not self.middle_finger_within_Thumb_finger and not self.little_finger_within_Thumb_finger
        if not self.double_clicked and  double_click_condition:
            pyautogui.doubleClick()
            self.double_clicked = True
            print("Double Clicking")
        elif not self.ring_finger_within_Thumb_finger:
            self.double_clicked = False
    
    def detect_dragging(self):
        if not self.dragging and self.all_fingers_down:
            pyautogui.mouseDown(button = "left")
            self.dragging = True
            print("Dragging")
        elif not self.all_fingers_down:
            pyautogui.mouseUp(button = "left")
            self.dragging = False
