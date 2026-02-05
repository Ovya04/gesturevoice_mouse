import pyaudio
import json
import pyautogui
from vosk import Model, KaldiRecognizer
import os

def run_voice():
    print("\n--- VOICE MODE ACTIVE ---")
    print("Say: click | double click | right click | scroll up | scroll down")
    print("Say: open notepad | type hello | exit | back\n")

    model_path = "vosk-model-small-en-us-0.15"

    if not os.path.isdir(model_path):
        print("ERROR: Vosk model not found.")
        print("Download from https://alphacephei.com/vosk/models")
        return

    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)

    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=4000
    )

    stream.start_stream()
    pyautogui.FAILSAFE = False

    try:
        while True:
            data = stream.read(4000, exception_on_overflow=False)

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").lower()

                if not text:
                    continue

                print("VOICE:", text)

                # -------- COMMANDS --------
                if "click" in text:
                    pyautogui.click()

                elif "double click" in text:
                    pyautogui.doubleClick()

                elif "right click" in text:
                    pyautogui.rightClick()

                elif "scroll up" in text:
                    pyautogui.scroll(300)

                elif "scroll down" in text:
                    pyautogui.scroll(-300)

                elif "open notepad" in text:
                    os.system("notepad")

                elif "type" in text:
                    to_type = text.replace("type", "").strip()
                    pyautogui.write(to_type, interval=0.05)

                elif "back" in text:
                    print("Returning to menu...")
                    break

                elif "exit" in text or "quit" in text:
                    print("Exiting program...")
                    exit(0)

    except KeyboardInterrupt:
        print("Voice mode stopped")

    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
