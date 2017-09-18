from fe_code.constitutive_laws import linear_elastic_plane_stress

class constitutiveData:
    def __init__(self):
        self.constitutive_law = linear_elastic_plane_stress.linearElasticPlaneStressLaw
        self.constitutive_properties = None

    def setConstitutiveProperties(self,ConstitutiveProperties):
        self.constitutive_properties = ConstitutiveProperties

    def getConstitutiveProperties(self):
        return self.constitutive_properties

    def printData(self):
        #constitutive_data = {'thickness':t,'E':E, 'nu':nu,'p':p}
        print(self.constitutive_properties)


