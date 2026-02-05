import threading
from gesture_control import run_gesture
from voice_control import run_voice

def run_combined():
    t1 = threading.Thread(target=run_gesture)
    t2 = threading.Thread(target=run_voice)

    t1.start()
    t2.start()
