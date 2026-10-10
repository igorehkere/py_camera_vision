import time

import cv2
import mediapipe as mp

camera = cv2.VideoCapture(0)

mpHand = mp.tasks.vision
mpDraw = mp.tasks.vision.drawing_utils

options = mpHand.HandLandmarkerOptions(
    base_options=mp.tasks.BaseOptions(
        model_asset_path="hand_landmarker.task"
    ),
    running_mode=mpHand.RunningMode.VIDEO,
    num_hands=2,
)

hands = mpHand.HandLandmarker.create_from_options(options)

connections = mpHand.HandLandmarksConnections.HAND_CONNECTIONS

while True:
    good, img = camera.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    mpImage = mp.Image(image_format=mp.ImageFormat.SRGB, data=imgRGB)
    timestamp = int(time.monotonic() * 1000)
    res = hands.detect_for_video(mpImage, timestamp)

    if res.hand_landmarks:
        for hand in res.hand_landmarks:
            mpDraw.draw_landmarks(img, hand, connections)

    cv2.imshow('IMAGE', img)

    if cv2.waitKey(1) == ord('q'):
        break