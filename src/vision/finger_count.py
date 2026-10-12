import cv2
import mediapipe as mp

mpHand = mp.tasks.vision
mpDraw = mp.tasks.vision.drawing_utils

options = mpHand.HandLandmarkerOptions(
    base_options=mp.tasks.BaseOptions(
        model_asset_path="../models/hand_landmarker.task"
    ),
    num_hands=2
)

hands = mpHand.HandLandmarker.create_from_options(options)

def count_fingers(landmarks) -> int:
    fingers = []

    if landmarks[1].x < landmarks[0].x:
        fingers.append(landmarks[4].x < landmarks[3].x)

    else:
        fingers.append(landmarks[4].x > landmarks[3].x)

    for tips in [8, 12, 16, 20]:
        fingers.append(landmarks[tips].y < landmarks[tips - 2].y)

    return fingers.count(True)


camera = cv2.VideoCapture(0)

while True:
    good, cam = camera.read()
    rgb = cv2.cvtColor(cam, cv2.COLOR_BGR2RGB)
    mpImage = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = hands.detect(mpImage)

    if result.hand_landmarks:
        for hand in result.hand_landmarks:
            finger_count = count_fingers(hand)
            h, w, c = cam.shape

            for lm in hand:
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(cam, (cx, cy), 5, (0, 255, 0), -1)

            cv2.putText(cam, f'Fingers: {finger_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("IMG", cam)

    if cv2.waitKey(1) == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()