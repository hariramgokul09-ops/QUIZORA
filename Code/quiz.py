import tkinter as tk
from tkinter import messagebox
import serial
import threading
import time
import random
quiz_
def start_quiz(root):
    print("in quiz.py")
    # Clear previous widgets (from Select_Subject or connection screen)
    for widget in root.winfo_children():
        widget.destroy()

    # ------------------ SETUP SERIAL ------------------
    try:
        arduino = serial.Serial('COM13', 9600, timeout=1)
        time.sleep(2)
        print("✅ Arduino connected.")
    except:
        arduino = None
        print("⚠️ Arduino not connected — demo mode enabled.")



    # ------------------ VARIABLES ------------------
    question_index = 0
    answered = False

    # ------------------ UI SETUP ------------------
    WIDTH, HEIGHT = 750, 550
    root.title("Fun Quiz - Biology")

    question_label = tk.Label(root, text="", font=("Arial", 20, "bold"),
                              wraplength=600, justify="center")
    question_label.pack(pady=40)

    option_labels = []
    for i in range(4):
        lbl = tk.Label(root, text="", font=("Arial", 16),
                       width=35, relief="ridge", pady=10)
        lbl.pack(pady=5)
        option_labels.append(lbl)

    feedback_label = tk.Label(root, text="", font=("Arial", 16, "italic"))
    feedback_label.pack(pady=30)

    # ------------------ LOGIC FUNCTIONS ------------------
    def display_question():
        """Display the current question and options"""
        nonlocal answered
        answered = False
        feedback_label.config(text="")
        q, opts, _, _ = quiz_data[question_index]
        question_label.config(text=f"Q{question_index + 1}. {q}")
        for i in range(4):
            option_labels[i].config(text=f"{i+1}. {opts[i]}", bg="SystemButtonFace")

    def check_answer(option_num):
        """Check selected answer"""
        nonlocal answered
        if answered:
            return
        correct = quiz_data[question_index][2]
        explanation = quiz_data[question_index][3]
        if option_num == correct:
            feedback_label.config(text="✅ Correct!", fg="green")
            option_labels[option_num - 1].config(bg="lightgreen")
        else:
            feedback_label.config(text=f"❌ Wrong! {explanation}", fg="red")
            option_labels[option_num - 1].config(bg="tomato")
            option_labels[correct - 1].config(bg="lightgreen")
        answered = True

    def next_question():
        """Go to the next question"""
        nonlocal question_index, answered
        if not answered:
            feedback_label.config(text="⚠️ Choose an option first!", fg="orange")
            return
        question_index += 1
        if question_index < len(quiz_data):
            display_question()
        else:
            messagebox.showinfo("Quiz Complete", "🎉 You’ve finished the quiz!")
            root.destroy()

    # ------------------ SERIAL LISTENER ------------------
    def listen_serial():
        while True:
            if arduino:
                try:
                    data = arduino.readline().decode().strip()
                    if data in ['1', '2', '3', '4']:
                        root.after(0, check_answer, int(data))
                    elif data == '5':
                        root.after(0, next_question)
                except:
                    pass
            time.sleep(0.1)

    # ------------------ START QUIZ ------------------
    threading.Thread(target=listen_serial, daemon=True).start()
    display_question()

def finalquizset():
    quiz_data = [
    [
        "Which of the following is a living thing?",
        ["Chair", "Cat", "Stone", "Toy"],
        2,
        [cite_start]"Living things can move, grow, and need food — a cat does all these. [cite: 8]"
    ],
    [
        "Which of these can grow?",
        ["Rock", "Car", "Plant", "Table"],
        3,
        [cite_start]"Plants are living; they grow by making their own food through photosynthesis. [cite: 15]"
    ],
    [
        "All living things need _______ to live.",
        ["Food", "Toys", "Air freshener", "None"],
        1,
        [cite_start]"Food gives energy for growth and activities. [cite: 22]"
    ],
    [
        "Which of these can breathe?",
        ["Fish", "Stone", "Pencil", "Fan"],
        1,
        [cite_start]"Fish breathe through gills to take in oxygen from water. [cite: 29]"
    ],
    [
        "Which one is non-living?",
        ["Bird", "Dog", "River", "Tree"],
        3,
        [cite_start]"A river moves, but it doesn’t grow or reproduce — it’s non-living. [cite: 36]"
    ],
    [
        "Living things can reproduce. Which of these can?",
        ["Hen", "Bag", "Clock", "Shoes"],
        1,
        [cite_start]"Hens lay eggs — they reproduce. [cite: 43]"
    ],
    [
        "Plants breathe through which part?",
        ["Roots", "Stem", "Leaves", "Flowers"],
        3,
        [cite_start]"Tiny pores on leaves called stomata help plants breathe. [cite: 50]"
    ],
    [
        "Living things respond to _______.",
        ["Light and sound", "Nothing", "Plastic", "Dust"],
        1,
        [cite_start]"Living things react to changes in surroundings, like light or temperature. [cite: 57]"
    ],
    [
        "Which of these grows from a seed?",
        ["Stone", "Plant", "Toy car", "Glass"],
        2,
        [cite_start]"Seeds grow into plants — a living process. [cite: 64]"
    ],
    [
        "Humans breathe using _______.",
        ["Gills", "Lungs", "Skin", "Stomata"],
        2,
        [cite_start]"Humans use lungs to exchange oxygen and carbon dioxide. [cite: 71]"
    ],
    [
        "Which of the following can make its own food?",
        ["Dog", "Human", "Plant", "Fish"],
        3,
        [cite_start]"Plants prepare food using sunlight (photosynthesis). [cite: 78]"
    ],
    [
        "Non-living things do not show which feature?",
        ["Breathing", "Shining", "Melting", "Breaking"],
        1,
        [cite_start]"Only living things breathe and exchange gases. [cite: 85]"
    ],
    [
        "A baby grows into an adult. This shows _______.",
        ["Growth", "Movement", "Rest", "Non-living"],
        1,
        [cite_start]"Increase in size or body parts shows growth — a living feature. [cite: 92]"
    ],
    [
        "Which of these moves on its own?",
        ["Table", "Ball", "Rabbit", "Fan"],
        3,
        [cite_start]"Living things can move on their own; non-living things need force. [cite: 99]"
    ],
    [
        "Which of these can feel pain?",
        ["Tree", "Human", "Stone", "Robot"],
        2,
        [cite_start]"Humans have sense organs and nerves to feel. [cite: 106]"
    ],
    [
        "Which is common in all living things?",
        ["Need water", "Made of metal", "Don’t breathe", "Never die"],
        1,
        [cite_start]"Water is essential for all living organisms to survive. [cite: 113]"
    ],
    [
        "Which is an example of a non-living thing found in nature?",
        ["Mountain", "Deer", "Bird", "Tree"],
        1,
        [cite_start]"Mountains are part of nature but not living. [cite: 120]"
    ],
    [
        "What happens to living things after death?",
        ["They start breathing again", "They decompose", "They turn into toys", "They grow faster"],
        2,
        [cite_start]"Dead organisms break down and return nutrients to the soil. [cite: 127]"
    ],
    [
        "What helps animals to reproduce?",
        ["Machines", "Their body systems", "Humans", "Wind"],
        2,
        [cite_start]"Animals have reproductive organs to produce offspring. [cite: 134]"
    ],
    [
        "Which of these can die?",
        ["Leaf", "Pencil", "Bag", "Table"],
        1,
        [cite_start]"A leaf is part of a plant — it’s living and can die when dry or detached. [cite: 141]"
    ]
]
    
    for i in range(10):
        a=random.randint(0,len(quiz_data)-1)
        