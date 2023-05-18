import tkinter as tk
from Manager import Manager
from FrameWidgets import FrameWidgets
import argparse

class DataLabeler:
    def __init__(self, mode):
        self.window = tk.Tk()
        self.window.title("Manual Data Labeler")

        self.manager = Manager()
        self.frame_widgets = FrameWidgets(self.window, self.manager, mode)

    def run(self):
        self.frame_widgets.read_images()
        self.frame_widgets.read_labels()
        self.frame_widgets.initialize_buttons()
        self.window.mainloop()

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--mode",
        "-m",
        help= "Single (Binary or Categorical Label) or Multi-label mode",
        choices= ['single', 'multi'],
        default= "single"
    )
    args = parser.parse_args()

    labeler = DataLabeler(args.mode)
    labeler.run()

if __name__ == "__main__":
    main()


