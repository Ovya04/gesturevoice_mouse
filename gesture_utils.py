def fingers_up(hand_landmarks):
    tips = [4, 8, 12, 16, 20]
    pips = [2, 6, 10, 14, 18]

    fingers = []
    for tip, pip in zip(tips[1:], pips[1:]):  # exclude thumb first
        fingers.append(hand_landmarks.landmark[tip].y <
                       hand_landmarks.landmark[pip].y)
    return fingers  # [index, middle, ring, pinky]
