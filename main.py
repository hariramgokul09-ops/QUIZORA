from home import HomeScreen
import tkinter as tk
WIDTH, HEIGHT = 850, 550
root = tk.Tk()
root.title("QUIZORA")

# Set size and center on screen
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
x = (screen_w - WIDTH) // 2
y = (screen_h - HEIGHT) // 2
root.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")

    
root.resizable(False, False)

if __name__ == "__main__":
    HomeScreen(root)
