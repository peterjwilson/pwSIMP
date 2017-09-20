# Python imports
import tkinter
import logging

# Project imports
# import converter_utilities as utils
# import top_gui_functions as gui

from gui import main_window


def main():
    logging.info("Starting pwSIMP")
    root = tkinter.Tk()
    main_window.mainWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()
