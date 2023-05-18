import tkinter as tk
import os
import sys

class Manager:
    def __init__(self, image_directory=None, label_file=None) -> None:
        self.image_paths = []
        self.image_count = 0
        self.possible_labels = []
        self.counters = []
        self.index = 0
        self.labels = []
        
        if image_directory:
            self.load_images(image_directory)

        if label_file:
            self.load_labels(label_file)
         
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
        # self.message = f"No more images to label.Labels saved to {self.output}."

    def reset_images(self):
        self.image_paths = []
        self.image_count = 0
        self.index = 0

    def reset_labels(self):
        self.possible_labels = []
        self.counters = []

    def reset_output(self):
        self.labels = []

    def reset_all(self):
        self.reset_images()
        self.reset_labels()
        self.reset_output()
    