from fe_code.processes import process

class dirichletPoint():
    def __init__(self):
        self.prescribed_disp_vector = [0,0,0]

    def implementProcess(self,stiffness_matrix):
        # Currently not considering prescribed non-zero displacements!!
        node_index = self.node_number - 1
        ndofs = stiffness_matrix.shape[0]
        dofs = [2*node_index,2*node_index+1]
        for i in range(2):
            if self.prescribed_disp_vector[i] != None:
                for col in range(ndofs):
                    #go thru cols, holding rows constant
                    stiffness_matrix[dofs[i],col] = 0.0
                for row in range(ndofs):
                    #go thru rows, holding cols constant
                    stiffness_matrix[row,dofs[i]] = 0.0
                # add in diagonal entry
                stiffness_matrix[dofs[i], dofs[i]] = 1.0

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