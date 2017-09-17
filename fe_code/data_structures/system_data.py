from fe_code.data_structures import geometry_data
from fe_code.data_structures import constitutive_data

class systemData:
    def __init__(self):
        self.geometryData = geometry_data.geometryData()
        self.constitutiveData = constitutive_data.constitutiveData()

    def getGeometryData(self):
        return self.geometryData

    def getConstitutiveData(self):
        return self.constitutiveData
