import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils
cam = cv2.VideoCapture(0)

def finger_status(hand_landmarks):
    tips = [4, 8, 12, 16, 20]
    fingers = []

    # الإبهام
    fingers.append(hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x)

    # باقي الأصابع
    for tip in tips[1:]:
        fingers.append(hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y)

    return fingers


while True:
    success, frame = cam.read()

    if not success:
        print("Camera not working")
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    text = "No Sign"

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:

            fingers = finger_status(hand_landmarks)

            # إشاراتك الأساسية
            if fingers == [0,0,0,0,0]:
                text = "Need Help"
            elif fingers == [1,1,1,1,1]:
                text = "Ganger"

            # الإشارات المطلوبة في المهمة
            elif fingers == [1,0,0,0,0]:
                text = "Goodbye"
            elif fingers == [0,1,1,0,0]:
                text = "Watch out"
            elif fingers == [0,1,0,0,0]:
                text = "Need to talk"
            elif fingers == [0,0,1,1,1]:
                text = "Please"

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.putText(frame, text, (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

    if cv2.getWindowProperty("Camera", cv2.WND_PROP_VISIBLE) < 1:
        break

cam.release()
cv2.destroyAllWindows()
