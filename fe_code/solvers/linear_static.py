from copy import deepcopy

import numpy as np
import sympy as sp
from numpy import linalg as la
from sympy import Matrix
from sympy.matrices import zeros

from fe_code.constitutive_laws import linear_elastic_plane_stress


def linearSolver(master_system_data):
    assembleAndSolve(master_system_data)

def assembleAndSolve(master_system_data):
    # get references
    system_data = master_system_data
    geom_data = master_system_data.getGeometryData()
    constitutive_data = master_system_data.getConstitutiveData()
    nodal_data = geom_data.getNodeVector()
    element_data = geom_data.getElementVector()
    process_data = master_system_data.getProcessData()

    # general system information
    n_dof = 2 * len(nodal_data)  # total number of degrees of freedom
    K = np.zeros((n_dof, n_dof))
    F = np.zeros(n_dof)

    # calc constitutive matrix, same for all elements
    cl = linear_elastic_plane_stress.linearElasticPlaneStressLaw()
    cl_props = constitutive_data.getConstitutiveProperties()
    thickness = cl_props['thickness']
    C = cl.calculate2DConstitutiveMatrix(cl_props)

    # assemble global stiffness matrix
    computeGlobalStiffnessMatrix(K,C,thickness,element_data,nodal_data)

    # impose processes
    # make a deepcopy before imposing processes
    K_mod = deepcopy(K)
    F_mod = deepcopy(F)
    imposeProcesses(K_mod, F_mod,process_data)

    # solve modified system of equations
    U = la.solve(K_mod, F_mod)

    # write displacements
    writeDisplacements(nodal_data,U)
    system_data.setDisplacementsCalculatedBool(True)

def computeGlobalStiffnessMatrix(K,C,thickness,element_data,nodal_data):

    # loop over all elements
    for i in range(len(element_data)):
        element_node_number_vector = element_data[i].getNodalVector()
        ele_node_coord = zeros(4, 2)
        for j in range(len(element_node_number_vector)):
            node_index = element_node_number_vector[j] - 1
            node = nodal_data[node_index]
            node_position_vector = node.getPositionVector2D()
            ele_node_coord[j, 0] = node_position_vector[0]
            ele_node_coord[j, 1] = node_position_vector[1]
        local_k = calcLocalQ4StiffnessMatrix(ele_node_coord,C,thickness)

        # add to global matrix
        addLocalMatrixToGlobalMatrix(local_k, K, element_node_number_vector)

def calcLocalQ4StiffnessMatrix(ele_node_coord,C,thickness):
    GP = Matrix([[-0.577350269189626, 0.577350269189626],
                 [0.577350269189626, 0.577350269189626],
                 [-0.577350269189626, -0.577350269189626],
                 [0.577350269189626, -0.577350269189626]])
    WtFac = np.array([1, 1, 1, 1])

    ##ShapeFunctions
    xi = sp.symbols('xi')
    eta = sp.symbols('eta')

    N1 = ((1 - xi) * (1 - eta)) / 4  # shapefunction node 1
    N2 = ((1 + xi) * (1 - eta)) / 4  # shapefunction node 2
    N3 = ((1 + xi) * (1 + eta)) / 4  # shapefunction node 3
    N4 = ((1 - xi) * (1 + eta)) / 4  # shapefunction node 4

    Ni = Matrix([[N1, N2, N3, N4]])  # assemble shapefunctions
    dNi_dxi = sp.diff(Ni, xi)  # derive shapefunctions for xi
    dNi_deta = sp.diff(Ni, eta)  # derive shapefunctions for eta

    ##calculate Jacobian J + inverse
    J_element = Matrix([dNi_dxi, dNi_deta]) * ele_node_coord
    J_elememt_inverse = sp.Inverse(J_element)

    ##calculate B matrix
    B = zeros(3, 8)  # initialize B
    for j in range(4):
        index_counter = j * 2
        dNj_dxi_deta = Matrix([[dNi_dxi[j]], [dNi_deta[j]]])
        dNj_dxdy = J_elememt_inverse * dNj_dxi_deta  # calculate dNj_dx,_dy
        temp_B = Matrix([[dNj_dxdy[0], 0], [0, dNj_dxdy[1]],
                         [dNj_dxdy[1], dNj_dxdy[0]]])
        B[0:3, index_counter:(index_counter + 2)] = temp_B  # assemble B

    K_stiff_i = zeros(8, 8)  # initialize local element stiffness matrix
    ####### 2) --> loop over all Gauss Points
    n_GP = 4
    for j in range(n_GP):
        gp_weight = WtFac[j]  # current gauss point weight
        gp_xi = GP[j, 0]  # current gauss point coordinate xi
        gp_eta = GP[j, 1]  # current gauss point coordinate eta

        B_j = (B.subs(xi, gp_xi)).subs(eta, gp_eta)  # evaluate B at GP
        B_j_transpose = B_j.T  # transpose B
        J_element_j = (J_element.subs(xi, gp_xi)).subs(eta, gp_eta)  # evaluate Jacobian at GP
        det_J_element_j = sp.det(J_element_j)  # calculate current det(J)

        # evaluate element stiffness matrix at current GP (2D - integration)
        K_stiff_i += thickness * B_j_transpose * C * B_j * det_J_element_j * gp_weight * gp_weight
    return K_stiff_i

def addLocalMatrixToGlobalMatrix(local_k, K,element_node_number_vector):
    element_dof_vector = []
    for i in range(4):
        node_index = element_node_number_vector[i] - 1
        element_dof_vector.append(2 * node_index)
        element_dof_vector.append(2 * node_index + 1)
    for row in range(8):
        for col in range(8):
            global_row = element_dof_vector[row]
            global_col = element_dof_vector[col]
            K[global_row, global_col] += local_k[row, col]

def imposeProcesses(K, F, process_data):
    # apply neumann first
    neumann_point_process_vector = process_data.getNeumannPointProcessVector()
    for i in range(len(neumann_point_process_vector)):
        neumann_point = neumann_point_process_vector[i]
        neumann_point.implementProcess(F)

    # now apply dirichlet
    dirichlet_point_process_vector = process_data.getDirichletPointProcessVector()
    for i in range(len(dirichlet_point_process_vector)):
        dirichlet_point = dirichlet_point_process_vector[i]
        dirichlet_point.implementProcess(K)

def writeDisplacements(nodal_data,U):
    for i in range(len(nodal_data)):
        disp = [U[2 * i], U[2 * i + 1]]
        nodal_data[i].setDisplacements(disp)
