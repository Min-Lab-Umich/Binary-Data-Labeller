import sys

from Labeller import Labeller
import tkinter as tk


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
    app = Labeller(tk.Tk(), sys.argv[1], 'png')
    app.mainloop()
