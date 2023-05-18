import tkinter as tk
from Manager import Manager
from FrameWidgets import FrameWidgets

class DataLabeler:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Manual Data Labeler")

        self.manager = Manager()
        self.frame_widgets = FrameWidgets(self.window, self.manager)

    def run(self):
        self.frame_widgets.read_images()
        self.frame_widgets.read_labels()
        self.frame_widgets.initialize_buttons(self.assign_label)
        self.window.mainloop()

def main():
    labeler = DataLabeler()
    labeler.run()

if __name__ == "__main__":
    main()


