import tkinter as tk
import os

class Manager:
    def __init__(self, image_directory=None, label_file=None) -> None:
        self.image_paths = []
        self.image_count = 0
        self.possible_labels = []
        if image_directory:
            self.load_images(image_directory)

        if label_file:
            self.load_labels(label_file)
         
    def load_images(self, image_directory):
        for filename in os.listdir(image_directory):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                image_path = os.path.join(image_directory, filename)
                self.image_paths.append(image_path)
        self.image_count = len(self.image_paths)

    def load_labels(self, label_file):
        with open(label_file) as f:
            self.possible_labels =  [l.strip() for l in f.readlines()]
    
    