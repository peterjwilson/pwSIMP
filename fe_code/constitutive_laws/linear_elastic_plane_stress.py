class linearElasticPlaneStressLaw():
    def __init__(self):
        self.description = 'Linear elastic plane stress law. Capable for 2D analysis currently'

    def getDescription(self):
        return self.description

    def calculate2DConstitutiveMatrix(self,constitutive_data,constitutive_matrix):
        constitutive_matrix = 0
