import tkinter as tk
from checkConnection import go_to_next_screen

def Select_Subject(root):
    # Clear all previous widgets
    for widget in root.winfo_children():
        widget.destroy()
        
    def next():
        go_to_next_screen(root)

    # --- Select Subject Section ---
    subject_label = tk.Label(root, text="Select Subject", font=("Arial", 16))
    subject_label.pack(pady=(30, 10))

    subject_var = tk.StringVar(value="Select Subject")
    chapter_var = tk.StringVar(value="Select Chapter Name")

    # --- Widgets for later use ---
    chapter_label = tk.Label(root, text="Select Chapter Name", font=("Arial", 16))
    chapter_dropdown = tk.OptionMenu(root, chapter_var, "")
    next_button = tk.Button(root, text="Next Screen", font=("Arial", 12), command=next)

    # Function called when subject changes
    def on_subject_selected(*args):
        selected_subject = subject_var.get()
        if selected_subject == "Biology":
            # Show chapter label and dropdown
            chapter_label.pack(pady=(30, 10))
            chapter_dropdown.pack(pady=5)

            # Clear old options and add the single easy chapter
            chapter_menu = chapter_dropdown["menu"]
            chapter_menu.delete(0, "end")

            chapter_name = "Living and Non-Living Things"
            chapter_menu.add_command(
                label=chapter_name,
                command=lambda: on_chapter_selected(chapter_name)
            )
        else:
            # Hide all if not valid subject
            chapter_label.pack_forget()
            chapter_dropdown.pack_forget()
            next_button.pack_forget()

    # Function called when chapter is selected
    def on_chapter_selected(chapter_name):
        chapter_var.set(chapter_name)
        # Now show Next Screen button
        next_button.pack(pady=30)

  
    

    # Subject dropdown
    subject_dropdown = tk.OptionMenu(root, subject_var, "Biology")
    subject_dropdown.config(width=20, font=("Arial", 12))
    subject_dropdown.pack(pady=5)

    # Update chapters when subject changes
    subject_var.trace("w", on_subject_selected)