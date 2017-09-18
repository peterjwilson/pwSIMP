from fe_code.processes import process

class dirichletPoint():
    def __init__(self):
        self.prescribed_disp_vector = [0,0,0]

    def implementProcess(self,stiffness_matrix,mass_matrix,force_vector):
        force_vector = 0

    def setProcess(self,node_number,disp_vector):
        self.prescribed_disp_vector = disp_vector
        self.node_number = node_number

    def getProcessName(self):
        return 'Dirichlet point process'

    def getProcessInfo(self):
        self.dict = {'node_number':self.node_number,'disp_vector':self.prescribed_disp_vector}
        return self.dict

    def getProcessString(self):
        s = []
        for i in range(3):
            s.append(str(self.prescribed_disp_vector[i]))
            if self.prescribed_disp_vector[i] == None:
                s[i] = 'Null'
        return_string = 'Node:' + str(self.node_number) + "        " + 'u_x = ' + s[0] + '           ' + 'u_y = ' + s[1]
        return return_string