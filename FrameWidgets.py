import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
from Manager import Manager
import os

class FrameWidgets:
    KEYMAP = {chr(i): i - 48 if i < 58 else i - 55 if i < 91 else i - 61 for i in range(48, 91)}
    def __init__(self, window, manager: Manager) -> None:
        self.window = window
        self.manager = manager

        self.control_frame = tk.Frame(self.window)
        self.control_frame.pack()

        self.read_images_button = tk.Button(self.control_frame, text="Load Folder", command=self.read_images)
        self.read_images_button.pack(side=tk.LEFT, padx=5)

        self.save_labels_button = tk.Button(self.control_frame, text="Save Labels", command=self.save_labels)
        self.save_labels_button.pack(side=tk.LEFT, padx=5)

        self.undo_button = tk.Button(self.control_frame, text="Undo", command=self.undo)
        self.window.bind("u", lambda event: self.undo_button.invoke())
        self.undo_button.pack(side=tk.LEFT, padx=5)

        self.exit_button = tk.Button(self.control_frame, text="Exit", command=self.exit)
        self.window.bind("<Escape>", lambda event: self.exit_button.invoke())
        self.exit_button.pack(side=tk.LEFT, padx=5)

        self.image_label = tk.Label(self.window)
        self.image_label.pack()

        self.button_frame = tk.Frame(self.window)
        self.button_frame.pack()

        self.count_frame = tk.Frame(self.window)
        self.count_frame.pack()

        self.message = f"{self.manager.image_count - self.manager.index} images remaining"
        self.message_frame = tk.Label(self.window, textvariable=self.message)
        self.message_frame.pack()

    def initialize_buttons(self, assign_label_func):
        self.button_frame.pack_forget()
        for index, label in enumerate(self.manager.possible_labels):
            button = tk.Button(self.button_frame, text=label, command=lambda idx=index:assign_label_func(idx))
            self.window.bind(str(self.KEYMAP[str(index + 1)]), lambda event, btn=button: btn.invoke())
            button.pack(side=tk.LEFT, padx=5) 
            counter = tk.IntVar(value=0)
            label = tk.Label(self.count_frame, textvariable=counter)  
            label.pack(side=tk.LEFT, padx=10)
            self.manager.counters.append(counter) 
        self.button_frame.pack(side=tk.BOTTOM)

    def read_images(self):
        image_directory = filedialog.askdirectory()
        self.manager.reset_images()
        self.manager.load_images(image_directory)

        if self.manager.image_count > 0:
            self.display_data(self.manager.image_paths[self.manager.index])
        else:
            print("No images found in the specified directory.")

    def read_labels(self):
        label_file = filedialog.askopenfilename()
        self.manager.load_labels(label_file)
 
    def save_labels(self):
        save_file = filedialog.asksaveasfile()
        self.manager.save_labels(save_file)

    def exit(self):
        self.window.destroy()

    def display_data(self, image_path):
        image = Image.open(image_path)
        image = image.resize((400, 300))
        tk_image = ImageTk.PhotoImage(image)
        self.image_label.configure(image=tk_image)
        self.image_label.image = tk_image

    def undo(self):
        self.manager.index -= 1
        decrement = self.manager.possible_labels.index(self.manager.labels.pop(-1))
        self.manager.counters[decrement].set(self.manager.counters[decrement].get() - 1)
        self.display_data(self.manager.image_paths[self.manager.index])
   