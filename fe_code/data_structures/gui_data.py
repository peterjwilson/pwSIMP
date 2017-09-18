


class guiData:
    def __init__(self):
        # Mesh variables
        self.highlighted_points = [] #holds references to highlighted entities

    def addHighlightedPoint(self,highlightedEntity):
        self.highlighted_points.append(highlightedEntity)

    def getHighlightedPoints(self):
        return self.highlighted_points

    def clearHighlightedPoints(self):
        self.highlighted_points.clear()

class highlightedEntity():
    def __init__(self,entity,highlighting_style):
        self.entity = entity
        self.highlighting_style = highlighting_style

    def getEntity(self):
        return self.entity

    def getStyle(self):
        return self.highlighting_style