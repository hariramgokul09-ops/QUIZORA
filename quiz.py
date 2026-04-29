import tkinter as tk
import random
import threading
import time
import os
from PIL import Image, ImageTk
from textToSpeech import speak  # Your TTS function
from test import getquestions  # Your question source

# ---------- SOUND FUNCTION ----------
try:
    import playsound3
except ImportError:
    playsound3 = None

def play_sound(path: str):
    """Play a sound file asynchronously if available."""
    if not playsound3:
        print("⚠️ playsound3 not installed — skipping sound.")
        return
    if not os.path.exists(path):
        print(f"⚠️ Sound file not found: {path}")
        return
    threading.Thread(target=lambda: playsound3.playsound(path), daemon=True).start()


# ---------- QUIZ FUNCTION ----------
def start_quiz(root, subject, chapter):
    quiz_data = finalquizset(subject, chapter)
    answers = []

    # Clear previous widgets
    for widget in root.winfo_children():
        widget.destroy()

    WIDTH, HEIGHT = 850, 550

    # ---------- BACKGROUND ----------
    bg_path = "./Assets/quiz.png"
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#1e1e1e", highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    if os.path.exists(bg_path):
        bg_image = Image.open(bg_path).resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        canvas.create_image(0, 0, image=bg_photo, anchor="nw")
        canvas.bg_photo = bg_photo  # prevent garbage collection

    # ---------- CANVAS TEXT ----------
    question_text = canvas.create_text(WIDTH//2, 80, text="", font=("Arial", 20, "bold"),
                                       fill="white", width=600, justify="center")
    feedback_text = canvas.create_text(WIDTH//2, 420, text="", font=("Arial", 16, "italic"),
                                       fill="white", width=600)

    # ---------- OPTION RECTANGLES ----------
    option_items = []
    for i in range(4):
        rect = canvas.create_rectangle(WIDTH//2 - 180, 140 + i*60, WIDTH//2 + 180, 180 + i*60,
                                       fill="", outline="white", width=2)
        txt = canvas.create_text(WIDTH//2, 160 + i*60, text="", font=("Arial", 16),
                                 fill="white", width=600)
        option_items.append((rect, txt))

    question_index = 0
    answered = False
    score = 0

    # ---------- LOGIC FUNCTIONS ----------
    def display_question():
        nonlocal answered
        answered = False
        canvas.itemconfig(feedback_text, text="")
        q, opts, correct, explanation, difficulty = quiz_data[question_index]

        canvas.itemconfig(question_text, text=f"Q{question_index + 1}. {q}")

        for i in range(4):
            rect, txt = option_items[i]
            canvas.itemconfig(txt, text=f" {opts[i]}")
            canvas.itemconfig(rect, fill="", outline="white")

        speak(q)

    def check_answer(option_num):
        nonlocal answered, score
        if answered:
            return

        correct = quiz_data[question_index][2]
        explanation = quiz_data[question_index][3]
        difficulty = quiz_data[question_index][4]

        for i, (rect, _) in enumerate(option_items):
            if i == correct - 1:
                canvas.itemconfig(rect, fill="green")
            elif i == option_num - 1 and option_num != correct:
                canvas.itemconfig(rect, fill="red")
            else:
                canvas.itemconfig(rect, fill="")

        if option_num == correct:
            canvas.itemconfig(feedback_text, text="✅ Correct!", fill="green")
            score += 1
            difficulty_correct[difficulty] += 1
            answers.append(("Correct", quiz_data[question_index][0], difficulty))
            # --- Play correct sound ---
            play_sound('./Assets/correct.mp3')
        else:
            canvas.itemconfig(feedback_text, text=f"❌ Wrong! {explanation}", fill="red")
            answers.append(("Wrong", quiz_data[question_index][0], difficulty))
            # --- Play wrong sound ---
            play_sound('./Assets/wrong.mp3')

        answered = True
    def next_question():
        nonlocal question_index, answered
        if not answered:
            canvas.itemconfig(feedback_text, text="⚠️ Choose an option first!", fill="orange")
            return

        question_index += 1
        if question_index < len(quiz_data):
            display_question()
        else:
            show_report()

    # ---------- OPTION BUTTONS ----------
    for i in range(4):
        rect, _ = option_items[i]
        canvas.tag_bind(rect, "<Button-1>", lambda e, n=i+1: check_answer(n))
        canvas.tag_bind(option_items[i][1], "<Button-1>", lambda e, n=i+1: check_answer(n))

    # ---------- NEXT BUTTON ----------
    next_btn = tk.Button(root, text="Next", font=("Arial", 14, "bold"),
                         bg="lightblue", command=next_question)
    canvas.create_window(WIDTH//2, 500, window=next_btn)

    # ---------- REPORT ----------
    def show_report():
        canvas.delete("all")
        if os.path.exists(bg_path):
            canvas.create_image(0, 0, image=bg_photo, anchor="nw")

        correct = score
        wrong = len(quiz_data) - score
        percentage = (correct / len(quiz_data)) * 100
        summary = "Excellent! 🌟" if percentage >= 80 else "Good Job! 👍" if percentage >= 50 else "Keep Practicing! 💪"

        canvas.create_text(WIDTH//2, 60, text="📊 Quiz Report", font=("Arial", 24, "bold"), fill="white")
        canvas.create_text(WIDTH//2, 120, text=f"Total Questions: {len(quiz_data)}", font=("Arial", 16), fill="white")
        canvas.create_text(WIDTH//2, 160, text=f"Correct Answers: {correct}", font=("Arial", 16), fill="green")
        canvas.create_text(WIDTH//2, 200, text=f"Wrong Answers: {wrong}", font=("Arial", 16), fill="red")
        canvas.create_text(WIDTH//2, 240, text=f"Final Score: {percentage:.1f}%", font=("Arial", 16, "bold"), fill="white")
        canvas.create_text(WIDTH//2, 280, text=summary, font=("Arial", 18, "italic"), fill="white")

def finalquizset(subject, chapter):
    questions = getquestions(subject, chapter)
    selected = []
    for _ in range(min(3, len(questions))):
        idx = random.randint(0, len(questions) - 1)
        selected.append(questions.pop(idx))
    return selected