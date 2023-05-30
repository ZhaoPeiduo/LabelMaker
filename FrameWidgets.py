import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
from Manager import Manager
import os
import shutil

class FrameWidgets:
    KEYMAP = {chr(i): i - 48 if i < 58 else i - 55 if i < 91 else i - 61 for i in range(48, 91)}
    def __init__(self, window, manager: Manager, mode) -> None:
        self.window = window
        self.manager = manager
        self.mode=  mode

        self.control_frame = tk.Frame(self.window)
        self.control_frame.pack()

        self.read_images_button = tk.Button(self.control_frame, text="Load Folder", command=self.read_images)
        self.read_images_button.pack(side=tk.LEFT, padx=5)

        self.save_labels_button = tk.Button(self.control_frame, text="Save Labels", command=self.save_labels)
        self.save_labels_button.pack(side=tk.LEFT, padx=5)

        self.undo_button = tk.Button(self.control_frame, text="Undo", command=self.undo)
        self.window.bind("u", lambda event: self.undo_button.invoke())
        self.undo_button.pack(side=tk.LEFT, padx=5)

        self.exit_button = tk.Button(self.control_frame, text="Exit", command=self.exit)
        self.window.bind("<Escape>", lambda event: self.exit_button.invoke())
        self.exit_button.pack(side=tk.LEFT, padx=5)

        if mode == "multi":
            self.window.bind("<Return>", lambda event: self.confirm())

        self.image_label = tk.Label(self.window)
        self.image_label.pack()

        self.label_button_frame = tk.Frame(self.window)
        self.archive_button_frame = tk.Frame(self.window)

        self.count_frame = tk.Frame(self.window)
        self.count_frame.pack()

        self.message = f"{self.manager.image_count - self.manager.index} images remaining"
        self.message_frame = tk.Label(self.window, textvariable=self.message)
        self.message_frame.pack()

    def initialize_label_buttons(self):
        for index, label in enumerate(self.manager.possible_labels):
            label_button = tk.Button(self.label_button_frame, text=label, command=lambda idx=index:self.assign_label(idx))
            self.window.bind(str(self.KEYMAP[str(index + 1)]), lambda event, btn=label_button: btn.invoke())
            label_button.pack(side=tk.LEFT, padx=5) 
            counter = tk.IntVar(value=0)
            label = tk.Label(self.count_frame, textvariable=counter)  
            label.pack(side=tk.LEFT, padx=10)
            self.manager.label_counters.append(counter) 
        self.label_button_frame.pack(side=tk.BOTTOM)

    def initialize_archive_button(self):
        archive_button = tk.Button(self.archive_button_frame, text="Archive", command=self.archive)
        self.window.bind("a", lambda event : archive_button.invoke())
        archive_button.pack(side=tk.LEFT, padx=5) 
        archive_label = tk.Label(self.archive_button_frame, textvariable=self.manager.archive_counter)
        archive_label.pack(side=tk.LEFT, padx=5)
        self.archive_button_frame.pack(side=tk.BOTTOM)


    def read_images(self):
        image_directory = filedialog.askdirectory(title="Select images to be labeled")
        self.image_directory = image_directory
        self.manager.reset_images()
        self.manager.load_images(image_directory)

        if self.manager.image_count > 0:
            self.display_data(self.manager.image_paths[self.manager.index])
        else:
            print("No images found in the specified directory.")

    def read_labels(self):
        label_file = filedialog.askopenfilename(title="Select file containing possible labels")
        self.manager.load_labels(label_file)
        if self.mode == "multi":
            self.label_buffer = {key : value for key, value in zip(self.manager.possible_labels, 
                                                                   [0 for _ in range(len(self.manager.possible_labels))])}
 
    def save_labels(self):
        save_file = filedialog.asksaveasfile(title="Select location to save labels")
        self.manager.save_labels(save_file)

    def exit(self):
        self.window.destroy()

    def display_data(self, image_path):
        image = Image.open(image_path)
        image = image.resize((400, 300))
        tk_image = ImageTk.PhotoImage(image)
        self.image_label.configure(image=tk_image)
        self.image_label.image = tk_image

    def hit_end(self):
        if self.manager.index == self.manager.image_count:
            self.save_labels()
            return True
        return False
        
    def next_image(self):
        if self.hit_end():
            return
        
        self.manager.index += 1
        
        if self.hit_end():
            return
        
        self.display_data(self.manager.image_paths[self.manager.index])

    def undo(self):
        if self.manager.index == 0:
            print("Nothing to undo!")
            return

        self.manager.index -= 1
        current_label = self.manager.labels.pop(-1)
        curr_image_path = self.manager.image_paths[self.manager.index]
        
        if not os.path.exists(curr_image_path):
            archive_to_undo = os.path.join('./archive', os.path.basename(self.image_directory), os.path.basename(curr_image_path))
            shutil.move(archive_to_undo, os.path.dirname(curr_image_path))
            self.manager.archive_counter.set(self.manager.archive_counter.get() - 1)

        elif self.mode == "single":
            decrement = self.manager.possible_labels.index(current_label)
            self.manager.label_counters[decrement].set(self.manager.label_counters[decrement].get() - 1)
        
        else:
            for label, value in current_label.items():
                print(self.manager.labels)
                decrement = self.manager.possible_labels.index(label)
                self.manager.label_counters[decrement].set(self.manager.label_counters[decrement].get() - 1)
        
        self.display_data(self.manager.image_paths[self.manager.index])
    
    def confirm(self):
        if self.hit_end():
            return
        
        self.manager.labels.append(self.label_buffer)
        self.label_buffer = {key : value for key, value in zip(self.manager.possible_labels, 
                                                                   [0 for _ in range(len(self.manager.possible_labels))])}
        self.next_image()

    def assign_label(self, index):
        if self.hit_end():
            return
        
        label_to_add = self.manager.possible_labels[index]
        if self.mode == "single":
            self.manager.labels.append(label_to_add)
            self.manager.label_counters[index].set(self.manager.label_counters[index].get() + 1)
            self.next_image()

        elif self.mode == "multi" and self.label_buffer[label_to_add] == 0:
            self.manager.label_counters[index].set(self.manager.label_counters[index].get() + 1)
            self.label_buffer[label_to_add] += 1
    
    def archive(self):
        if self.hit_end():
            return
        
        assert self.image_directory is not None
        if not os.path.exists('./archive'):
            os.mkdir('./archive')
        archive_folder = './archive/'+ os.path.basename(self.image_directory)
        if not os.path.exists(archive_folder):
            os.mkdir(archive_folder)
        image_path_to_archive = self.manager.image_paths[self.manager.index]
        shutil.move(image_path_to_archive, archive_folder)
        self.manager.labels.append("Archived")
        self.manager.archive_counter.set(self.manager.archive_counter.get() + 1)
        self.next_image()
   