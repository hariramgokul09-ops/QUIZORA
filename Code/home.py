import tkinter as tk
from Select_subject import Select_Subject
from PIL import Image, ImageTk

def HomeScreen(root):
    for widget in root.winfo_children():
        widget.destroy()
        
    def move_to_nextScreen():
        Select_Subject(root)
        
    bg_image = Image.open("./Assets/Homebg.jpeg")   # Replace with your actual image file
    bg_image = bg_image.resize((850, 550))
    bg_photo = ImageTk.PhotoImage(bg_image)
    
    canvas = tk.Canvas(root, width=850, height=550, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    quiz_button = tk.Button(
        root,
        text="Quiz",
        font=("Segoe UI", 16, "bold"),
        bg="#F71616",      # Button background color
        fg="white",        # Text color
        activebackground="#1AD409",  # Color when pressed
        activeforeground="white",
        relief="flat",     # Removes 3D border
        width=12,
        height=2,
        command=move_to_nextScreen,
        bd=3
        
        
    )
    quiz_button.place(x=45, y=360)
    
    root.mainloop()