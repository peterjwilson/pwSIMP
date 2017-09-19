from fe_code.data_structures import geometry_data
from fe_code.data_structures import process_data

class systemData:
    def __init__(self):
        self.geometryData = geometry_data.geometryData()
        self.processesData = process_data.processData()
        self.displacements_calculated = False
        self.SIMP_calculated = False
        self.display_nodes = False
        self.original_volume_frac = 1.0

    def getGeometryData(self):
        return self.geometryData

    def getConstitutiveData(self):
        return self.constitutiveData

    def getProcessData(self):
        return self.processesData

    def getDisplacementsCalculatedBool(self):
        return self.displacements_calculated

    def setDisplacementsCalculatedBool(self,bool_in):
        self.displacements_calculated =  bool_in

    def setSIMPCalculatedBool(self,bool_in):
        self.SIMP_calculated =  bool_in

    def getSIMPCalculatedBool(self):
        return self.SIMP_calculated

    def getDisplayNodes(self):
        return self.display_nodes

    def toggleDisplayNodes(self,window_update):
        if self.display_nodes:
            self.display_nodes = False
        else:
            self.display_nodes = True
        window_update()

    def setVolumeFrac(self,frac_in):
        self.original_volume_frac = frac_in

    def getVolumeFrac(self):
        return self.original_volume_frac
