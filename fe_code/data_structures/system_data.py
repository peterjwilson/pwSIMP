from fe_code.data_structures import geometry_data
from fe_code.data_structures import constitutive_data
from fe_code.data_structures import process_data

class systemData:
    def __init__(self):
        self.geometryData = geometry_data.geometryData()
        self.constitutiveData = constitutive_data.constitutiveData()
        self.processesData = process_data.processData()

    def getGeometryData(self):
        return self.geometryData

    def getConstitutiveData(self):
        return self.constitutiveData
