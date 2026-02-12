import cv2
import mediapipe as mp
import pyautogui
import time
import math
import state


def fingers_up(hand):
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]

    states = []
    for tip, pip in zip(tips, pips):
        states.append(hand.landmark[tip].y < hand.landmark[pip].y)
    return states  # [index, middle, ring, pinky]

def distance(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)

def run_gesture():
    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)
    pyautogui.FAILSAFE = False
    screen_w, screen_h = pyautogui.size()

    print("\n--- GESTURE MODE ACTIVE ---")
    print("GESTURE → ACTION MAP")
    print("[Index] → Move mouse")
    print("[Pinch] → Left click")
    print("[Index+Middle] → Right click")
    print("[Middle only] → Double click")
    print("[Open palm] → Scroll up")
    print("[Fist] → Scroll down")
    print("[Ring only] → Next slide")
    print("[Pinky only] → Back to menu")
    print("Press 'q' → Exit program\n")

    last_click = 0

    with mp_hands.Hands(max_num_hands=1,
                        min_detection_confidence=0.7,
                        min_tracking_confidence=0.7) as hands:

        while state.GESTURE_ENABLED:

            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb)

            action_text = "No gesture"

            if result.multi_hand_landmarks:
                hand = result.multi_hand_landmarks[0]

                # 🔴 DRAW ALL 21 LANDMARKS
                mp_draw.draw_landmarks(
                    frame, hand, mp_hands.HAND_CONNECTIONS
                )

                fingers = fingers_up(hand)

                index_tip = hand.landmark[8]
                thumb_tip = hand.landmark[4]

                x = int(index_tip.x * screen_w)
                y = int(index_tip.y * screen_h)

                # MOVE
                if fingers == [True, False, False, False]:
                    pyautogui.moveTo(x, y, duration=0.03)
                    action_text = "Moving mouse"

                # LEFT CLICK (PINCH)
                if distance(index_tip, thumb_tip) < 0.035:
                    if time.time() - last_click > 0.7:
                        pyautogui.click()
                        last_click = time.time()
                        action_text = "Left Click"

                # RIGHT CLICK
                if fingers == [True, True, False, False]:
                    pyautogui.rightClick()
                    action_text = "Right Click"
                    time.sleep(0.4)

                # DOUBLE CLICK
                if fingers == [False, True, False, False]:
                    pyautogui.doubleClick()
                    action_text = "Double Click"
                    time.sleep(0.4)

                # SCROLL UP
                if fingers == [True, True, True, True]:
                    pyautogui.scroll(300)
                    action_text = "Scroll Up"
                    time.sleep(0.2)

                # SCROLL DOWN
                if fingers == [False, False, False, False]:
                    pyautogui.scroll(-300)
                    action_text = "Scroll Down"
                    time.sleep(0.2)

                # NEXT SLIDE
                if fingers == [False, False, True, False]:
                    pyautogui.press("right")
                    action_text = "Next Slide"
                    time.sleep(0.5)

                # BACK TO MENU
                if fingers == [False, False, False, True]:
                    print("Back to main menu")
                    break

            # 🟢 SHOW ACTION ON SCREEN
            cv2.putText(frame, f"ACTION: {action_text}",
                        (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2)

            cv2.imshow("Gesture Mode | Pinky = Back | q = Exit", frame)

            key = cv2.waitKey(1)
            if key == ord('q'):
                state.GESTURE_ENABLED = False
                break


        cap.release()
        cv2.destroyAllWindows()
