from .events import Events


class LegState:
    def __init__(self, side):
        self.side = side
        self.straight = None

    def update(self, events: Events, hip, knee, ankle, hip_angle, knee_angle):
        self.straight = knee_angle > 160

    def __str__(self):
        states = ("straight" if self.straight else "",)
        states = filter(lambda s: s != "", states)
        return ", ".join(states)


class LegsState:

    KNEE_UP_MAX_ANGLE = 155

    KNEE_MIN_VISIBILITY = 0.5

    def __init__(self):
        self.left = LegState("left")
        self.right = LegState("right")

        self.left_up_state = False
        self.right_up_state = False
        self.squat = False
        self.steps = 0

    def update(
        self,
        mode: str,
        events: Events,
        left_hip,
        right_hip,
        left_knee,
        right_knee,
        left_ankle,
        right_ankle,
        left_hip_angle,
        right_hip_angle,
        left_knee_angle,
        right_knee_angle,
    ):
        self.left.update(
            events,
            left_hip,
            left_knee,
            left_ankle,
            left_hip_angle,
            left_knee_angle,
        )
        self.right.update(
            events,
            right_hip,
            right_knee,
            right_ankle,
            right_hip_angle,
            right_knee_angle,
        )

        if mode == "Driving":
            return

        if (
            left_knee[3] > self.KNEE_MIN_VISIBILITY
            and right_knee[3] > self.KNEE_MIN_VISIBILITY
        ):
            if (
                left_knee_angle < self.KNEE_UP_MAX_ANGLE
                and right_knee_angle < self.KNEE_UP_MAX_ANGLE
            ):
                if not self.squat:
                    self.squat = True
                    events.add("squat")
            else:
                self.squat = False

            if self.squat:
                return

            if left_knee_angle < self.KNEE_UP_MAX_ANGLE:
                if not self.left_up_state:
                    self.left_up_state = True
                    self.steps += 1
            else:
                self.left_up_state = False

            if right_knee_angle < self.KNEE_UP_MAX_ANGLE:
                if not self.right_up_state:
                    self.right_up_state = True
                    self.steps += 1
            else:
                self.right_up_state = False

    def __str__(self):
        return f"steps: {self.steps}"
