from fe_code.data_structures import geometry_data
from fe_code.data_structures import constitutive_data
from fe_code.data_structures import process_data

class systemData:
    def __init__(self):
        self.geometryData = geometry_data.geometryData()
        self.constitutiveData = constitutive_data.constitutiveData()
        self.processesData = process_data.processData()
        self.displacements_calculated = False

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