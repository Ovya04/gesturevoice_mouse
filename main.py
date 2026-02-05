from auth import setup_db, login, register
from gesture_control import run_gesture
from voice_control import run_voice
from fusion_control import run_combined

setup_db()

print("1. Register\n2. Login")
choice = input("Choose: ")

user = input("Username: ")
pwd = input("Password: ")

if choice == "1":
    if register(user, pwd):
        print("Registered successfully")
    else:
        print("User already exists")
        exit()

if not login(user, pwd):
    print("Invalid credentials")
    exit()

print("Select Mode")
print("1. Gesture")
print("2. Voice")
print("3. Combined")

mode = input("Mode: ")

if mode == "1":
    run_gesture()
elif mode == "2":
    run_voice()
elif mode == "3":
    run_combined()
