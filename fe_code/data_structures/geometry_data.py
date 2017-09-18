

class geometryData:
    def __init__(self):
        # Mesh variables
        self.element_vector = [] #holds references to each element
        self.node_vector = [] #holds references to each node (class)
        self.bounding_centre = 0
        self.bounding_radius = 0
        self.bounding_sphere = [self.bounding_centre,self.bounding_radius]

        # Raw geometry variables
        self.point_vector = []
        self.line_vector = []
        self.surface_vector = []

    def add_element(self,element_type,element_nodes,element_number):
        n1 = geometryData.nodal_data(self.node_vector,element_nodes[0])
        n2 = geometryData.nodal_data(self.node_vector, element_nodes[1])
        n3 = geometryData.nodal_data(self.node_vector, element_nodes[2])
        element_nodal_vector = [n1,n2,n3]
        geometryData.element_data(self.element_vector,element_type,element_nodal_vector,element_number)

    def printGeomData(self):
        for i in range(len(self.element_vector)):
            print("\nelement ",i+1)
            element_nodes = self.element_vector[i].getNodalVector()
            for j in range(len(element_nodes)):
                element_nodes[j].printPosition()

    def getElementVector(self):
        return self.element_vector

    def getNodeVector(self):
        return self.node_vector


    class element_data:
        def __init__(self,master_element_vector,element_type,element_nodal_vector,element_number):
            if element_type == 'T3':
                geometryData.element_data_T3(master_element_vector,element_nodal_vector,element_number)
            else:
                raise Exception('An element which is not T3 has been created. Only T3 elements exist now.')



    class element_data_T3:
        def __init__(self,master_element_vector,node_vector,element_number):
            self.type = 'T3'
            self.element_node_vector = node_vector #vector references to the 3 nodes
            self.element_number = element_number
            master_element_vector.append(self)

        def getNodalVector(self):
            return self.element_node_vector

    class nodal_data:
        def __init__(self, master_nodal_vector,position):
            master_nodal_vector.append(self)
            self.node_number = len(master_nodal_vector)
            self.position_vector = position
            self.velocity_vector = []
            self.acceleration_vector = []
            self.dofs = 2 #hardcoded membrane


        def printPosition(self):
            print("position = ",self.position_vector)

        def getPositionVector(self):
            return self.position_vector

        def getPositionVector2D(self):
            return [self.position_vector[0],self.position_vector[1]]

        def getNodeNumber(self):
            return self.node_number

        def getNumberOfNodalDofs(self):
            return self.dofs