import sys
import traceback
import cv2
import numpy as np
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QImage
import mediapipe as mp
from body import BodyState
from body.const import IMAGE_HEIGHT, IMAGE_WIDTH

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

BG_COLOR = (192, 192, 192)  # gray


class Cv2Thread(QThread):
    update_frame = Signal(QImage)
    update_state = Signal(dict)

    def __init__(
        self, parent=None, mp_config=None, body_config=None, events_config=None
    ):
        QThread.__init__(self, parent)
        self.status = True
        self.cap = True
        self.body = BodyState(body_config, events_config)
        self.mp_config = mp_config

    def run(self):
        print("run mediapipe", self.mp_config)
        self.cap = cv2.VideoCapture(0)
        with mp_pose.Pose(**self.mp_config) as pose:
            while self.cap.isOpened() and self.status:
                success, image = self.cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    # If loading a video, use 'break' instead of 'continue'.
                    continue

                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                # Recolor image to RGB
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                # Make detection
                results = pose.process(image)

                # Recolor back to BGR
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                if (
                    self.mp_config["enable_segmentation"]
                    and results.segmentation_mask is not None
                ):
                    try:
                        # Draw selfie segmentation on the background image.
                        # To improve segmentation around boundaries, consider applying a joint
                        # bilateral filter to "results.segmentation_mask" with "image".
                        condition = (
                            np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
                        )
                        # The background can be customized.
                        #   a) Load an image (with the same width and height of the input image) to
                        #      be the background, e.g., bg_image = cv2.imread('/path/to/image/file')
                        #   b) Blur the input image by applying image filtering, e.g.,
                        #      bg_image = cv2.GaussianBlur(image,(55,55),0)
                        bg_image = cv2.GaussianBlur(image, (55, 55), 0)
                        if bg_image is None:
                            bg_image = np.zeros(image.shape, dtype=np.uint8)
                            bg_image[:] = BG_COLOR
                        image = np.where(condition, image, bg_image)
                    except Exception:
                        print(traceback.format_exc())

                # Draw landmark annotation on the image.
                mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style(),
                )

                self.body.calculate(image, results)

                # Reading the image in RGB to display it
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                # Creating and scaling QImage
                h, w, ch = image.shape
                image = QImage(image.data, w, h, ch * w, QImage.Format_RGB888)
                image = image.scaled(IMAGE_WIDTH, IMAGE_HEIGHT, Qt.KeepAspectRatio)

                # Emit signal
                self.update_frame.emit(image)
                self.update_state.emit(dict(body=self.body))

                if cv2.waitKey(5) & 0xFF == 27:
                    break

        sys.exit(-1)
