import tkinter as tk
from PIL import Image, ImageTk
import os
import argparse

class DataLabeler:
    def __init__(self, image_directory, labels_file, output, sep):
        self.image_directory = image_directory
        with open (labels_file) as f:
            self.possible_labels =  [l.strip() for l in f.readlines()]
        self.output = output
        self.sep = sep
        self.keymap = {chr(i): i - 48 if i < 58 else i - 55 if i < 91 else i - 61 for i in range(48, 91)}

        self.index = 0
        self.image_paths = []
        self.labels = []

        self.window = tk.Tk()
        self.window.title("Manual Data Labeler")

        self.label_var = tk.StringVar()
        self.label_var.set("")

        self.image_label = tk.Label(self.window)
        self.image_label.pack()

        self.button_frame = tk.Frame(self.window)
        self.button_frame.pack()

        self.count_frame = tk.Frame(self.window)
        self.count_frame.pack()
        self.counters = []

        for index, label in enumerate(self.possible_labels):
            button = tk.Button(self.button_frame, text=label, command=lambda idx=index:self.assign_label(idx))
            self.window.bind(str(self.keymap[str(index + 1)]), lambda event, btn=button: btn.invoke())
            button.pack(side=tk.LEFT, padx=5) 
            counter = tk.IntVar(value=0)
            label = tk.Label(self.count_frame, textvariable=counter)  
            label.pack(side=tk.LEFT, padx=10)
            self.counters.append(counter) 

    def get_image_paths(self):
        for filename in os.listdir(self.image_directory):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                image_path = os.path.join(self.image_directory, filename)
                self.image_paths.append(image_path)
    
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
            self.display_data()
        else:
            self.complete_labeling()

    def display_data(self):
        image_path = self.image_paths[self.index]
        image = Image.open(image_path)
        image = image.resize((400, 300))
        tk_image = ImageTk.PhotoImage(image)
        self.image_label.configure(image=tk_image)
        self.image_label.image = tk_image

    def complete_labeling(self):
        self.window.destroy()
        self.save_labels()

    def save_labels(self):
        with open(self.output, "w") as f:
            for image_path, label in zip(self.image_paths, self.labels):
                f.write(f"{image_path}{self.sep}{label}\n")

        print("Labeling Complete!")
        print("Labels saved to", self.output)

    def run(self):
        self.get_image_paths()
        if len(self.image_paths) > 0:
            self.display_data()
        else:
            print("No images found in the specified directory.")
            self.window.destroy()
        self.window.mainloop()

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--image_directory", 
        "-imdir", 
        help="Input image directory",
        default="./Dataset"
    )

    parser.add_argument(
        "--labels", 
        "-l", 
        help="Class labels in .txt / .csv format, one line per label",
        default= "./labels.txt"
    )

    parser.add_argument(
        "--output", 
        "-o", 
        help="Output file name", 
        default="./output.txt"
    )

    parser.add_argument(
        "--sep", 
        "-s", 
        help="Delimiter", 
        default=","
    )
    
    args = parser.parse_args()

    labeler = DataLabeler(args.image_directory, args.labels, args.output, args.sep)
    labeler.run()

if __name__ == "__main__":
    main()


