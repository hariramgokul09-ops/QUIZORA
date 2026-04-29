import tkinter as tk
from tkinter import messagebox
from checkConnection import go_to_next_screen
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
    """Play a click sound asynchronously if the file exists."""
    if not playsound3:
        print("⚠️ playsound3 not installed — skipping sound.")
        return
    if not os.path.exists(path):
        print(f"⚠️ Sound file not found: {path}")
        return

    threading.Thread(target=lambda: playsound3.playsound(path), daemon=True).start()


def Select_Subject(root):
    # Clear previous widgets
    for widget in root.winfo_children():
        widget.destroy()

    # --- Load background image ---
    bg_path = "./Assets/test.jpg"
    if os.path.exists(bg_path):
        bg_image = Image.open(bg_path).resize((850, 550))
        bg_photo = ImageTk.PhotoImage(bg_image)
        canvas = tk.Canvas(root, width=850, height=550, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=bg_photo, anchor="nw")
        canvas.bg_photo = bg_photo  # Prevent garbage collection
    else:
        root.configure(bg="#202020")
        canvas = tk.Canvas(root, width=850, height=550, highlightthickness=0, bg="#202020")
        canvas.pack(fill="both", expand=True)

    # --- Helper function to place widgets on top ---
    def place_widget(widget, x, y):
        canvas.create_window(x, y, window=widget)

    # --- Next screen handler ---
    def next_screen():
        play_sound('./Assets/click.mp3')
        subject = subject_entry.get().strip()
        chapter = chapter_entry.get().strip()

        if not subject or not chapter:
            messagebox.showwarning("Input Required", "Please enter both subject and chapter name.")
            speak("Please enter both subject and chapter name")
            return

        speak(f"Starting quiz for {subject}, chapter {chapter}")
        go_to_next_screen(root, subject, chapter)

    # --- Labels and Entry boxes ---
    tk.Label(root, text="Enter Subject:", font=("Arial", 14, "bold"), bg="#ffffff").place(x=250, y=70)
    subject_entry = tk.Entry(root, width=30, font=("Arial", 12))

    tk.Label(root, text="Enter Chapter:", font=("Arial", 14, "bold"), bg="#ffffff").place(x=250, y=180)
    chapter_entry = tk.Entry(root, width=30, font=("Arial", 12))

    next_button = tk.Button(
        root,
        text="Next Screen",
        font=("Arial", 12, "bold"),
        bg="#DC143C",
        fg="white",
        command=next_screen
    )

    # --- Place widgets ---
    place_widget(subject_entry, 425, 100)
    place_widget(chapter_entry, 425, 210)
    place_widget(next_button, 425, 270)