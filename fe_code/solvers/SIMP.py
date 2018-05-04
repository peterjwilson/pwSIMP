from copy import deepcopy
import logging

import numpy as np
import sympy as sp
from numpy import linalg as la
from sympy import Matrix
from sympy.matrices import zeros

from fe_code.solvers import linear_static


def SIMPOptimisation(master_system_data, updateProgressBarFunc,update_func):
    runSIMPMethod(master_system_data, updateProgressBarFunc,update_func)


def runSIMPMethod(master_system_data, updateProgressBarFunc,update_func):
    # get references
    system_data = master_system_data
    geom_data = master_system_data.getGeometryData()
    nodal_data = geom_data.getNodeVector()
    element_data = geom_data.getElementVector()
    process_data = master_system_data.getProcessData()

    system_data.setSaveImages(False)


    # Distribute material according to volume fraction. Already done.
    original_vol_frac = system_data.getVolumeFrac()


    # Declarations

    iteration_limit = 1
    filter_radius = int(2)

    # Iteration loop
    for iteration in range(iteration_limit):
        system_data.incrementSimpIteration()
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
            dot_prod = (u.T * k * u)[0]
            compliance += dot_prod #includes density effects


            # Determine element sensitivty
            virgin_strain_energy = dot_prod/(rho**p) #excludes density effects
            dc.append(-p*(rho**(p-1)) * virgin_strain_energy)

        #Exit element loop
        master_system_data.appendStrainEnergy(compliance)
        update_func()

        # Filter sensitivities
        divisions = system_data.getSystemDivisions()
        dc = filterSensitivities(divisions,dc,rho_vector,filter_radius)

        # Update design with Optimality Criterion method
        rho_vector = np.array(rho_vector)
        dc = np.array(dc)
        updated_rho = updateWithOC(element_data,dc, rho_vector,original_vol_frac)
        for i in range(len(element_data)):
            element = element_data[i]
            element.setElementDensity(updated_rho[i])
        system_data.setSIMPCalculatedBool(True)


    # Finalise
    #window_update()

def filterSensitivities(divisions,dc,rho_vector,filter_radius):
    xdiv = int(divisions[0])
    ydiv = int(divisions[1])
    updated_dc = []
    for row in range(ydiv):
        for col in range(xdiv):
            sum = 0.0
            kmin = int(max(row-filter_radius,0)) #vertical extremities
            kmax = int(min(row+filter_radius,ydiv))
            lmin = int(max(col - filter_radius, 0)) # horizontal extremities
            lmax = int(min(col + filter_radius, xdiv))
            updated_dc_entry = 0.0
            for k in range(kmin,kmax):
                for l in range(lmin, lmax):
                    lin_pos_l_k = l + k * xdiv
                    fac = filter_radius - ((row-k)**2 + (col-l)**2)**0.5
                    sum += max(0.0,fac)
                    updated_dc_entry += max(0,fac)*rho_vector[lin_pos_l_k]*dc[lin_pos_l_k]
            updated_dc_entry /= sum
            updated_dc.append(updated_dc_entry)

    return updated_dc

def updateWithOC(element_data,dc, rho_vector,original_vol_frac):
    l1 = 0
    l2 = 100000 #100000
    move = 0.2 #0.2
    rho_minus = rho_vector - move
    rho_plus = rho_vector + move
    original_volume = original_vol_frac * len(element_data)
    number_of_elements = len(rho_vector)
    while (l2-l1) > 0.0001:
        #updated_rho = []
        vol = 0.0
        lmid = 0.5*(l2+l1)
        rho_calc = rho_vector*((-dc/lmid)**0.5)
        for i in range(number_of_elements):
            new_entry = max(0.001,
                           max(rho_minus[i],
                               min(1.0,
                                   min(rho_plus[i],rho_calc[i])
                                   )
                               )
                           )
            #updated_rho.append(new_entry)
            vol += new_entry
        if vol - original_volume > 0:
            l1 = lmid
        else:
            l2 = lmid

    # with the converge lagrangian multiplier, store the results

    updated_rho = []
    lmid = 0.5 * (l2 + l1)
    rho_calc = rho_vector * ((-dc / lmid) ** 0.5)
    for i in range(number_of_elements):
        new_entry = max(0.001,
                        max(rho_minus[i],
                            min(1.0,
                                min(rho_plus[i], rho_calc[i])
                                )
                            )
                        )
        updated_rho.append(new_entry)
    return updated_rho

