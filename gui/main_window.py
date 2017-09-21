# Python imports
import tkinter as tk
from tkinter import ttk
import logging

# Project imports
from gui import visualisation_window
from gui import popup_window_form_2col
from gui import popup_window_process_input

from fe_code.data_structures import system_data
from fe_code.data_structures import geometry_data
from fe_code.data_structures import gui_data

from fe_code.solvers import linear_static
from fe_code.solvers import SIMP

from fe_code.processes import dirchlet_point
from fe_code.processes import neumann_point

from gui.gui_functions import highlighting


# This class is the main Window of the GUI
class mainWindow():  # This is the main Window

    def __init__(self, root_window):  # Constructor
        self.window = root_window
        self.window.wm_title("pwSIMP")
        root_window.state('zoomed')
        logging.info("Initializing Main Window")
        self.header_color = "#606060"
        self.main_frame = self._SetMainFrame()
        self.system_data = system_data.systemData()
        self.gui_data = gui_data.guiData()
        self.process_data = self.system_data.getProcessData()
        self.highlighting = highlighting.highlighting(self.system_data)

        # setup variables for input boxes
        self.child_window_open = False
        self.input_variable_vector = []
        self.input_finalize_function = None
        self.strain_list = self.system_data.getStrainEnergy()
        self.visualisation_setup = False

        vertical_index = [1]
        # Setup left frame
        child_frame_1_w = [30]
        self.child_frame_1 = self._SetChildFrame(child_frame_1_w)
        self.child_frame_1.pack(anchor=tk.W, fill=tk.Y, expand=False, side=tk.LEFT)
        self._InitializeFrame1Widgets(self.child_frame_1, child_frame_1_w, vertical_index)
        self.child_frame_1.pack()

        # Setup right frame
        child_frame_2_w = [self.window.winfo_screenwidth() - child_frame_1_w[0]]
        self.child_frame_2 = self._SetChildFrame(child_frame_2_w)
        self.child_frame_2.pack(anchor=tk.N, fill=tk.BOTH, expand=True, side=tk.LEFT)
        root_window.update()
        self.visualisation_window = visualisation_window.visualisationWindow(self.system_data, self.child_frame_2)
        self.visualisation_setup = True

    def _SetMainFrame(self):
        frame_main = ttk.Frame(self.window)
        # frame_main.grid(column=0, row=0, sticky=(tk.N ,tk.W ,tk.E ,tk.S))
        return frame_main

    def _SetChildFrame(self, framewidth):
        frame_child = ttk.Frame(self.window, width=framewidth)
        return frame_child

    def _InitializeFrame1Widgets(self, frame, child_frame_1_w, vertical_index):
        self._CreateLabel(frame, "Geometry definition", vertical_index, child_frame_1_w)
        self._SetButton_DefineGeometry(frame, "Define basic geometry", vertical_index, child_frame_1_w)
        # self._SetButton_ImportGeometry(frame, "Import external geometry", vertical_index, child_frame_1_w)

        self._CreateLabel(frame, "View options", vertical_index, child_frame_1_w)
        self._SetButton_DisplayNodes(frame, "Display nodes", vertical_index, child_frame_1_w)

        self._CreateLabel(frame, "Material definition", vertical_index, child_frame_1_w)
        self._SetButton_DefineMaterial(frame, "Define material properties", vertical_index, child_frame_1_w)
        self._SetButton_ShowMaterialResponse(frame, "Show material response", vertical_index, child_frame_1_w)

        self._CreateLabel(frame, "Dirichlet BCs", vertical_index, child_frame_1_w)
        self._SetButton_DefineDirichletPoint(frame, "Point", vertical_index, child_frame_1_w)
        # line
        # surface

        self._CreateLabel(frame, "Neumann BCs", vertical_index, child_frame_1_w)
        self._SetButton_DefineNeumannPoint(frame, "Point", vertical_index, child_frame_1_w)
        # line
        # surface

        # self._CreateLabel(frame, "Discretisation", vertical_index, child_frame_1_w)
        # self._SetButton_DefineManualMesh(frame, "Manually mesh", vertical_index, child_frame_1_w)
        # automesh

        self._CreateLabel(frame, "Solution", vertical_index, child_frame_1_w)
        self._SetButton_SolveLinearSystem(frame, "Solve linear system", vertical_index, child_frame_1_w)
        self._SetProgressBar(frame)
        self._SetButton_PerformSIMPOptimisation(frame, "Perform SIMP optimisation", vertical_index, child_frame_1_w)
        self.addStrainEnergyBox(frame,"Strain energy")

    def _CreateLabel(self, frame, label_string, vertical_index_position, width):
        # tk.Label(frame, text=label_string, justify=tk.LEFT, bg="#606060",
        #        relief=tk.GROOVE, padx=20).grid(row=vertical_index_position, column=0, columnspan=2, sticky=tk.W + tk.E)
        label = tk.Label(frame, text=label_string, justify=tk.LEFT, bg="#606060",
                         relief=tk.GROOVE, padx=20)
        label.pack(fill=tk.X)
        vertical_index_position[0] += 1

    def _SetButton_DefineGeometry(self, frame, label_string, vertical_index_position, button_width):
        button_geo = tk.Button(frame, text=label_string, width=button_width,
                               command=lambda: self.OpenChildWindow(self._CreateBasicGeometryEntryWindow))
        # button_geo.grid(row=vertical_index_position, column=0, columnspan=2)
        button_geo.pack(fill=tk.X)
        vertical_index_position[0] += 1

    def _SetButton_ImportGeometry(self, frame, label_string, vertical_index_position, button_width):
        button_geo = tk.Button(frame, text=label_string, width=button_width,
                               command=lambda: self.OpenChildWindow(self._CreateImportGeometryEntryWindow))
        # button_geo.grid(row=vertical_index_position, column=0, columnspan=2)
        button_geo.pack(fill=tk.X)
        vertical_index_position[0] += 1

    def _SetButton_DisplayNodes(self, frame, label_string, vertical_index_position, button_width):
        button_geo = tk.Button(frame, text=label_string, width=button_width,
                               command=lambda: self.system_data.toggleDisplayNodes(self.visualisation_window.update))
        # button_geo.grid(row=vertical_index_position, column=0, columnspan=2)
        button_geo.pack(fill=tk.X)
        vertical_index_position[0] += 1

    def _SetButton_DefineMaterial(self, frame, label_string, vertical_index_position, button_width):
        button_geo = tk.Button(frame, text=label_string, width=button_width,
                               command=lambda: self.OpenChildWindow(self._CreateMaterialEntryWindow))
        # button_geo.grid(row=vertical_index_position, column=0, columnspan=2)
        button_geo.pack(fill=tk.X)
        vertical_index_position[0] += 1

    def _SetButton_ShowMaterialResponse(self, frame, label_string, vertical_index_position, button_width):
        button_geo = tk.Button(frame, text=label_string, width=button_width,
                               command=lambda: self.OpenChildWindow(self._CreateMaterialResponseWindow))
        # button_geo.grid(row=vertical_index_position, column=0, columnspan=2)
        button_geo.pack(fill=tk.X)
        vertical_index_position[0] += 1

    def _SetButton_DefineDirichletPoint(self, frame, label_string, vertical_index_position, button_width):
        button_geo = tk.Button(frame, text=label_string, width=button_width,
                               command=lambda: self.OpenChildWindow(self._CreateDirichletPoint))
        # button_geo.grid(row=vertical_index_position, column=0, columnspan=2)
        button_geo.pack(fill=tk.X)
        vertical_index_position[0] += 1

    def _SetButton_DefineNeumannPoint(self, frame, label_string, vertical_index_position, button_width):
        button_geo = tk.Button(frame, text=label_string, width=button_width,
                               command=lambda: self.OpenChildWindow(self._CreateNeumannPoint))
        # button_geo.grid(row=vertical_index_position, column=0, columnspan=2)
        button_geo.pack(fill=tk.X)
        vertical_index_position[0] += 1

    def _SetButton_DefineManualMesh(self, frame, label_string, vertical_index_position, button_width):
        button_geo = tk.Button(frame, text=label_string, width=button_width,
                               command=lambda: self.OpenChildWindow(self._CreateManualMesh))
        # button_geo.grid(row=vertical_index_position, column=0, columnspan=2)
        button_geo.pack(fill=tk.X)
        vertical_index_position[0] += 1

    def _SetButton_SolveLinearSystem(self, frame, label_string, vertical_index_position, button_width):
        button_geo = tk.Button(frame, text=label_string, width=button_width,
                               command=lambda: self.solveLinearElasticSystem())
        # button_geo.grid(row=vertical_index_position, column=0, columnspan=2)
        button_geo.pack(fill=tk.X)
        vertical_index_position[0] += 1

    def _SetButton_PerformSIMPOptimisation(self, frame, label_string, vertical_index_position, button_width):
        button_geo = tk.Button(frame, text=label_string, width=button_width,
                               command=lambda: self.runSIMPmethod())
        # button_geo.grid(row=vertical_index_position, column=0, columnspan=2)
        button_geo.pack(fill=tk.X)
        vertical_index_position[0] += 1

    def OpenChildWindow(self, child_create_function, args=None):
        if self.child_window_open:
            self.PlotCmdOutput("Only one window can be open at a time", "red")
        else:
            if args is None:
                self.child_window_object = child_create_function()
            else:
                self.child_window_open = True
                self.child_window_object = child_create_function(args)

    def _CreateBasicGeometryEntryWindow(self):
        text_vector = []
        text_vector.append('Xmin')
        text_vector.append('Xmax')
        text_vector.append('Ymin')
        text_vector.append('Ymax')
        text_vector.append('Xdiv')
        text_vector.append('Ydiv')
        self.input_variable_vector.clear()
        self.input_finalize_function = self.finalizeBasicGeometryEntryWindow
        self.BasicGeometryEntryWindow = popup_window_form_2col.popup_2_col(6, text_vector, 'Enter basic geometry',
                                                                           self.input_variable_vector,
                                                                           self.input_finalize_function)
        return self.BasicGeometryEntryWindow

    def finalizeBasicGeometryEntryWindow(self):
        self.child_window_open = False

        # recover extremities of rectangle domain

        Xmin = float(self.input_variable_vector[0].get())
        Xmax = float(self.input_variable_vector[1].get())
        Ymin = float(self.input_variable_vector[2].get())
        Ymax = float(self.input_variable_vector[3].get())

        X1 = Xmin
        Y1 = Ymin
        X2 = Xmax
        Y2 = Ymin
        X3 = Xmax
        Y3 = Ymax
        X4 = Xmin
        Y4 = Ymax

        # split into square elements with divisions
        Xdiv = float(self.input_variable_vector[4].get())
        Ydiv = float(self.input_variable_vector[5].get())

        Xstep = (Xmax - Xmin) / Xdiv
        Ystep = (Ymax - Ymin) / Ydiv

        geom_data = self.system_data.getGeometryData()
        master_node_vector = geom_data.getNodeVector()
        master_element_vector = geom_data.getElementVector()

        divisions = [Xdiv,Ydiv]
        self.system_data.setSystemDivisions(divisions)
        step = [Xstep,Ystep]
        self.system_data.setSystemStepSize(step)

        number_of_nodes = int((Xdiv + 1) * (Ydiv + 1))

        for i in range(number_of_nodes):
            # work like a typewriter, horizontally to the end, then back and up
            Xindex = i % (Xdiv + 1)
            Yindex = (i - Xindex) / (Xdiv + 1)
            x = Xmin + Xindex * Xstep
            y = Ymin + Yindex * Ystep
            z = 0.0
            position = [x, y, z]
            node = geometry_data.nodal_data(master_node_vector, position, i + 1)
            geom_data.updateSystemExtremities(position)

        number_of_square_elements = int(Xdiv * Ydiv)

        for i in range(number_of_square_elements):
            # work like a typewriter, horizontally to the end, then back and up
            Xindex = i % Xdiv
            Yindex = (i - Xindex) / Xdiv

            # node numbers (not indexes) for current element
            n1 = int((Yindex) * (Xdiv + 1) + Xindex + 1)
            n2 = int(n1 + 1)
            n3 = int(n1 + (Xdiv + 1))
            n4 = int(n3 + 1)

            node_numbers = [n1, n2, n4, n3]  # arranged anti-clockwise
            geometry_data.element_data_Q4(master_element_vector, node_numbers, i + 1)

        # geom_data.removeDuplicateNodes()

        self.visualisation_window.update()

    def _CreateMaterialEntryWindow(self):
        text_vector = []
        text_vector.append('Thickness')
        text_vector.append('Youngs modulus')
        text_vector.append('Poissons ratio')
        text_vector.append('Penalty factor p')
        text_vector.append('Volume fraction')
        self.input_variable_vector.clear()
        self.input_finalize_function = self.finalizeMaterialEntryWindow
        self.BasicGeometryEntryWindow = popup_window_form_2col.popup_2_col(5, text_vector,
                                                                           'Enter elastic material data',
                                                                           self.input_variable_vector,
                                                                           self.input_finalize_function)
        return self.BasicGeometryEntryWindow

    def finalizeMaterialEntryWindow(self):
        t = float(self.input_variable_vector[0].get())
        E = float(self.input_variable_vector[1].get())
        nu = float(self.input_variable_vector[2].get())
        p = float(self.input_variable_vector[3].get())
        vol_frac = float(self.input_variable_vector[4].get())
        self.system_data.setVolumeFrac(vol_frac)
        constitutive_data = {'thickness': t, 'E': E, 'nu': nu, 'p': p, 'rho':vol_frac}
        geom_data = self.system_data.getGeometryData()
        elem_data = geom_data.getElementVector()
        for i in range(len(elem_data)):
            e = elem_data[i]
            e.setConstitutiveData(constitutive_data)

    def _CreateDirichletPoint(self):
        dirichlet_point_process_vector = self.process_data.getDirichletPointProcessVector()

        self.dirichletPointInput = popup_window_process_input.processInput(dirchlet_point.dirichletPoint,
                                                                           dirichlet_point_process_vector,
                                                                           self.finalizeProcessInput)

    def _CreateNeumannPoint(self):
        neumann_point_process_vector = self.process_data.getNeumannPointProcessVector()

        self.neumannPointInput = popup_window_process_input.processInput(neumann_point.neumannPoint,
                                                                         neumann_point_process_vector,
                                                                         self.finalizeProcessInput)

    def finalizeProcessInput(self):
        self.visualisation_window.update()

    def _SetProgressBar(self,frame):
        self.progress_bar = ttk.Progressbar(frame, orient=tk.HORIZONTAL, mode='determinate')
        self.progress_bar.pack(fill=tk.X)
        self.progress_bar['value'] = 0.0

    def updateProgressBar(self,percentage):
        self.progress_bar['value'] = percentage
        self.window.update_idletasks()

    def solveLinearElasticSystem(self):
        linear_static.linearSolver(self.system_data,self.updateProgressBar)
        self.visualisation_window.update()

    def runSIMPmethod(self):
        SIMP.SIMPOptimisation(self.system_data,self.updateProgressBar,self.updateStrainEnergyBox)
        self.visualisation_window.update()

    def addStrainEnergyBox(self,frame,title):
        ##add list
        self.listbox = tk.Listbox(frame)
        self.listbox.pack(fill=tk.BOTH)
        self.updateStrainEnergyBox()

    def updateStrainEnergyBox(self):
        self.listbox.delete(0,tk.END)
        for i in range(len(self.strain_list)):
            self.listbox.insert(tk.END, str(self.strain_list[i]))
        if self.visualisation_setup:
            self.visualisation_window.update()
