import tkinter as tk
import pygame
import os
from copy import deepcopy

from fe_code.data_structures import gui_data


class pygameWindow:
    def __init__(self, parentFrame, frameWidth, frameHeight, systemData_in, guiData_in):
        self.parent = parentFrame
        self.system_data = systemData_in
        self.geom_data = self.system_data.getGeometryData()
        self.gui_data = guiData_in
        self.height = frameHeight
        self.width = frameWidth[0]
        os.environ['SDL_WINDOWID'] = str(self.parent.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(pygame.Color(255, 255, 255))

        pygame.display.init()
        pygame.display.update()

    def draw(self):
        # maybe update widget height and width here

        # clear
        self.screen.fill(pygame.Color(255, 255, 255))

        # draw things
        self.drawElements()
        self.drawHighlightedPoints()

        # finally, update
        pygame.display.update()

    def flipYValueOfPoint(self, node):
        # flip, because (0,0) is at the top left of the widget
        node[1] = self.height - node[1]
        # now it is at the bottom left of the widget

    def drawElements(self):
        element_vector = self.geom_data.getElementVector()
        for element in range(len(element_vector)):
            self.drawElementLines(element_vector[element])

    def drawElementLines(self, element):
        element_nodes = element.getNodalVector()
        for node in range(len(element_nodes)):
            start = element_nodes[node].getPositionVector2D()
            end = element_nodes[(node + 1) % len(element_nodes)].getPositionVector2D()
            self.flipYValueOfPoint(start)
            self.flipYValueOfPoint(end)
            pygame.draw.line(self.screen, (50, 50, 255), start, end)

    def convertVectorToInt(self,vector):
        for i in range(len(vector)):
            vector[i] = int(vector[i])

    def drawHighlightedPoints(self):
        highlighted_points = self.gui_data.getHighlightedPoints()
        if len(highlighted_points) > 0:
            for i in range(len(highlighted_points)):
                entity = highlighted_points[i]
                node = entity.getEntity()
                style = entity.getStyle()
                temp_point = deepcopy(node.getPositionVector2D())
                self.convertVectorToInt(temp_point)
                self.flipYValueOfPoint(temp_point)
                pygame.draw.circle(self.screen, style['color'], temp_point, int(style['size']))
