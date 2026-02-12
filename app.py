import customtkinter as ctk
import threading
import sys

import state
from auth import setup_db, login, register
from gesture_control import run_gesture
from voice_control import run_voice
from fusion_control import run_combined

setup_db()

# ---------------- APPEARANCE ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ---------------- MAIN WINDOW ----------------
app = ctk.CTk()
app.title("Gesture & Voice Control System")
app.geometry("750x600")
app.resizable(False, False)

# ---------------- LOG REDIRECTION ----------------
class Redirect:
    def __init__(self, textbox):
        self.textbox = textbox

    def write(self, text):
        self.textbox.insert("end", text)
        self.textbox.see("end")

    def flush(self):
        pass

# ---------------- FUNCTIONS ----------------
def show_dashboard():
    login_frame.pack_forget()
    dashboard_frame.pack(fill="both", expand=True)

def handle_login():
    user = username_entry.get()
    pwd = password_entry.get()

    if login(user, pwd):
        print(f"\nUser '{user}' logged in successfully\n")
        show_dashboard()
    else:
        status_label.configure(text="Invalid Credentials", text_color="red")

def handle_register():
    user = username_entry.get()
    pwd = password_entry.get()

    if register(user, pwd):
        status_label.configure(text="Registered Successfully", text_color="green")
    else:
        status_label.configure(text="User Already Exists", text_color="red")

def start_gesture():
    if not state.GESTURE_ENABLED:
        state.GESTURE_ENABLED = True
        print("\nStarting Gesture Mode...\n")
        threading.Thread(target=run_gesture, daemon=True).start()

def start_voice():
    if not state.VOICE_ENABLED:
        state.VOICE_ENABLED = True
        print("\nStarting Voice Mode...\n")
        threading.Thread(target=run_voice, daemon=True).start()

def start_combined():
    if not state.GESTURE_ENABLED and not state.VOICE_ENABLED:
        state.GESTURE_ENABLED = True
        state.VOICE_ENABLED = True
        print("\nStarting Combined Mode...\n")
        threading.Thread(target=run_combined, daemon=True).start()

def stop_all():
    state.GESTURE_ENABLED = False
    state.VOICE_ENABLED = False
    print("\nAll modes stopped.\n")

# ---------------- LOGIN FRAME ----------------
login_frame = ctk.CTkFrame(app)
login_frame.pack(fill="both", expand=True)

title_label = ctk.CTkLabel(login_frame,
                           text="Gesture & Voice Control System",
                           font=("Arial", 24))
title_label.pack(pady=40)

username_entry = ctk.CTkEntry(login_frame,
                              placeholder_text="Username",
                              width=250)
username_entry.pack(pady=10)

password_entry = ctk.CTkEntry(login_frame,
                              placeholder_text="Password",
                              show="*",
                              width=250)
password_entry.pack(pady=10)

login_button = ctk.CTkButton(login_frame,
                             text="Login",
                             width=200,
                             command=handle_login)
login_button.pack(pady=10)

register_button = ctk.CTkButton(login_frame,
                                text="Register",
                                width=200,
                                command=handle_register)
register_button.pack(pady=5)

status_label = ctk.CTkLabel(login_frame, text="")
status_label.pack(pady=10)

# ---------------- DASHBOARD FRAME ----------------
dashboard_frame = ctk.CTkFrame(app)

dashboard_title = ctk.CTkLabel(dashboard_frame,
                               text="Control Panel",
                               font=("Arial", 22))
dashboard_title.pack(pady=20)

button_frame = ctk.CTkFrame(dashboard_frame)
button_frame.pack(pady=10)

gesture_btn = ctk.CTkButton(button_frame,
                            text="🖐 Start Gesture",
                            width=200,
                            command=start_gesture)
gesture_btn.grid(row=0, column=0, padx=10, pady=10)

voice_btn = ctk.CTkButton(button_frame,
                          text="🎤 Start Voice",
                          width=200,
                          command=start_voice)
voice_btn.grid(row=0, column=1, padx=10, pady=10)

combined_btn = ctk.CTkButton(button_frame,
                             text="🔄 Start Combined",
                             width=200,
                             command=start_combined)
combined_btn.grid(row=1, column=0, padx=10, pady=10)

stop_btn = ctk.CTkButton(button_frame,
                         text="⛔ Stop All",
                         fg_color="red",
                         hover_color="#aa0000",
                         width=200,
                         command=stop_all)
stop_btn.grid(row=1, column=1, padx=10, pady=10)

# ---------------- LOG AREA ----------------
log_label = ctk.CTkLabel(dashboard_frame,
                         text="Live Console",
                         font=("Arial", 18))
log_label.pack(pady=10)

log_text = ctk.CTkTextbox(dashboard_frame,
                          width=650,
                          height=250)
log_text.pack(pady=10)

# Redirect print() to GUI
sys.stdout = Redirect(log_text)

# ---------------- RUN APP ----------------
app.mainloop()
