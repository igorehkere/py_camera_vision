import cv2
import mediapipe as mp

mpHands= mp.tasks.vision
mpDraw = mp.tasks.vision.drawing_utils

def finger_ok(landmarks) -> bool:
    ok = False

    if (abs(landmarks[4].y - landmarks[8].y) < 0.07) and (abs(landmarks[4].x - landmarks[8].x) < 0.07):
        ok = True

    return ok

options = mpHands.HandLandmarkerOptions(
    base_options=mp.tasks.BaseOptions(
        model_asset_path="../hand_landmarker.task"
    ),
    num_hands=2
)

hands = mpHands.HandLandmarker.create_from_options(options)
camera = cv2.VideoCapture(0)

while True:
    good, img = camera.read()

    rgbImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mpImg = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgbImg)
    result = hands.detect(mpImg)

    if result.hand_landmarks:
        for hand in result.hand_landmarks:
            ok_finger = finger_ok(hand)

            h, w, c = img.shape
            for lm in hand:
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(img, (cx, cy), 5, (0, 255, 0), -1)

            text_finger = ""
            if ok_finger:
                text_finger = "OK"

            cv2.putText(img, f'Fingers: {text_finger}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("img", img)

    if cv2.waitKey(1) == ord("q"):
        break