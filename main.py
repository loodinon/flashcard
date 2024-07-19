import tkinter as tk
from app import App


if __name__ == "__main__":
    with open('setting.txt', 'r') as file:
        lines = file.readlines()
        w = int(lines[0].split(":")[1].strip())
        h = int(lines[1].split(":")[1].strip())
        a = int(lines[2].split(":")[1].strip())
        mw = int(lines[3].split(":")[1].strip())
    
    root = tk.Tk()
    app = App(root, app_size=(w, h), arrow_size=(a, a), max_words=mw)
    root.mainloop()
