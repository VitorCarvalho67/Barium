import numpy as np
from typing import Literal
from .const import IMAGE_WIDTH, IMAGE_HEIGHT


def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(
        a[1] - b[1], a[0] - b[0]
    )
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle


def calculate_slope(a, b):
    a = np.array(a)
    b = np.array(b)

    angle = np.arctan((b[1] - a[1]) / (b[0] - a[0]))
    angle = angle * 180.0 / np.pi

    return angle


def calculate_distance(a, b):
    a = np.array(a)
    b = np.array(b)

    distance = np.linalg.norm(a - b)

    return distance


def vec_length(v: np.array):
    return np.sqrt(sum(i**2 for i in v))


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def look_at(eye: np.array, target: np.array):
    axis_z = normalize((eye - target))
    if vec_length(axis_z) == 0:
        axis_z = np.array((0, -1, 0))

    axis_x = np.cross(np.array((0, 0, 1)), axis_z)

    if vec_length(axis_x) == 0:
        axis_x = np.array((1, 0, 0))

    axis_y = np.cross(axis_z, axis_x)
    rot_matrix = np.matrix([axis_x, axis_y, axis_z]).transpose()

    return rot_matrix


def get_side_facing(elements):
    left = np.array([0, 0, 0], dtype=np.float32)
    right = np.array([0, 0, 0], dtype=np.float32)

    for [right_element, left_element] in elements:
        right += np.array(
            [
                right_element[0],
                right_element[1],
                right_element[2],
            ],
            dtype=np.float32,
        )
        left += np.array(
            [
                left_element[0],
                left_element[1],
                left_element[2],
            ],
            dtype=np.float32,
        )

    right /= len(elements)
    left /= len(elements)

    orient = look_at(left, right)

    angle_x = np.arctan2(orient[2, 1], orient[2, 2])
    angle_z = np.arctan2(orient[1, 0], orient[0, 0])

    angle_x = angle_x * 180 / np.pi
    angle_z = angle_z * 180 / np.pi

    # print(angle_x, angle_z)

    if angle_z > 0:
        angles = [
            [[0, 36], ["left"]],
            [[36, 70], ["front", "left"]],
            [[70, 110], ["front"]],
            [[110, 144], ["front", "right"]],
            [[144, 180], ["right"]],
        ]

        for angle in angles:
            if angle[0][0] <= angle_x <= angle[0][1]:
                return angle[1]

    else:
        angles = [
            [[0, 10], ["left"]],
            [[10, 70], ["back", "left"]],
            [[70, 110], ["back"]],
            [[110, 170], ["back", "right"]],
            [[170, 180], ["right"]],
        ]

        for angle in angles:
            if angle[0][0] <= angle_x <= angle[0][1]:
                return angle[1]


def is_landmarks_closed(landmarks: list, max_distance: float):
    if len(landmarks) < 2:
        return False
    i = 0
    while i < len(landmarks) - 1:
        j = i + 1

        l1 = landmarks[i]
        l2 = landmarks[j]

        if np.abs(l1[0] - l2[0]) > max_distance or np.abs(l1[1] - l2[1]) > max_distance:
            return False

        i += 1
    return True


def is_landmarks_in_rectangle(
    landmarks: list, x: float, y: float, width: float, height: float
):
    for landmark in landmarks:
        if not in_range(landmark[0] * IMAGE_WIDTH, x, x + width) or not in_range(
            landmark[1] * IMAGE_HEIGHT, y, y + height
        ):
            return False
    return True


def compare_nums(
    a: float, b: float, operator: Literal["eq", "ne", "gt", "lt", "gte", "lte"]
):
    if operator == "eq":
        return a == b
    elif operator == "ne":
        return a != b
    elif operator == "gt":
        return a > b
    elif operator == "lt":
        return a < b
    elif operator == "gte":
        return a >= b
    elif operator == "lte":
        return a <= b


def in_range(a: float, min: float, max: float):
    return a > min and a < max


def get_landmark_coordinates(landmarks, landmark):
    value = landmarks[landmark.value]
    return [
        value.x,
        value.y,
        value.z,
        value.visibility,
    ]


def log_landmark(landmark):
    l = list(
        map(lambda n: None if not n else f"{' ' if n > 0 else ''}{n:.2f}", landmark)
    )
    return f"x: {l[0]}, y: {l[1]}, z: {l[2]}, v: {l[3]}"


def log_angle(angle):
    return f"{angle:.1f}"
