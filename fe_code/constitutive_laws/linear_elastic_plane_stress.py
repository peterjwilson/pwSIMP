import numpy as np
import sympy as sp
from sympy import Matrix

class linearElasticPlaneStressLaw():
    def __init__(self):
        self.description = 'Linear elastic plane stress law. Capable for 2D analysis currently'

    def getDescription(self):
        return self.description

    def calculate2DConstitutiveMatrix(self,constitutive_data):
        #constitutive_data = {'thickness':t,'E':E, 'nu':nu,'p':p}
        nu = constitutive_data['nu']
        E = constitutive_data['E']
        p = constitutive_data['p']
        Mat = Matrix([[1, nu, 0], [nu, 1, 0], [0, 0, (1 - nu) / 2]])
        Mat = Mat * (E / (1 - nu ** 2))
        return Mat
