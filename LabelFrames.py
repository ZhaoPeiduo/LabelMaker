import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
import os

class SettingFrame:
    def __init__(self, window, manager) -> None:
        self.window = window
        self.manager = manager

        self.control_frame = tk.Frame(self.window)
        self.control_frame.pack()

        self.read_new_button = tk.Button(self.control_frame, text="Load Folder", command=self.read_images)
        self.read_new_button.pack(side=tk.LEFT, padx=5)

        self.exit_button = tk.Button(self.control_frame, text="Exit", command=self.exit)
        self.window.bind("<Escape>", lambda event: self.exit_button.invoke())
        self.exit_button.pack(side=tk.LEFT, padx=5)
    
    def read_images(self):
        image_directory = filedialog.askdirectory()
        self.manager.load_images(image_directory)

    def read_labels(self):
        label_file = filedialog.askopenfilename().name
        self.manager.load_labels(label_file)


    def exit(self):
        self.window.destroy()


class ImageDisplayFrame:
    def __init__(self, window) -> None:
        self.image_label = tk.Label(self.window)
        self.image_label.pack()

    def display_data(self, image_path):
        image = Image.open(image_path)
        image = image.resize((400, 300))
        tk_image = ImageTk.PhotoImage(image)
        self.image_label.configure(image=tk_image)
        self.image_label.image = tk_image
