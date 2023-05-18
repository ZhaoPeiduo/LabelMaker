import tkinter as tk
import os
from Manager import Manager
import argparse
from LabelFrames import SettingFrame, ImageDisplayFrame, LabelButtonFrame

class DataLabeler:
    def __init__(self, image_directory, labels_file, output):
        self.window = tk.Tk()
        self.window.title("Manual Data Labeler")

        self.manager = Manager(image_directory, labels_file)
        self.setting_frame = SettingFrame(self.window, self.manager)
        self.image_display_frame = ImageDisplayFrame(self.window, self.manager)
        self.label_button_frame = LabelButtonFrame(self.window, self.manager)

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
            self.image_display_frame.display_data(self.manager.image_paths[self.manager.index])
        else:
            self.setting_frame.save_labels()

    def run(self):
        self.setting_frame.read_images()
        self.setting_frame.read_labels()
        self.label_button_frame.initialize_buttons(self.assign_label)
        if self.manager.image_count > 0:
            self.image_display_frame.display_data(self.manager.image_paths[self.manager.index])
        else:
            print("No images found in the specified directory.")
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


