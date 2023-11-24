import cv2
from .events import Events
from .utils import (
    compare_nums,
    is_landmarks_closed,
    calculate_slope,
    calculate_distance,
    in_range,
    is_landmarks_in_rectangle,
)
from .const import IMAGE_HEIGHT, IMAGE_WIDTH, DRIVING_UP_AREA


class ArmState:

    CURL_MAX_ANGLE = 45

    def __init__(self, side):
        self.side = side

        self.straight = None
        self.curl = None
        self.up = None
        self.front = None
        self.raised = None

    @property
    def is_left(self):
        return self.side == "left"

    def update(
        self,
        events: Events,
        shoulder,
        elbow,
        wrist,
        pinky,
        index,
        thumb,
        shoulder_angle,
        elbow_angle,
    ):
        self.straight = elbow_angle > 160
        self.up = shoulder_angle > 45
        self.front = wrist[2] > shoulder[2]
        self.curl = elbow_angle < self.CURL_MAX_ANGLE
        self.raised = wrist[1] < shoulder[1]

    def __str__(self):
        states = (
            "straight" if self.straight else "",
            "curl" if self.curl else "",
            "up" if self.up else "down",
            "front" if self.front else "back",
        )
        states = filter(lambda s: s != "", states)
        return ", ".join(states)


class ArmsState:

    ELBOW_CROSS_MAX_ANGLE = 60

    DRIVING_SLOPE_ANGLE = 25

    def __init__(self):
        self.left = ArmState("left")
        self.right = ArmState("right")

        self.crossed = None
        self.left_swing = None
        self.left_swing_up = None
        self.right_swing = None
        self.right_swing_up = None
        self.hold_hands = None

        self.driving_hands = None

    def update(
        self,
        mode: str,
        image,
        events: Events,
        nose,
        left_shoulder,
        right_shoulder,
        left_elbow,
        right_elbow,
        left_wrist,
        right_wrist,
        left_pinky,
        right_pinky,
        left_index,
        right_index,
        left_thumb,
        right_thumb,
        left_shoulder_angle,
        right_shoulder_angle,
        left_elbow_angle,
        right_elbow_angle,
    ):
        self.left.update(
            events,
            left_shoulder,
            left_elbow,
            left_wrist,
            left_pinky,
            left_index,
            left_thumb,
            left_shoulder_angle,
            left_elbow_angle,
        )
        self.right.update(
            events,
            right_shoulder,
            right_elbow,
            right_wrist,
            right_pinky,
            right_index,
            right_thumb,
            right_shoulder_angle,
            right_elbow_angle,
        )

        left_right_hands_slope = calculate_slope(left_thumb, right_thumb)

        if mode == "Driving":
            if is_landmarks_closed(
                [
                    left_pinky,
                    right_pinky,
                    left_index,
                    right_index,
                    left_thumb,
                    right_thumb,
                ],
                0.3,
            ):
                self.driving_hands = True

                cv2.circle(
                    image,
                    (
                        int((left_thumb[0] + right_thumb[0]) / 2 * IMAGE_WIDTH),
                        int((left_thumb[1] + right_thumb[1]) / 2 * IMAGE_HEIGHT),
                    ),
                    50,
                    (255, 0, 0),
                    5,
                )

                # 2 hands are in driving up area
                if is_landmarks_in_rectangle(
                    [
                        left_pinky,
                        right_pinky,
                        left_index,
                        right_index,
                        left_thumb,
                        right_thumb,
                    ],
                    **DRIVING_UP_AREA,
                ):
                    events.add("d2_driving_up")

                if left_right_hands_slope > self.DRIVING_SLOPE_ANGLE:
                    events.add("d1_driving_left")
                elif left_right_hands_slope < -self.DRIVING_SLOPE_ANGLE:
                    events.add("d1_driving_right")
                else:
                    events.add("d1_driving_default")
            else:
                self.driving_hands = False

            return

        # if left_right_hands_slope < 10 and is_landmarks_closed(
        #     [
        #         left_pinky,
        #         right_pinky,
        #         left_index,
        #         right_index,
        #         left_thumb,
        #         right_thumb,
        #     ],
        #     0.1,
        # ):
        #     if not self.hold_hands:
        #         self.hold_hands = True
        #         events.add("hold_hands")
        # else:
        #     self.hold_hands = False

        # if self.hold_hands:
        #     return

        if (
            compare_nums(left_wrist[0], right_wrist[0], "lt")
            and left_elbow_angle < self.ELBOW_CROSS_MAX_ANGLE
            and right_elbow_angle < self.ELBOW_CROSS_MAX_ANGLE
        ):
            if not self.crossed:
                self.crossed = True
                events.add("cross")
        else:
            self.crossed = False

        if self.crossed:
            return

        if compare_nums(left_wrist[0], nose[0], "lt"):
            if not self.left_swing:
                self.left_swing = True
                events.add(f"left_swing{'_hold' if self.right.raised else ''}")
        else:
            self.left_swing = False

        if compare_nums(left_wrist[0], nose[0], "gt") and self.left.raised:
            if not self.left_swing_up:
                self.left_swing_up = True
                events.add("left_swing_up")
        else:
            self.left_swing_up = False

        if compare_nums(right_wrist[0], nose[0], "gt"):
            if not self.right_swing:
                self.right_swing = True
                events.add(f"right_swing{'_hold' if self.left.raised else ''}")
        else:
            self.right_swing = False

        if compare_nums(right_wrist[0], nose[0], "lt") and self.right.raised:
            if not self.right_swing_up:
                self.right_swing_up = True
                events.add("right_swing_up")
        else:
            self.right_swing_up = False

    def __str__(self):
        return f""
