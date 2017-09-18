

class geometryData:
    def __init__(self):
        # Mesh variables
        self.element_vector = [] #holds references to each element
        self.node_vector = [] #holds references to each node (class)
        self.system_min_x = [0]
        self.system_max_x = [1]
        self.system_min_y = [0]
        self.system_max_y = [1]

        # Raw geometry variables
        self.point_vector = []
        self.line_vector = []
        self.surface_vector = []

    def add_element(self,element_type,element_nodes,element_number):
        # add nodes into master nodal vector
        element_nodal_vector = []
        for i in range(len(element_nodes)):
            element_nodal_vector.append(self.nodal_data(self.node_vector,element_nodes[i]))

        # update system extremities
        for i in range(len(element_nodal_vector)):
            node = element_nodal_vector[i].getPositionVector2D()
            self.updateSystemExtremities(node)

        #finally, add element
        geometryData.element_data(self.element_vector,element_type,element_nodal_vector,element_number)

    def removeDuplicateNodes(self):
        remove_count = 0
        for e in range(len(self.element_vector)):
            element = self.element_vector[e]
            element_nodes = element.getNodalVector()
            for e_n in range(len(element_nodes)):
                node_index = element_nodes[e_n].getNodeNumber() - 1 - remove_count
                node_position = element_nodes[e_n].getPositionVector2D()
                # now check against other nodes after this node
                for i in range(0,node_index):
                    check_node_position = self.node_vector[i].getPositionVector2D()
                    if node_position[0] == check_node_position[0]:
                        if node_position[1] == check_node_position[1]:
                            #duplicate found, replace with lowest index duplicate
                            element_nodes[e_n] = self.node_vector[i]
                            del self.node_vector[node_index]
                            remove_count += 1
                            break
        # Now go thru and update the node numbers
        for i in range(len(self.node_vector)):
            node = self.node_vector[i]
            node.updateNodeNumber(i+1)



    def printGeomData(self):
        for i in range(len(self.element_vector)):
            print("\nelement ",i+1)
            element_nodes = self.element_vector[i].getNodalVector()
            for j in range(len(element_nodes)):
                element_nodes[j].printPosition()

    def getSystemExtremities(self):
        return [self.system_min_x[0],self.system_max_x[0],self.system_min_y[0],self.system_max_y[0]]

    def updateSystemExtremities(self,node_position_vector):
        #x
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


    class element_data:
        def __init__(self,master_element_vector,element_type,element_nodal_vector,element_number):
            if element_type == 'T3':
                geometryData.element_data_T3(master_element_vector,element_nodal_vector,element_number)
            elif element_type == 'Q4':
                geometryData.element_data_Q4(master_element_vector,element_nodal_vector,element_number)
            else:
                raise Exception('An element which is not T3 or Q4 has been created. Only T3 elements exist now.')

    class element_data_Q4:
        def __init__(self,master_element_vector,node_vector,element_number):
            self.type = 'Q4'
            self.element_node_vector = node_vector #vector references to the 4 nodes
            self.element_number = element_number
            master_element_vector.append(self)

        def getNodalVector(self):
            return self.element_node_vector

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

        def updateNodeNumber(self,int_in):
            self.node_number = int_in

        def getNumberOfNodalDofs(self):
            return self.dofs