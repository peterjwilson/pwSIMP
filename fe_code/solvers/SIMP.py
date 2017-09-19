from copy import deepcopy
import logging

import numpy as np
import sympy as sp
from numpy import linalg as la
from sympy import Matrix
from sympy.matrices import zeros

from fe_code.solvers import linear_static


def SIMPOptimisation(master_system_data, updateProgressBarFunc,window_update):
    runSIMPMethod(master_system_data, updateProgressBarFunc,window_update)


def runSIMPMethod(master_system_data, updateProgressBarFunc,window_update):
    # get references
    system_data = master_system_data
    geom_data = master_system_data.getGeometryData()
    nodal_data = geom_data.getNodeVector()
    element_data = geom_data.getElementVector()
    process_data = master_system_data.getProcessData()

    # Distribute material according to volume fraction. Already done.
    original_vol_frac = system_data.getVolumeFrac()

    # Declarations

    iteration_limit = 5
    filter_radius = 2

    # Iteration loop
    for iteration in range(iteration_limit):
        # Solve for displacements
        linear_static.linearSolver(master_system_data, updateProgressBarFunc)

        compliance = 0.0
        dc = []
        rho_vector = []

        # Loop over all elements
        for i in range(len(element_data)):
            element = element_data[i]
            k = element.getElementK()
            element_node_numbers = element.getNodalVector()
            u = zeros(8,1)
            for j in range(4):
                node_index = element_node_numbers[j] - 1
                node = nodal_data[node_index]
                node_disp = node.getDisplacements()
                u[2 * j] = node_disp[0]
                u[2 * j + 1] = node_disp[1]
            rho = element.getElementDensity()
            rho_vector.append(rho)
            p = element.getPenalty()

            # Add compliance
            #f = k * u
            dot_prod = (u.T * k * u)[0]
            compliance += dot_prod #includes density effects


            # Determine element sensitivty
            virgin_strain_energy = dot_prod/(rho**p) #excludes density effects
            dc.append(-p*(rho**(p-1)) * virgin_strain_energy)

        #Exit element loop
        info = 'Compliance = ' + str(compliance)
        print(info)
        logging.info(info)
        # Filter sensitivities
        # filterSensitivities

        # Update design with Optimality Criterion method
        rho_vector = np.array(rho_vector)
        dc = np.array(dc)
        updated_rho = updateWithOC(element_data,dc, rho_vector,original_vol_frac)
        for i in range(len(element_data)):
            element = element_data[i]
            element.setElementDensity(updated_rho[i])
        system_data.setSIMPCalculatedBool(True)
        window_update()

    # Finalise


def filterSensitivities(dc,filter_radius):
    filter_radius = 1

def updateWithOC(element_data,dc, rho_vector,original_vol_frac):
    l1 = 0
    l2 = 100000
    move = 0.2
    while (l2-l1) > 0.0001:
        updated_rho = []
        lmid = 0.5*(l2+l1)
        rho_minus = rho_vector - move
        rho_plus = rho_vector + move
        rho_calc = rho_vector*((-dc/lmid)**0.5)
        for i in range(len(rho_vector)):
            new_entry = max(0.001,
                           max(rho_minus[i],
                               min(1.0,
                                   min(rho_plus[i],rho_calc[i])
                                   )
                               )
                           )
            updated_rho.append(new_entry)
        if sum(updated_rho) - original_vol_frac * len(element_data) > 0:
            l1 = lmid
        else:
            l2 = lmid
    return updated_rho

