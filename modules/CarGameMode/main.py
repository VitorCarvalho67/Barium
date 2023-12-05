import cv2
import vgamepad as vg
from Mediapipe_hand_detection import MediapipeHandDetection
import math


class VirtualSteering:

    def __init__(self):
        print("Initializing the VirtualSteeringClass")
        self.cap = cv2.VideoCapture(0)

        window_size = 1280, 720
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, window_size[0])            # Set the size of our capture
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, window_size[1])

        # MediapipeHandDetection
        self.MHD = MediapipeHandDetection()

        # Gamepad values
        self.gamepad = vg.VX360Gamepad()

        # steering wheel options:
        self.wheel_r = int(window_size[0]*0.2)              # current radius
        self.wheel_r_acc_max = int(window_size[0]*0.3)      # this is the biggest radius, at which acc will become max
        self.wheel_r_acc_min = int(window_size[0]*0.2)      # if radius becomes more than this, we accelerate
        self.wheel_r_decc_max = int(window_size[0]*0.015)   # minimum radius, at which decceleration
        self.wheel_r_decc_min = int(window_size[0]*0.15)    # if below this, we start braking

        self.wheel_r_acc_max = 350/2
        self.wheel_r_acc_min = 275/2
        self.wheel_r_decc_max = 125/2
        self.wheel_r_decc_min = 225/2

        self.wheel_angle = 0
        self.wheel_cent = (0,0)
        self.wheel_spoke1 = (0,0)         # the spokes of the steering wheel
        self.wheel_spoke2 = (0,0)
        self.wheel_spoke3 = (0,0)

        self.wheel_color_norm = (255,255,255)
        self.wheel_color_acc = (0, 255,0)
        self.wheel_color_decc = (0, 0, 255)
        self.wheel_color_cur = self.wheel_color_norm

        self.joystickvalues = 0         # for gamepad sample

        self.hand_left = []
        self.hand_right = []
        self.hist_n = 5             # how many frames we are

        self.xl, self.yl = -1, -1
        self.xr, self.yr = -1, -1

    def UpdateDetectedHandsHistory(self, all_hands):

        # just update based on detection
        self.xl = -1
        self.yl = -1
        self.xr = -1
        self.yr = -1
        if all_hands[0][0] != -1:
            self.xl, self.yl = all_hands[0][1], all_hands[0][2]
        if all_hands[1][0] != -1:
            self.xr, self.yr = all_hands[1][1], all_hands[1][2]


    def UpdateGamePad(self):

        # print(self.wheel_r)
        # print(self.wheel_angle)     # this means stuff, [90, -90], which is the difference between straight

        # we need to input the stuff
        ang_joystick = self.wheel_angle*1.0+90
        # print(f"Ang joystick : {ang_joystick}")

        xjoystick = 32768 * math.cos(math.radians(ang_joystick))
        yjoystick = 32768 * math.sin(math.radians(ang_joystick))

        xjoystick = int(min(max(xjoystick, -32768), 32767))
        yjoystick = int(min(max(yjoystick, -32768), 32767))
        # print(xjoystick, yjoystick)
        self.gamepad.left_joystick(x_value=xjoystick, y_value=yjoystick)  # values between -32768 and 32767

        if self.wheel_r > self.wheel_r_acc_min:
            right_trigger_val = abs(255 * 3 * (self.wheel_r - self.wheel_r_acc_min)/(self.wheel_r_acc_max - self.wheel_r_acc_min))
            right_trigger_val = min(255, max(0, int(right_trigger_val)))
            left_trigger_val = 0
            # print(right_trigger_val, left_trigger_val)
        elif self.wheel_r<self.wheel_r_decc_min:
            right_trigger_val = 0
            left_trigger_val = abs(255 * 3 * (self.wheel_r - self.wheel_r_decc_min) / (self.wheel_r_decc_min - self.wheel_r_decc_max))
            left_trigger_val = min(255,max(0, int(left_trigger_val)))
            # print(right_trigger_val, left_trigger_val)
        else:
            right_trigger_val = 0
            left_trigger_val = 0
            # print(right_trigger_val, left_trigger_val)

        self.gamepad.left_trigger(value=left_trigger_val)  # value between 0 and 255
        self.gamepad.right_trigger(value=right_trigger_val)  # value between 0 and 255

        # this updates the game with the gamepad
        self.gamepad.update()  # send the updated state to the computer

    def GetAvgHandValues(self, hand_to_avg):

        if len(hand_to_avg) > 0:
            hand_x = 0
            hand_y = 0
            for i in range(len(hand_to_avg)):
                hand_x += hand_to_avg[i][1]
                hand_y += hand_to_avg[i][2]
            hand_x /= len(hand_to_avg)
            hand_y /= len(hand_to_avg)
        else:
            hand_x, hand_y = -1, -1
        return hand_x, hand_y

    def UpdateWheelValues(self):

        if self.xl != -1 and self.yl != -1 and self.xr != -1 and self.yr != -1:    # both hands visible, lets update
            self.wheel_cent = (int((self.xl+self.xr)/2), int((self.yl+self.yr)/2))
            self.wheel_r = int(math.sqrt(math.pow(self.xl-self.xr, 2) + math.pow(self.yl - self.yr, 2))/2)
            self.wheel_angle = math.degrees(math.atan((self.yr - self.wheel_cent[1]) / (self.xr - self.wheel_cent[0])))

            # visual, get the spokes
            p1_alpha = self.wheel_angle + 45 + 180
            p2_alpha = self.wheel_angle + 135 + 180
            p3_alpha = self.wheel_angle + 270 + 180

            self.wheel_spoke1 = (int(self.wheel_cent[0] + math.cos(math.radians(p1_alpha)) * self.wheel_r),
                  int(self.wheel_cent[1] + math.sin(math.radians(p1_alpha)) * self.wheel_r))
            self.wheel_spoke2 = (int(self.wheel_cent[0] + math.cos(math.radians(p2_alpha)) * self.wheel_r),
                  int(self.wheel_cent[1] + math.sin(math.radians(p2_alpha)) * self.wheel_r))
            self.wheel_spoke3 = (int(self.wheel_cent[0] + math.cos(math.radians(p3_alpha)) * self.wheel_r),
                  int(self.wheel_cent[1] + math.sin(math.radians(p3_alpha)) * self.wheel_r))

            # colorize
            if self.wheel_r>self.wheel_r_acc_min:
                self.wheel_color_cur = self.wheel_color_acc
            elif self.wheel_r<self.wheel_r_decc_min:
                self.wheel_color_cur = self.wheel_color_decc
            else:
                self.wheel_color_cur = self.wheel_color_norm

    def StartDetection(self):
        print("We started our detection")

        while True:
            success, image = self.cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # run the Hand detection using mediapipe, which results in a list [[-1/1, xcoor, ycoor],[-1/1, xcoor, ycoor]
            all_hands = self.MHD.DetectSingleImg(image)           # mediapipe specific

            # smoothing over history
            self.UpdateDetectedHandsHistory(all_hands=all_hands)

            # Update the steering wheel position (using, self.xl, self.yl, self.xr, self.yr)
            self.UpdateWheelValues()

            # update gamepad
            self.UpdateGamePad()

            # visuals: Draw the center of the detected hands
            for hands_cur in all_hands:
                if hands_cur[0] == 1:
                    image = cv2.circle(image, (int(hands_cur[1]), int(hands_cur[2])), 12, (0, 0, 0), -1)
                    image = cv2.circle(image, (int(hands_cur[1]), int(hands_cur[2])), 10, (255, 255, 255), -1)

            # our smoothed keypoints
            if self.xl != -1 and self.yl != -1:
                image = cv2.circle(image, (int(self.xl), int(self.yl)), 12, (0, 0, 0), -1)
                image = cv2.circle(image, (int(self.xl), int(self.yl)), 10, (255, 0, 255), -1)
            if self.xr != -1 and self.yr != -1:
                image = cv2.circle(image, (int(self.xr), int(self.yr)), 12, (0, 0, 0), -1)
                image = cv2.circle(image, (int(self.xr), int(self.yr)), 10, (255, 0, 255), -1)

            # visuals, draw the wheel and its spokes
            image = cv2.circle(image, self.wheel_cent, self.wheel_r, self.wheel_color_cur, 5)
            image = cv2.line(image, self.wheel_cent, self.wheel_spoke1, self.wheel_color_cur, 5)
            image = cv2.line(image, self.wheel_cent, self.wheel_spoke2, self.wheel_color_cur, 5)
            image = cv2.line(image, self.wheel_cent, self.wheel_spoke3, self.wheel_color_cur, 5)

            # show it
            image = cv2.flip(image, 1)
            cv2.imshow('image', image)
            cv2.waitKey(1)


if __name__ == "__main__":

    VS = VirtualSteering()
    VS.StartDetection()
