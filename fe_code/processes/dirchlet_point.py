from fe_code.processes import process

class dirichletPoint(process):
    def __init__(self):
        # setup defaults
        self.prescribed_disp_vector = [0,0,0]

    def __init__(self,prescribed_disp_vector,node_ref):
        self.prescribed_disp_vector = prescribed_disp_vector
        self.node_reference = node_ref

    def implementProcess(self,stiffness_matrix,mass_matrix,force_vector):
        force_vector = 0