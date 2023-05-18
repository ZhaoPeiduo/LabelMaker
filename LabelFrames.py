import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
import os

class SettingFrame:
    def __init__(self, window, image_directory) -> None:
        self.window = window
        self.image_directory = image_directory
        self.image_paths = []
        
        self.control_frame = tk.Frame(self.window)
        self.control_frame.pack()

        self.load_new_button = tk.Button(self.control_frame, text="Load Folder", command=self.load_folder)
        self.load_new_button.pack(side=tk.LEFT, padx=5)

        self.exit_button = tk.Button(self.control_frame, text="Exit", command=self.exit)
        self.window.bind("<Escape>", lambda event: self.exit_button.invoke())
        self.exit_button.pack(side=tk.LEFT, padx=5)
    
    def load_folder(self):
        self.image_directory = filedialog.askdirectory()
        for filename in os.listdir(self.image_directory):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                image_path = os.path.join(self.image_directory, filename)
                self.image_paths.append(image_path)
        self.image_count = len(self.image_paths)
    
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
