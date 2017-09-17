import tkinter as tk
import pygame
import os

from fe_code.data_structures import system_data

class pygameWindow:
    def __init__(self,parentFrame,frameWidth,frameHeight,systemData_in):
        self.parent = parentFrame
        self.system_data = systemData_in
        self.geom_data = self.system_data.getGeometryData()
        os.environ['SDL_WINDOWID'] = str(self.parent.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        self.screen = pygame.display.set_mode((frameWidth[0], frameHeight))
        self.screen.fill(pygame.Color(255, 255, 255))

        pygame.display.init()
        pygame.display.update()

    def draw(self):
        self.screen.fill(pygame.Color(255, 255, 255))
        self.drawElements()
        pygame.display.update()
        #root.update()


    def drawElements(self):
        element_vector = self.geom_data.getElementVector()
        for element in range(len(element_vector)):
            self.drawElementLines(element_vector[element])


    def drawElementLines(self,element):
        element_nodes = element.getNodalVector()
        for node in range(len(element_nodes)):
            start = element_nodes[node].getPositionVector2D()
            end =  element_nodes[(node + 1) % len(element_nodes)].getPositionVector2D()
            pygame.draw.line(self.screen,(50,50,255),start,end)