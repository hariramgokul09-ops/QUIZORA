import tkinter as tk
from Select_subject import Select_Subject
from PIL import Image, ImageTk
from textToSpeech import speak
import threading
import os

# Try importing playsound3 safely
try:
    import playsound3
except ImportError:
    playsound3 = None


def play_sound(path: str):
    """Play click sound asynchronously if available."""
    if not playsound3:
        print("⚠️ playsound3 not installed — skipping sound.")
        return
    if not os.path.exists(path):
        print(f"⚠️ Sound file not found: {path}")
        return

    # Call the playsound function inside the module
    threading.Thread(target=lambda: playsound3.playsound(path), daemon=True).start()


def HomeScreen(root):
    # clear previous widgets
    for widget in root.winfo_children():
        widget.destroy()

    def move_to_nextScreen():
        play_sound('./Assets/click.mp3')
        speak("Starting quiz")
        Select_Subject(root)

    # load background
    bg_path = "./Assets/Homebg.jpeg"
    if os.path.exists(bg_path):
        bg_image = Image.open(bg_path).resize((850, 550))
        bg_photo = ImageTk.PhotoImage(bg_image)
        canvas = tk.Canvas(root, width=850, height=550, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=bg_photo, anchor="nw")
        canvas.image = bg_photo  # prevent garbage collection
    else:
        root.configure(bg="#202020")

    # quiz button
    quiz_button = tk.Button(
        root,
        text="Quiz",
        font=("Segoe UI", 16, "bold"),
        bg="#F71616",
        fg="white",
        activebackground="#F71616",
        activeforeground="white",
        relief="flat",
        width=12,
        height=2,
        command=move_to_nextScreen,
        bd=3
    )
    quiz_button.place(x=45, y=360)

    root.mainloop()