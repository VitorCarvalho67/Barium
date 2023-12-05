import cv2
import mediapipe as mp
import numpy as np

'''
    This is the class which can take images (either from webcam or other source) and run
    the google mediapipe on them
'''


class MediapipeHandDetection:

    def __init__(self):

        # initialize our Mediapipe variables
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands

        # detected hands
        self.detected_hands = [[-1, -1, -1], [-1, -1, -1]]       # visible, x coor, ycoor

    def CalcCenterHand(self, hand_landmarks):
        # Calculates the center of the hand
        cent_x = np.mean([hand_landmarks.landmark[point].x for point in self.mp_hands.HandLandmark])
        cent_y = np.mean([hand_landmarks.landmark[point].y for point in self.mp_hands.HandLandmark])

        return cent_x, cent_y

    def DetectSingleImg(self, image):

        with self.mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5,
                                 min_tracking_confidence=0.5) as hands:

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            imageHeight, imageWidth, _ = image.shape

            # get the center of the hands
            self.detected_hands = [[-1, -1, -1], [-1, -1, -1]]
            if results.multi_hand_landmarks:
                for i_hand in range(min(2, len(results.multi_hand_landmarks))):
                    xcent, ycent = self.CalcCenterHand(results.multi_hand_landmarks[i_hand])
                    self.detected_hands[i_hand] = [1, xcent * imageWidth, ycent * imageHeight]

        # return our detected_hands
        return self.detected_hands

    # TESTING PART :, standalone function which can be called and will draw on the image
    def StartDetection(self):
        self.cap = cv2.VideoCapture(0)

        with self.mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
            while True:
                success, image = self.cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    # If loading a video, use 'break' instead of 'continue'.
                    continue

                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = hands.process(image)

                imageHeight, imageWidth, _ = image.shape

                # get the center of the hands
                self.detected_hands = [[-1,-1,-1],[-1,-1,-1]]
                if results.multi_hand_landmarks:

                    for i_hand in range(min(2,len(results.multi_hand_landmarks))):
                        xcent, ycent = self.CalcCenterHand(results.multi_hand_landmarks[i_hand])
                        self.detected_hands[i_hand] = [1, xcent*imageWidth, ycent*imageHeight]

                # Draw the hand annotations on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        self.mp_drawing.draw_landmarks(
                            image,
                            hand_landmarks,
                            self.mp_hands.HAND_CONNECTIONS,
                            self.mp_drawing_styles.get_default_hand_landmarks_style(),
                            self.mp_drawing_styles.get_default_hand_connections_style())
                # Flip the image horizontally for a selfie-view display.

                # draw the center of the hands
                for hands_cur in self.detected_hands:
                    if hands_cur[0] == 1:
                        image = cv2.circle(image, (int(hands_cur[1]), int(hands_cur[2])), 10, (255,255,255), -1)
                    print(hands_cur)
                cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
                if cv2.waitKey(5) & 0xFF == 27:
                    break


# # TESTING : standalone version for mediapipe
# if __name__=="__main__":
#     MHD = MediapipeHandDetection()  # initialize our detection class
#     MHD.StartDetection()
