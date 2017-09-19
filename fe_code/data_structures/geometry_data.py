from copy import deepcopy
from sympy import Matrix

class geometryData:
    def __init__(self):
        # Mesh variables
        self.element_vector = []  # holds references to each element
        self.node_vector = []  # holds references to each node (class)
        self.system_min_x = [0]
        self.system_max_x = [1]
        self.system_min_y = [0]
        self.system_max_y = [1]

        # Raw geometry variables
        self.point_vector = []
        self.line_vector = []
        self.surface_vector = []

    def add_element(self, element_type, element_nodes, element_number):
        # add nodes into master nodal vector
        element_nodal_vector = []
        for i in range(len(element_nodes)):
            element_nodal_vector.append(self.nodal_data(self.node_vector, element_nodes[i]))

        # update system extremities
        for i in range(len(element_nodal_vector)):
            node = element_nodal_vector[i].getPositionVector2D()
            self.updateSystemExtremities(node)

        # finally, add element
        geometryData.element_data(self.element_vector, element_type, element_nodal_vector, element_number)

    def removeDuplicateNodes(self):
        remove_count = 0
        for e in range(len(self.element_vector)):
            element = self.element_vector[e]
            element_nodes = element.getNodalVector()
            for e_n in range(len(element_nodes)):
                node_index = element_nodes[e_n].getNodeNumber() - 1 - remove_count
                node_position = element_nodes[e_n].getPositionVector2D()
                # now check against other nodes after this node
                for i in range(0, node_index):
                    check_node_position = self.node_vector[i].getPositionVector2D()
                    if node_position[0] == check_node_position[0]:
                        if node_position[1] == check_node_position[1]:
                            # duplicate found, replace with lowest index duplicate
                            element_nodes[e_n] = self.node_vector[i]
                            del self.node_vector[node_index]
                            remove_count += 1
                            break
        # Now go thru and update the node numbers
        for i in range(len(self.node_vector)):
            node = self.node_vector[i]
            node.updateNodeNumber(i + 1)

    def printGeomData(self):
        for i in range(len(self.element_vector)):
            print("\nelement ", i + 1)
            element_nodes = self.element_vector[i].getNodalVector()
            for j in range(len(element_nodes)):
                element_nodes[j].printPosition()

    def getSystemExtremities(self):
        return [self.system_min_x[0], self.system_max_x[0], self.system_min_y[0], self.system_max_y[0]]

    def updateSystemExtremities(self, node_position_vector):
        # x
        if node_position_vector[0] < self.system_min_x[0]:
            self.system_min_x[0] = node_position_vector[0]
        elif node_position_vector[0] > self.system_max_x[0]:
            self.system_max_x[0] = node_position_vector[0]

        # y
        if node_position_vector[1] < self.system_min_y[0]:
            self.system_min_y[0] = node_position_vector[1]
        elif node_position_vector[1] > self.system_max_y[0]:
            self.system_max_y[0] = node_position_vector[1]

    def getElementVector(self):
        return self.element_vector

    def getNodeVector(self):
        return self.node_vector

class element_data_Q4:
    def __init__(self, master_element_vector, node_numbers, element_number):
        self.type = 'Q4'
        self.element_node_vector = node_numbers  # node numbers (not indexes) for this element
        self.element_number = element_number
        self.element_index = element_number - 1 #position in master element vector
        master_element_vector.append(self)
        self.has_constitutive_data = False

    def setConstitutiveData(self,constitutive_data):
        self.constitutive_data = deepcopy(constitutive_data)
        self.thickness = self.constitutive_data['thickness']
        self.nu = self.constitutive_data['nu']
        self.E = self.constitutive_data['E']
        self.p = self.constitutive_data['p']
        self.rho = self.constitutive_data['rho']
        self.has_constitutive_data = True

    def setElementK(self,k_in):
        self.k = k_in

    def getElementK(self):
        return self.k

    def calculateConstitutiveMatrix(self):
        #E = self.E*(self.rho**self.p)
        C = Matrix([[1, self.nu, 0], [self.nu, 1, 0], [0, 0, (1 - self.nu) / 2]])
        C = C * (self.E / (1 - self.nu ** 2)) * self.thickness
        return C

    def getNodalVector(self):
        return self.element_node_vector

    def setElementDensity(self,rho_in):
        self.rho = rho_in

    def getElementDensity(self):
        return self.rho

    def getPenalty(self):
        return self.p

    def getRhoPowerP(self):
        return (self.rho**self.p)

class element_data_T3:
    def __init__(self, master_element_vector, node_vector, element_number):
        self.type = 'T3'
        self.element_node_vector = node_vector  # node numbers (not indexes) for this element
        self.element_number = element_number
        master_element_vector.append(self)

    def getNodalVector(self):
        return self.element_node_vector

class nodal_data:
    def __init__(self, master_nodal_vector, position, node_number):
        master_nodal_vector.append(self)
        self.node_number = node_number
        self.node_index = node_number-1 #position in master nodal vector
        self.position_vector = position
        self.displacement_vector = []
        self.velocity_vector = []
        self.acceleration_vector = []
        self.dofs = 2  # hardcoded membrane

    def printPosition(self):
        print("position = ", self.position_vector)

    def getPositionVector(self):
        return self.position_vector

    def getPositionVector2D(self):
        return [self.position_vector[0], self.position_vector[1]]

    def getNodeNumber(self):
        return self.node_number

    def updateNodeNumber(self, int_in):
        self.node_number = int_in

    def getNumberOfNodalDofs(self):
        return self.dofs

    def setDisplacements(self,disp_in):
        self.displacement_vector = disp_in

    def getDisplacements(self):
        return self.displacement_vector