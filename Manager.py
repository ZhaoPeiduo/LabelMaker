import tkinter as tk
import os
import sys

class Manager:
    def __init__(self) -> None:
        self.image_paths = []
        self.image_count = 0
        self.possible_labels = []
        self.label_counters = []
        self.archive_counter = tk.IntVar(value=0)
        self.index = 0
        self.labels = []
         
    def load_images(self, image_directory):
        for filename in os.listdir(image_directory):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                if sys.platform.startswith("win"):
                    image_path = image_directory + "/" + filename
                else:
                    image_path = os.path.join(image_directory, filename)
                self.image_paths.append(image_path)
        self.image_count = len(self.image_paths)

    def load_labels(self, label_file):
        with open(label_file) as f:
            self.possible_labels =  [l.strip() for l in f.readlines()]
    
    def save_labels(self, save_file):
        for image_path, label in zip(self.image_paths, self.labels):
            image_path = os.path.relpath(image_path)
            if sys.platform.startswith('win'):
                image_path = image_path.replace('\\', '/')
            save_file.write(f"{image_path},{label}\n")
        print(f"Labels saved to {save_file.name}")        

    def reset_images(self):
        self.image_paths = []
        self.image_count = 0
        self.index = 0
        for counter in self.label_counters:
            counter.set(0)
    