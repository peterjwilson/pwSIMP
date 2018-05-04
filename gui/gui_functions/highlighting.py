#import pygame

from fe_code.data_structures import gui_data


class highlighting:
    def __init__(self, master_system_data):
        self.system_data = master_system_data

    def highlightAllNodes(self, guiData, pygame_instance):
        geom_data = self.system_data.getGeometryData()
        nodal_vector = geom_data.getNodeVector()
        highlighting_style = {'shape': 'circle', 'color': (150, 150, 150), 'size': 5}
        for i in range(len(nodal_vector)):
            highlighted_entity = gui_data.highlightedEntity(nodal_vector[i], highlighting_style)
            guiData.addHighlightedPoint(highlighted_entity)
        pygame_instance.draw()

    def clearHighlightAllNodes(self,guiData, pygame_instance):
        guiData.clearHighlightedPoints()
        pygame_instance.draw()
