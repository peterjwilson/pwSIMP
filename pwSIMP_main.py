# Python imports
import tkinter
import logging
import pygame
import pyglet

# Project imports
# import converter_utilities as utils
# import top_gui_functions as gui

from gui import main_window

def main():
    logging.info("Starting pwSIMP")
    root = tkinter.Tk()
    main_window.mainWindow(root)

    #pygame.display.update()

    while True:
        root.update()
        pygame.display.update()

    # root.after(100,pygame_update)
    # #root.after_idle(pygame.display.update)
    # root.mainloop()



    #root.update()


if __name__ == '__main__':
    main()
