import tkinter as tk
from PIL import Image, ImageTk
from content_handler import *


class App:
    def __init__(self, master, app_size=(350, 300), arrow_size=(40, 40), max_words=50):
        self.master = master

        BG_COLOR = "#e8f1fd"
        FRONT_COLOR = "#84d9ba"
        BACK_COLOR = "#3c7363"
        FRONT_TEXT_COLOR = "#303030"
        BACK_TEXT_COLOR = "#b8d9d0"

        self.front_color = FRONT_COLOR
        self.back_color = BACK_COLOR
        self.front_text_color = FRONT_TEXT_COLOR
        self.back_text_color = BACK_TEXT_COLOR

        master.title('FlashCard')
        master.resizable(False, False)
        master.config(bg=BG_COLOR)

        self.current_card_index = tk.IntVar()
        self.max_words = max_words
        self.app_size = app_size
        self.flashcard_size = (app_size[0]-100, app_size[1]-50)

        x_app_coord = master.winfo_screenwidth() - app_size[0] - 100
        y_app_coord = master.winfo_screenheight() - app_size[1] - 100
        master.geometry(f'{app_size[0]}x{app_size[1]}+{x_app_coord}+{y_app_coord}')

        # Initialize elements
        # Menu
        self.app_name = tk.Label(
            master, text="FLASHCARD", 
            font=('Bahnschrift Bold Condensed', 45), 
            fg=self.back_color, 
            bg=BG_COLOR
        )

        self.local_button = tk.Label(
            master, 
            text="Local\n(Press F1)", 
            font=('Bahnschrift SemiBold', 14), 
            fg=self.back_text_color, 
            bg=self.back_color
        )
        self.local_button.bind("<Button-1>", lambda event: self.load(event, "local"))
        self.local_button.bind("<Enter>", lambda event: event.widget.config(cursor="hand2"))
        self.local_button.bind("<Leave>", lambda event: event.widget.config(cursor=""))

        self.online_button = tk.Label(
            master, 
            text="Online\n(Press F2)", 
            font=('Bahnschrift SemiBold', 14), 
            fg=self.back_text_color, 
            bg=self.back_color
        )
        self.online_button.bind("<Button-1>", lambda event: self.load(event, "online"))
        self.online_button.bind("<Enter>", lambda event: event.widget.config(cursor="hand2"))
        self.online_button.bind("<Leave>", lambda event: event.widget.config(cursor=""))

        # Main page
        self.counter = tk.Label(
            master, 
            font=('Bahnschrift SemiBold Condensed', 12), 
            bg=BG_COLOR
        )

        self.back_to_menu_frame = tk.Frame(master, bg=BG_COLOR)
        back_to_menu_img = ImageTk.PhotoImage(
            Image.open('assets/back.png').resize((18, 18), Image.BICUBIC)
        )
        self.back_to_menu_img = tk.Label(
            self.back_to_menu_frame, image=back_to_menu_img, bg=BG_COLOR
        )
        self.back_to_menu_img.image = back_to_menu_img
        self.back_to_menu_label = tk.Label(
            self.back_to_menu_frame, 
            text="Back to Menu", 
            font=('Bahnschrift SemiBold Condensed', 12), 
            bg=BG_COLOR
        )
        self.back_to_menu_img.bind("<Button-1>", lambda event: self.back())
        self.back_to_menu_label.bind("<Button-1>", lambda event: self.back())
        self.back_to_menu_frame.bind("<Button-1>", lambda event: self.back())

        self.back_to_menu_frame.bind("<Enter>", lambda event: event.widget.config(cursor="hand2"))
        self.back_to_menu_frame.bind("<Leave>", lambda event: event.widget.config(cursor=""))
        self.back_to_menu_label.bind("<Enter>", lambda event: event.widget.config(cursor="hand2"))
        self.back_to_menu_label.bind("<Leave>", lambda event: event.widget.config(cursor=""))
        self.back_to_menu_img.bind("<Enter>", lambda event: event.widget.config(cursor="hand2"))
        self.back_to_menu_img.bind("<Leave>", lambda event: event.widget.config(cursor=""))

        self.prev_arrow_img = ImageTk.PhotoImage(
            Image.open('assets/left.png').resize(arrow_size, Image.BICUBIC)
        )
        self.prev_button = tk.Label(master, image=self.prev_arrow_img, bg=BG_COLOR)
        self.prev_button.bind("<Button-1>", self.prev_flashcard)
        self.prev_button.bind(
            "<Enter>", 
            lambda event: event.widget.config(cursor="hand2") \
                if self.has_prev_flashcard() else event.widget.config(cursor="")
        )
        self.prev_button.bind("<Leave>", lambda event: event.widget.config(cursor=""))

        self.next_arrow_img = ImageTk.PhotoImage(
            Image.open('assets/right.png').resize(arrow_size, Image.BICUBIC))
        self.next_button = tk.Label(master, image=self.next_arrow_img, bg=BG_COLOR)
        self.next_button.bind('<Button-1>', self.next_flashcard)
        self.next_button.bind(
            "<Enter>", 
            lambda event: event.widget.config(cursor="hand2") \
                if self.has_next_flashcard() else event.widget.config(cursor="")
        )
        self.next_button.bind("<Leave>", lambda event: event.widget.config(cursor=""))

        self.flashcard_frame = tk.Frame(master, bd=2, bg=BG_COLOR)
        self.flashcard_label = tk.Label(
            self.flashcard_frame, 
            wraplength=app_size[0]-150, 
            justify=tk.LEFT, 
            font=('Bahnschrift SemiCondensed', 16), 
            bg=BG_COLOR
        )

        self.flashcard_label.bind('<Button-1>', self.swap_flashcard)
        self.flashcard_frame.bind('<Button-1>', self.swap_flashcard)
        self.flashcard_label.bind("<Enter>", lambda event: event.widget.config(cursor="hand2"))
        self.flashcard_label.bind("<Leave>", lambda event: event.widget.config(cursor=""))
        self.flashcard_frame.bind("<Enter>", lambda event: event.widget.config(cursor="hand2"))
        self.flashcard_frame.bind("<Leave>", lambda event: event.widget.config(cursor=""))

        master.bind('<Escape>', lambda event: master.destroy())

        self.place_menu()

    def place_menu(self):
        self.flashcard_frame.place_forget()
        self.next_button.place_forget()
        self.prev_button.place_forget()
        self.back_to_menu_frame.place_forget()
        self.counter.place_forget()

        self.app_name.place(relx=0.5, rely=0.45, anchor='center')
        self.local_button.place(
            relx=0.25, rely=0.85, anchor='center', relheight=0.2, relwidth=0.4
        )
        self.online_button.place(
            relx=0.75, rely=0.85, anchor='center', relheight=0.2, relwidth=0.4
        )

        self.master.bind('<F1>', lambda event: self.load(event, "local"))
        self.master.bind('<F2>', lambda event: self.load(event, "online"))
        self.master.unbind('<Left>')
        self.master.unbind('<Right>')
        self.master.unbind("<Return>")
        self.master.unbind("<space>")
        self.master.unbind("<BackSpace>")

    def place_content(self):
        self.app_name.place_forget()
        self.local_button.place_forget()
        self.online_button.place_forget()

        self.flashcard_frame.place(
            relx=0.5, rely=0.95, width=self.flashcard_size[0], height=self.flashcard_size[1], anchor='s'
        )
        self.flashcard_label.place(relx=0.5, rely=0.5, anchor='center')

        self.next_button.place(
            relx=1-25/self.app_size[0], rely=0.52, anchor='center'
        )
        self.prev_button.place(
            relx=25/self.app_size[0], rely=0.52, anchor='center'
        )

        self.back_to_menu_img.pack(side=tk.LEFT)
        self.back_to_menu_label.pack(side=tk.LEFT)
        self.back_to_menu_frame.place(relx=0.99, rely=0.01, anchor='ne')

        self.counter.place(relx=0.01, rely=0.01, anchor='nw')

        self.master.bind('<Left>', lambda event: self.prev_flashcard(event))
        self.master.bind('<Right>', lambda event: self.next_flashcard(event))
        self.master.bind("<Return>", lambda event: self.swap_flashcard(event))
        self.master.bind("<space>", lambda event: self.swap_flashcard(event))
        self.master.bind("<BackSpace>", lambda event: self.back())
        self.master.unbind('<F1>')
        self.master.unbind('<F2>')
        self.master.unbind('<F12>')

    def load(self, event, kind):
        event.widget.config(cursor="wait")

        self.place_content()
        contents = handle_content(get_content(kind))
        self.flashcards = nlp_handle_content(contents, self.max_words - 1)
        self.flashcard_label.config(
            text=self.flashcards[self.current_card_index.get()][2]
        )
        self.format_front()

        self.current_card_index.trace_add("write", self.update_arrow_state)
        self.current_card_index.trace_add("write", self.update_counter)
        self.current_card_index.set(0)

        event.widget.config(cursor="")

    def back(self, event=None):
        self.place_menu()
        self.current_card_index.set(0)

    def swap_flashcard(self, event):
        if self.flashcard_label['text'] == self.flashcards[self.current_card_index.get()][2]:
            self.format_back()
        else:
            self.format_front()

    def update_counter(self, *args):
        self.counter.config(
            text=f"{self.current_card_index.get() + 1}/{len(self.flashcards)}"
        )

    def update_arrow_state(self, *args):
        if not self.has_prev_flashcard():
            self.prev_button.config(state=tk.DISABLED)
            self.next_button.config(state=tk.NORMAL)
        elif not self.has_next_flashcard():
            self.prev_button.config(state=tk.NORMAL)
            self.next_button.config(state=tk.DISABLED)
        else:
            self.prev_button.config(state=tk.NORMAL)
            self.next_button.config(state=tk.NORMAL)

    def prev_flashcard(self, event):
        if self.has_prev_flashcard():
            self.current_card_index.set(self.current_card_index.get()-1)
            self.flashcard_label.config(
                text=self.flashcards[self.current_card_index.get()][2]
            )
            self.format_front()

    def next_flashcard(self, event):
        if self.has_next_flashcard():
            self.current_card_index.set(self.current_card_index.get()+1)
            self.flashcard_label.config(
                text=self.flashcards[self.current_card_index.get()][2]
            )
            self.format_front()

    def has_prev_flashcard(self):
        return self.current_card_index.get() > 0

    def has_next_flashcard(self):
        return self.current_card_index.get() < len(self.flashcards) - 1

    def format_front(self):
        self.flashcard_label.config(
            text=self.flashcards[self.current_card_index.get()][2],
            bg=self.front_color,
            fg=self.front_text_color
        )
        self.flashcard_frame.config(bg=self.front_color)

    def format_back(self):
        self.flashcard_label.config(
            text=self.flashcards[self.current_card_index.get()][1],
            bg=self.back_color,
            fg=self.back_text_color
        )
        self.flashcard_frame.config(bg=self.back_color)
