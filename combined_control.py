import threading
from gesture_control import run_gesture_move_only
from voice_control import run_voice

def run_combined():
    print("""
COMBINED MODE – MULTIMODAL CONTROL
----------------------------------
Gesture  → Cursor movement
Voice    → Action trigger
Say "back" to return, "exit" to quit
""")

    gesture_thread = threading.Thread(
        target=run_gesture_move_only, daemon=True
    )
    gesture_thread.start()

    run_voice()  # voice controls actions
