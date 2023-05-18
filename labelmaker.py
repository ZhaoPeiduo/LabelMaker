import tkinter as tk
import os
from Manager import Manager
from LabelFrames import SettingFrame, ImageDisplayFrame

class DataLabeler:
    def __init__(self, image_directory, labels_file, output, sep):
        self.output = output
        self.sep = sep
        self.keymap = {chr(i): i - 48 if i < 58 else i - 55 if i < 91 else i - 61 for i in range(48, 91)}

        self.index = 0
        self.labels = []

        self.window = tk.Tk()
        self.window.title("Manual Data Labeler")

        self.label_var = tk.StringVar()
        self.label_var.set("")

        self.setting_frame = SettingFrame(self.window)
        self.image_display_frame = ImageDisplayFrame(self.window)

        self.button_frame = tk.Frame(self.window)
        self.button_frame.pack()

        self.count_frame = tk.Frame(self.window)
        self.count_frame.pack()
        self.counters = []

        self.message =  f"{self.image_count - self.index} images remaining"
        self.message_frame = tk.Label(self.window, textvariable=self.message)
        self.message_frame.pack()

        for index, label in enumerate(self.possible_labels):
            button = tk.Button(self.button_frame, text=label, command=lambda idx=index:self.assign_label(idx))
            self.window.bind(str(self.keymap[str(index + 1)]), lambda event, btn=button: btn.invoke())
            button.pack(side=tk.LEFT, padx=5) 
            counter = tk.IntVar(value=0)
            label = tk.Label(self.count_frame, textvariable=counter)  
            label.pack(side=tk.LEFT, padx=10)
            self.counters.append(counter) 

    def load(self):
        self.reset_variables()
        self.run()

    def reset_variables(self):
        self.image_directory = self.setting_frame.load_folder()
        self.image_paths = []
        self.index = 0
        for counter in self.counters:
            counter.set(0)
    
    def increment_y(self, counter: tk.IntVar):
        counter.set(counter.get() + 1)

    def assign_label(self, index):
        self.label_var.set(self.possible_labels[index])
        self.increment_y(self.counters[index])
        self.next_data()

    def next_data(self):
        label = self.label_var.get()
        self.labels.append(label)
        self.label_var.set("")
        self.index += 1

        if self.index < len(self.image_paths):
            self.image_display_frame.display_data(self.image_paths[self.index])
        else:
            self.save_labels()

    def save_labels(self):
        with open(self.output, "w") as f:
            for image_path, label in zip(self.image_paths, self.labels):
                f.write(f"{image_path}{self.sep}{label}\n")
        
        self.message = f"No more images to label.Labels saved to {self.output}."

    def run(self):
        self.setting_frame.load_folder()
        if self.setting_frame.image_count > 0:
            self.image_display_frame.display_data(self.image_paths[self.index])
        else:
            print("No images found in the specified directory.")
        self.window.mainloop()

def main():
    labeler = DataLabeler()
    labeler.run()

if __name__ == "__main__":
    main()


