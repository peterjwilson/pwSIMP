
class results_data:
    def __init__(self):
        self.element_data
        self.node_data



class element_data:
    def __init__(self,type,nodes,element_number):
        if type == 'T3':
            self.element_list.append(element_data_T3(nodes,element_number))
        else:
            raise Exception('An element which is not T3 has been created. Only T3 elements exist now.')


class element_data_T3:
    def __init__(self,nodes,element_number):
        self.element_nodes = nodes
        self.element_number = element_number

class nodal_data:
    def __init__(self, node_number, position):
        self.node_number = node_number
        self.x = position[0]
        self.y = position[1]
        self.z = position[2]