import tkinter as tk
from tkinter import ttk
from pathlib import Path
import glob, os
import csv
from PIL import Image, ImageTk


class Labeller(tk.Frame):
    """Labelling true or false data"""

    def __init__(self, master, dir_path_str: str, data_type: str):
        super().__init__(master)
        self.master = master
                
        """Initialise labeller variables"""
        # input/output directory, which contains
        try:
            self.dir = Path(dir_path_str)
        except:
            print("Failed to open path")

        self.data_type = data_type
        self.files = []
        self.add_all_files()
        self.img = None
        self.panel = None
        self.img_tk = None

        # check if such a file exists
        self.config_file_path = self.dir / "config.txt"
        self.csv_output_path = self.dir / "labels.csv"
        
        self.last_labelled_idx = -1
        if not self.config_file_path.exists():
            print("New work session")
            # initialise the config file
            # create the output csv
            self.init_config()
            # create csv file
            self.create_csv_file()
        else:
            print("Resuming from a checkpoint")
            self.last_labelled_idx = self.read_config_file()

        self.opened_csv = None
        self.current_image_idx = self.last_labelled_idx + 1
        # open csv file, append the csv file
        self.render_initial()
    
    def save_check_point(self):
        """Save the labelled data back into """
        with open(self.config_file_path, 'w') as self.config_file:
            self.config_file.write(str(self.last_labelled_idx))

    def get_current_image_path(self):
        """Return the path to the current image that we are labelling."""
        return str(self.dir / self.files[self.current_image_idx])

    def render_next(self):
        """Render the next image."""
        path = self.get_current_image_path()
        self.img = Image.open(path)
        self.img_tk = ImageTk.PhotoImage(self.img)
        if self.panel is not None:
            self.panel.configure(image=self.img_tk)
            self.panel.image = self.img_tk


    def render_initial(self):
        """Render the image and the options."""
        # render the image
        # reference: https://stackoverflow.com/questions/23901168/how-do-i-insert-a-jpeg-image-into-a-python-tkinter-window
        self.render_next()
        self.panel = tk.Label(self.master, image=self.img_tk)
        self.panel.pack()

        # render the options: yes or no; and bind to keyboard events
        # reference: https://codereview.stackexchange.com/questions/191477/binding-a-keyboard-key-to-a-tkinter-button
        self.yes = ttk.Button(self.master, text="YES", command=self.yes_callback)
        self.master.bind('y', lambda event: self.yes_callback())

        self.no = ttk.Button(self.master, text="NO", command=self.no_callback)
        self.master.bind('n', lambda event: self.no_callback())

        self.yes.pack()
        self.no.pack()

    def open_csv_output(self, func):
        with open(self.csv_output_path, 'w') as self.opened_csv:
            self.csv_writer = csv.writer(self.opened_csv)
            func()

    def write_to_csv(self, filename, value):
        self.open_csv_output(lambda :
                             self.csv_writer.
                             writerow([filename, value]))
        self.last_labelled_idx += 1
        self.current_image_idx = self.last_labelled_idx + 1
        self.render_next()

    def yes_callback(self):
        """Write a yes to the output file."""
        self.write_to_csv(self.get_current_image_path(), 1)

    def no_callback(self):
        """Write a no to the output file."""
        self.write_to_csv(self.get_current_image_path(), 0)

    def add_all_files(self):
        """Index all the files.
        
        Assume glob.glob iterations' order doesn't change across runs...
        """
        for file in os.listdir(self.dir):
            if file.endswith(f".{self.data_type}"):
            # append all the files
                self.files.append(file)

    def init_config(self):
        """Touch a configuration file."""
        with open(self.config_file_path, 'w') as self.config_file:
            self.config_file.write("-1") # 

    def create_csv_file(self):
        """Create a csv file for output"""
        with open(self.csv_output_path, 'w') as _:
            pass
        

    def read_config_file(self):
        """Read the configuration file and return . Should only contain 1 number."""
        with open(self.config_file_path, 'r') as file:
            data = list(map(int, file.readlines()))
            return int(data[0])