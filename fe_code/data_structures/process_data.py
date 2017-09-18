

class processData:
    def __init__(self):
        self.dirichlet_point = []  # holds references to each process
        self.neumann_point = []  # holds references to each process

    def addDirichletPoint(self,process_in):
        self.dirichlet_point.append(process_in)

    def getDirichletPointProcessVector(self):
        return self.dirichlet_point

    def addNeumannPoint(self, process_in):
        self.neumann_point.append(process_in)

    def getNeumannPointProcessVector(self):
        return self.neumann_point

    def printProcessVector(self,process_vector):
        for i in range(len(process_vector)):
            process = process_vector[i]
