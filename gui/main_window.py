# Python imports
import tkinter as tk
from tkinter import ttk
import logging
import _thread


# Project imports
from gui import pygame_window
from gui import popup_window_form_2col

from fe_code.data_structures import system_data
from fe_code.data_structures import gui_data

from gui.gui_functions import highlighting

# This class is the main Window of the GUI
class mainWindow(): # This is the main Window

    def __init__(self, root_window): # Constructor
        self.window = root_window
        self.window.wm_title("pwSIMP")
        root_window.state('zoomed')
        logging.info("Initializing Main Window")
        self.header_color = "#606060"
        self.main_frame = self._SetMainFrame()
        self.system_data = system_data.systemData()
        self.gui_data = gui_data.guiData()
        self.highlighting = highlighting.highlighting(self.system_data)


        # setup variables for input boxes
        self.child_window_open = False
        self.input_variable_vector = []
        self.input_finalize_function = None



        vertical_index = [1]
        #Setup left frame
        child_frame_1_w = [30]
        self.child_frame_1 = self._SetChildFrame(child_frame_1_w)
        self.child_frame_1.pack(anchor=tk.W, fill=tk.Y, expand=False, side=tk.LEFT)
        self._InitializeFrame1Widgets(self.child_frame_1,child_frame_1_w,vertical_index)
        self.child_frame_1.pack()

        # Setup right frame
        child_frame_2_w = [self.window.winfo_screenwidth() - child_frame_1_w[0]]
        self.child_frame_2 = self._SetChildFrame(child_frame_2_w)
        self.child_frame_2.pack(anchor=tk.N, fill=tk.BOTH, expand=True, side=tk.LEFT)
        root_window.update()
        self.pygame_instance = pygame_window.pygameWindow(self.child_frame_2,child_frame_2_w,self.child_frame_2.winfo_height(),self.system_data,self.gui_data)

    def _SetMainFrame(self):
        frame_main = ttk.Frame(self.window)
        #frame_main.grid(column=0, row=0, sticky=(tk.N ,tk.W ,tk.E ,tk.S))
        return frame_main

    def _SetChildFrame(self ,framewidth):
        frame_child = ttk.Frame(self.window, width = framewidth)
        return frame_child

    def _InitializeFrame1Widgets(self,frame,child_frame_1_w,vertical_index):
        self._CreateLabel(frame,"Geometry definition",vertical_index,child_frame_1_w)
        self._SetButton_DefineGeometry(frame,"Define basic geometry",vertical_index,child_frame_1_w)
        self._SetButton_ImportGeometry(frame, "Import external geometry", vertical_index, child_frame_1_w)

        self._CreateLabel(frame, "View options", vertical_index, child_frame_1_w)
        self._SetButton_DisplayNodes(frame, "Display nodes", vertical_index, child_frame_1_w)

        self._CreateLabel(frame, "Material definition", vertical_index, child_frame_1_w)
        self._SetButton_DefineMaterial(frame, "Define material properties", vertical_index, child_frame_1_w)
        self._SetButton_ShowMaterialResponse(frame, "Show material response", vertical_index, child_frame_1_w)

        self._CreateLabel(frame, "Dirichlet BCs", vertical_index, child_frame_1_w)
        self._SetButton_DefineDirichletPoint(frame, "Point", vertical_index, child_frame_1_w)
        #line
        #surface

        self._CreateLabel(frame, "Neumann BCs", vertical_index, child_frame_1_w)
        self._SetButton_DefineNeumannPoint(frame, "Point", vertical_index, child_frame_1_w)
        # line
        # surface

        self._CreateLabel(frame, "Discretisation", vertical_index, child_frame_1_w)
        self._SetButton_DefineManualMesh(frame, "Manually mesh", vertical_index, child_frame_1_w)
        # automesh

        self._CreateLabel(frame, "Solution", vertical_index, child_frame_1_w)
        self._SetButton_SolveLinearSystem(frame, "Solve linear system", vertical_index, child_frame_1_w)
        self._SetButton_PerformSIMPOptimisation(frame, "Perform SIMP optimisation", vertical_index, child_frame_1_w)

    def _CreateLabel(self,frame,label_string,vertical_index_position,width):
        #tk.Label(frame, text=label_string, justify=tk.LEFT, bg="#606060",
         #        relief=tk.GROOVE, padx=20).grid(row=vertical_index_position, column=0, columnspan=2, sticky=tk.W + tk.E)
        label = tk.Label(frame, text=label_string, justify=tk.LEFT, bg="#606060",
                 relief=tk.GROOVE, padx=20)
        label.pack(fill=tk.X)
        vertical_index_position[0] += 1

    def _SetButton_DefineGeometry(self,frame,label_string,vertical_index_position,button_width):
        button_geo = tk.Button(frame, text=label_string, width=button_width,
                               command=lambda: self.OpenChildWindow(self._CreateBasicGeometryEntryWindow))
        #button_geo.grid(row=vertical_index_position, column=0, columnspan=2)
        button_geo.pack(fill=tk.X)
        vertical_index_position[0] += 1

    def _SetButton_ImportGeometry(self, frame, label_string, vertical_index_position, button_width):
        button_geo = tk.Button(frame, text=label_string, width=button_width,
                               command=lambda: self.OpenChildWindow(self._CreateImportGeometryEntryWindow))
        #button_geo.grid(row=vertical_index_position, column=0, columnspan=2)
        button_geo.pack(fill=tk.X)
        vertical_index_position[0] += 1

    def _SetButton_DisplayNodes(self, frame, label_string, vertical_index_position, button_width):
        button_geo = tk.Button(frame, text=label_string, width=button_width,
                               command=lambda: self.highlighting.highlightAllNodes(self.gui_data,self.pygame_instance))
        # button_geo.grid(row=vertical_index_position, column=0, columnspan=2)
        button_geo.pack(fill=tk.X)
        vertical_index_position[0] += 1

    def _SetButton_DefineMaterial(self, frame, label_string, vertical_index_position, button_width):
        button_geo = tk.Button(frame, text=label_string, width=button_width,
                               command=lambda: self.OpenChildWindow(self._CreateMaterialEntryWindow))
        #button_geo.grid(row=vertical_index_position, column=0, columnspan=2)
        button_geo.pack(fill=tk.X)
        vertical_index_position[0] += 1

    def _SetButton_ShowMaterialResponse(self, frame, label_string, vertical_index_position, button_width):
        button_geo = tk.Button(frame, text=label_string, width=button_width,
                               command=lambda: self.OpenChildWindow(self._CreateMaterialResponseWindow))
        #button_geo.grid(row=vertical_index_position, column=0, columnspan=2)
        button_geo.pack(fill=tk.X)
        vertical_index_position[0] += 1

    def _SetButton_DefineDirichletPoint(self, frame, label_string, vertical_index_position, button_width):
        button_geo = tk.Button(frame, text=label_string, width=button_width,
                               command=lambda: self.OpenChildWindow(self._CreateDirichletPoint))
        #button_geo.grid(row=vertical_index_position, column=0, columnspan=2)
        button_geo.pack(fill=tk.X)
        vertical_index_position[0] += 1

    def _SetButton_DefineNeumannPoint(self, frame, label_string, vertical_index_position, button_width):
        button_geo = tk.Button(frame, text=label_string, width=button_width,
                               command=lambda: self.OpenChildWindow(self._CreateNeumannPoint))
        #button_geo.grid(row=vertical_index_position, column=0, columnspan=2)
        button_geo.pack(fill=tk.X)
        vertical_index_position[0] += 1

    def _SetButton_DefineManualMesh(self, frame, label_string, vertical_index_position, button_width):
        button_geo = tk.Button(frame, text=label_string, width=button_width,
                               command=lambda: self.OpenChildWindow(self._CreateManualMesh))
        #button_geo.grid(row=vertical_index_position, column=0, columnspan=2)
        button_geo.pack(fill=tk.X)
        vertical_index_position[0] += 1

    def _SetButton_SolveLinearSystem(self, frame, label_string, vertical_index_position, button_width):
        button_geo = tk.Button(frame, text=label_string, width=button_width,
                               command=lambda: self.OpenChildWindow(self._SolveLinearSystem))
        #button_geo.grid(row=vertical_index_position, column=0, columnspan=2)
        button_geo.pack(fill=tk.X)
        vertical_index_position[0] += 1

    def _SetButton_PerformSIMPOptimisation(self, frame, label_string, vertical_index_position, button_width):
        button_geo = tk.Button(frame, text=label_string, width=button_width,
                               command=lambda: self.OpenChildWindow(self._PerformSIMPOptimisation))
        #button_geo.grid(row=vertical_index_position, column=0, columnspan=2)
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
        text_vector=[]
        text_vector.append('Xmin')
        text_vector.append('Xmax')
        text_vector.append('Ymin')
        text_vector.append('Ymax')
        text_vector.append('Xdiv')
        text_vector.append('Ydiv')
        self.input_variable_vector.clear()
        self.input_finalize_function = self.finalizeBasicGeometryEntryWindow
        self.BasicGeometryEntryWindow = popup_window_form_2col.popup_2_col(6,text_vector,'Enter basic geometry',self.input_variable_vector,self.input_finalize_function)
        return self.BasicGeometryEntryWindow

    def finalizeBasicGeometryEntryWindow(self):
        self.child_window_open = False

        # recover extremities of rectangle domain

        Xmin= float(self.input_variable_vector[0].get())
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

        # split into triangle elements with divisions
        Xdiv = float(self.input_variable_vector[4].get())
        Ydiv = float(self.input_variable_vector[5].get())
        number_of_square_elements = int(Xdiv * Ydiv)
        Xstep = (Xmax - Xmin) / Xdiv
        Ystep = (Ymax - Ymin) / Ydiv

        geom_data = self.system_data.getGeometryData()
        node_vector = []

        for i in range(number_of_square_elements):
            # work like a typewriter, horizontally to the end, then back and up
            Xindex = i%Xdiv
            Yindex = (i - Xindex)/Xdiv

            #now determine nodes of 1st triangle element at current index
            x1 = Xindex*Xstep
            y1 = Yindex*Ystep
            z1 = 0.0

            x2 = (Xindex+1)*Xstep
            y2 = y1
            z2 = 0.0

            x3 = x1
            y3 = (Yindex+1)*Ystep
            z3 = 0.0

            n1 = [x1,y1,z1]
            n2 = [x2, y2, z2]
            n3 = [x3, y3, z3]
            node_vector.clear()
            node_vector.append(n1)
            node_vector.append(n2)
            node_vector.append(n3)

            geom_data.add_element('T3',node_vector,2*i + 1)

            # now determine nodes of 2nd triangle element at current index
            x1 = x2
            y1 = y2
            z1 = z2

            y2 = y3
            z2 = 0.0

            n1 = [x1, y1, z1]
            n2 = [x2, y2, z2]
            n3 = [x3, y3, z3]
            node_vector.clear()
            node_vector.append(n1)
            node_vector.append(n2)
            node_vector.append(n3)

            geom_data.add_element('T3', node_vector, 2 * i + 2)

        self.pygame_instance.draw()

    def _CreateMaterialEntryWindow(self):
        text_vector = []
        text_vector.append('Thickness')
        text_vector.append('Youngs modulus')
        text_vector.append('Poissons ratio')
        text_vector.append('Penalty factor p')
        self.input_variable_vector.clear()
        self.input_finalize_function = self.finalizeMaterialEntryWindow
        self.BasicGeometryEntryWindow = popup_window_form_2col.popup_2_col(4, text_vector, 'Enter elastic material data',
                                                                           self.input_variable_vector,
                                                                           self.input_finalize_function)
        return self.BasicGeometryEntryWindow

    def finalizeMaterialEntryWindow(self):
        constitutive_data_pointer = self.system_data.getConstitutiveData()
        t = float(self.input_variable_vector[0].get())
        E = float(self.input_variable_vector[1].get())
        nu = float(self.input_variable_vector[2].get())
        p = float(self.input_variable_vector[3].get())
        constitutive_data = {'thickness':t,'E':E, 'nu':nu,'p':p}
        constitutive_data_pointer.setConstitutiveProperties(constitutive_data)
        #constitutive_data_pointer.printData()