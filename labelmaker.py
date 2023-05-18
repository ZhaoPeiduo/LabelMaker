import tkinter as tk
import os
from Manager import Manager
import argparse
from FrameWidgets import FrameWidgets

class DataLabeler:
    def __init__(self, image_directory, labels_file, output):
        self.window = tk.Tk()
        self.window.title("Manual Data Labeler")

        self.manager = Manager(image_directory, labels_file)
        self.frame_widgets = FrameWidgets(self.window, self.manager)

        self.message =  f"{self.manager.image_count - self.manager.index} images remaining"
        self.message_frame = tk.Label(self.window, textvariable=self.message)
        self.message_frame.pack()
    
    def increment_y(self, counter: tk.IntVar):
        counter.set(counter.get() + 1)

    def assign_label(self, index):
        self.manager.labels.append(self.manager.possible_labels[index])
        self.increment_y(self.manager.counters[index])
        self.manager.index += 1
        if self.manager.index < self.manager.image_count:
            self.frame_widgets.display_data(self.manager.image_paths[self.manager.index])
        else:
            self.frame_widgets.save_labels()

    def run(self):
        self.frame_widgets.read_images()
        self.frame_widgets.read_labels()
        self.frame_widgets.initialize_buttons(self.assign_label)
        self.window.mainloop()

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--image_directory", 
        "-imdir", 
        help="Input image directory",
    )

    parser.add_argument(
        "--labels", 
        "-l", 
        help="Class labels in .txt / .csv format, one line per label",
    )

    parser.add_argument(
        "--output", 
        "-o", 
        help="Output file name", 
    )

    args = parser.parse_args()

    labeler = DataLabeler(args.image_directory, args.labels, args.output)
    labeler.run()

if __name__ == "__main__":
    main()


