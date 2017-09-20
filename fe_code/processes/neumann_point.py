from fe_code.processes import process

class neumannPoint():
    def __init__(self):
        # setup defaults
        self.prescribed_force_vector = [0,0,0]

    def implementProcess(self,force_vector):
        node_index = self.node_number - 1
        dofs = [2*node_index,2*node_index+1]
        for i in range(2):
            if self.prescribed_force_vector[i] != None:
                force_vector[dofs[i]] += self.prescribed_force_vector[i]


    def setProcess(self,node_number,force_vector):
        self.prescribed_force_vector = force_vector
        self.node_number = node_number

    def getProcessName(self):
        return 'Neumann point process'

    def getProcessInfo(self):
        self.dict = {'node_number':self.node_number,'force_vector':self.prescribed_force_vector}
        return self.dict

    def getProcessString(self):
        s = []
        for i in range(3):
            s.append(str(self.prescribed_force_vector[i]))
            if self.prescribed_force_vector[i] == None:
                s[i] = 'Null'
        return_string = 'Node:' + str(self.node_number) + "        " + 'f_x = ' + s[0] + '           ' + 'f_y = ' + s[1]
        return return_string