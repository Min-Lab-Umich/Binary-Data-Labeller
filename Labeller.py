import tkinter as tk
from tkinter import ttk
from pathlib import Path
import os
import csv
from PIL import Image, ImageTk
import cv2
import shutil

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
        self.yes = None
        self.no = None
        self.img_tk = None

        # check if such a file exists
        self.config_file_path = self.dir / "config.txt"
        # self.csv_output_path = self.dir / "labels.csv"
        
        self.particle_path = self.dir / "output/particle"
        self.non_particle_path = self.dir / "output/non_particle"
        self.create_output_dir()
        self.current_image_idx = 0
        if not self.config_file_path.exists():
            print("New work session")
            # initialise the config file
            # create the output csv
            self.init_config()
            # create csv file
            # self.create_csv_file()
        else:
            print("Resuming from a checkpoint")
            self.current_image_idx = self.read_config_file()

        self.opened_csv = None
        self.current_image_idx += 1
        # open csv file, append the csv file
        self.render_initial()

    def create_output_dir(self):
        os.makedirs(self.particle_path, exist_ok=True)
        os.makedirs(self.non_particle_path, exist_ok=True)

    def save_check_point(self):
        """Save the labelled data back into """
        with open(self.config_file_path, 'w') as self.config_file:
            self.config_file.write(str(self.current_image_idx))

    def get_current_image_path(self):
        """Return the path to the current image that we are labelling."""
        if self.current_image_idx >= len(self.files):
            self.render_finished()
            # return str(self.dir / self.files[len(self.files) - 1])

        return str(self.dir / self.files[self.current_image_idx])

    def render_finished(self):
        print("Finished Labelling")
        finished = tk.Label(self.master, text='Finished Labelling')
        if self.yes is not None:
            self.yes.state = "disabled"
        if self.no is not None:
            self.no.state = "disabled"
        finished.pack()
        exit()

    def render_next(self):
        """Render the next image."""
        path = self.get_current_image_path()
        print(path)
        img = cv2.imread(path)
        b, g, r = cv2.split(img)
        img = cv2.merge((r, g, b))
        self.img = Image.fromarray(img)
        # self.img.show()
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
        self.yes = ttk.Button(self.master, text="YES",
                              command=self.yes_callback)
        self.master.bind('y', lambda event: self.yes_callback())

        self.no = ttk.Button(self.master, text="NO", command=self.no_callback)
        self.master.bind('n', lambda event: self.no_callback())

        self.yes.pack()
        self.no.pack()

    # def open_csv_output(self, func):
    #     with open(self.csv_output_path, 'a') as self.opened_csv:
    #         self.csv_writer = csv.writer(self.opened_csv)
    #         func()

    def copy_file(self, filename, is_particle):
        """Copy the file to an appropriate output folder"""
        
        copy_to_dir = None
                    
        self.save_check_point()
        self.current_image_idx += 1
        if self.current_image_idx != len(self.files):
            self.render_next()
        else:
            self.render_finished()
            
        if is_particle:
            copy_to_dir = self.particle_path
        else:
            copy_to_dir = self.non_particle_path
        shutil.copyfile(filename, f"{copy_to_dir}/{filename.split('/')[-1]}")

    def yes_callback(self):
        """Write a yes to the output file."""
        self.copy_file(self.get_current_image_path(), 1)

    def no_callback(self):
        """Write a no to the output file."""
        self.copy_file(self.get_current_image_path(), 0)

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
            self.config_file.write("-1")  #

    # def create_csv_file(self):
        # """Create a csv file for output"""
        # with open(self.csv_output_path, 'w') as _:
            # pass

    def read_config_file(self):
        """Read the configuration file and return . Should only contain 1 number."""
        with open(self.config_file_path, 'r') as file:
            data = list(map(int, file.readlines()))
            return int(data[0])