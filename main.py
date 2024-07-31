import tkinter as tk
from app import App
from utils import read_setting


if __name__ == "__main__":
    mw, mode = read_setting()

    root = tk.Tk()
    app = App(root, max_words=mw, mode=mode)
    root.mainloop()
