import tkinter as tk
from tkinter import ttk
from pathlib import Path
import glob, os
import csv


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

        # check if such a file exists
        self.config_file = self.dir / "config.txt"
        self.csv_output_dir = self.dir /  "labels.csv"
        self.num_labelled = 0
        if not self.config_file.exists():
            print("New work session")
            # initialise the config file
            # create the output csv
            self.init_config()
            # create csv file
            self.create_csv_file()
        else:
            print("Resuming from a checkpoint")
            self.num_labelled = self.read_config_file()

        self.opened_csv = None
        # open csv file, append the csv file
        with open(self.csv_output_dir, 'a') as self.opened_csv:
            self.csv_write = csv.writer(self.opened_csv)
            self.render()
            
    
    def save_check_point(self):
        """Save the labelled data back into """


    def render(self):
        """Render the image and the options."""
        
        # render the image
        # reference: https://stackoverflow.com/questions/23901168/how-do-i-insert-a-jpeg-image-into-a-python-tkinter-window
        path = 
        img = ImageTk.PhotoImage(Image.open(path))
        panel = tk.Label(self.master, image = img)
        panel.pack()

        # redner the options: yes or no; and bind to keyboard events
        # reference: https://codereview.stackexchange.com/questions/191477/binding-a-keyboard-key-to-a-tkinter-button
        yes = ttk.Button(self.master, text="YES", command=self.yes_callback())
        yes.pack('y', lambda event: self.yes_callback())

        no = ttk.Button(self.master, text="NO", command=self.no_callback())
        no.pack('n', lambda event: self.no_callback())


    def yes_callback(self):
        

        pass

    def no_callback(self):
        pass

    def add_all_files(self):
        """Index all the files.
        
        Assume glob.glob iterations' order doesn't change across runs...
        """
        for file in glob.glob(f"*.{self.data_type}"):
            # append all the files
            self.files.append(file)

    def init_config(self):
        """Touch a configuration file."""
        pass

    def create_csv_file(self):
        """Create a csv file for output"""
        with open(self.csv_output_dir, 'w') as _:
            pass
        

    def read_config_file(self):
        """Read the configuration file and return . Should only contain 1 number."""
        with open(self.config_file, 'r') as file:
            data = file.read()
            return int(data)