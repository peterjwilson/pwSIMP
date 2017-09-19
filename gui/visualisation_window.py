# Python imports
import tkinter as tk
from tkinter import messagebox
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import collections  as mc
from matplotlib.patches import Polygon
import seaborn as sp
import numpy as np


class visualisationWindow:
    def __init__(self, master_system_data, frame):
        self.system_data = master_system_data
        self.geom_data = master_system_data.getGeometryData()
        self.process_data = master_system_data.getProcessData()
        self.element_vector = self.geom_data.getElementVector()
        self.node_vector = self.geom_data.getNodeVector()
        self.my_frame = frame

        # Triangle config
        self.tri_size = 2

        # Arrow config
        self.arrow_size = 4

        self.plot_node_numbers = True

        sp.set()
        self.f = Figure()
        self.subPlot = self.f.add_subplot(111)
        self.axis_offset = 0.5

        self.subPlot.plot([])
        self.MatplotCanvas = FigureCanvasTkAgg(self.f, self.my_frame)
        self.MatplotCanvas.show()
        self.MatplotCanvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.MatplotToolbar = NavigationToolbar2TkAgg(self.MatplotCanvas, self.my_frame)
        self.MatplotToolbar.update()
        self.MatplotCanvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update(self):
        self.subPlot.cla()
        # plot entities
        if self.system_data.getDisplayNodes():
            self.plotNodes()
        #self.plotElements('black')
        self.plotProcesses()
        if self.system_data.getDisplacementsCalculatedBool():
            self.plotSIMPresults()
            #self.plotDisplacements('red')
        if self.system_data.getSIMPCalculatedBool():
            self.plotSIMPresults()


        # finalize and update
        plot_bounds = self.geom_data.getSystemExtremities()
        self.addPlotFat(plot_bounds, 30.0)
        self.subPlot.axis(plot_bounds)
        self.MatplotCanvas.show()
        self.MatplotToolbar.update()



    def setPlotNodeNumbers(self, boolean_in):
        self.plot_node_numbers = boolean_in

    def addPlotFat(self, plot_bounds, percentage_fat):
        xspan = plot_bounds[1] - plot_bounds[0]
        xhalf = xspan / 2.0
        xmid = plot_bounds[0] + xhalf

        yspan = plot_bounds[3] - plot_bounds[2]
        yhalf = yspan / 2.0
        ymid = plot_bounds[2] + yhalf

        multiplier = (100.0 + percentage_fat) / 100.0
        plot_bounds[0] = xmid - xhalf * multiplier
        plot_bounds[1] = xmid + xhalf * multiplier
        plot_bounds[2] = ymid - yhalf * multiplier
        plot_bounds[3] = ymid + yhalf * multiplier

    def plotNodes(self):
        node_x_positions = []
        node_y_positions = []
        for i in range(len(self.node_vector)):
            node_position = self.node_vector[i].getPositionVector2D()
            node_x_positions.append(node_position[0])
            node_y_positions.append(node_position[1])
        self.subPlot.plot(node_x_positions, node_y_positions, markeredgecolor='#77B5FE', linestyle='None',
                          linewidth=2.0,
                          markersize=7.0, marker='o', markeredgewidth=3.0, markerfacecolor='#77B5FE')

        if self.plot_node_numbers:
            for i in range(len(self.node_vector)):
                node_label = str(i + 1)
                self.subPlot.text(node_x_positions[i], node_y_positions[i], node_label, color='red')

    def plotElements(self,color_in,include_displacements=False):
        lines = []
        for i in range(len(self.element_vector)):
            element = self.element_vector[i]
            element_node_vector = element.getNodalVector()
            for j in range(len(element_node_vector)):
                n1number = int(element_node_vector[j])
                n2number = int(element_node_vector[(j + 1) % len(element_node_vector)])
                node1 = self.node_vector[n1number-1]
                node2 = self.node_vector[n2number-1]
                node1_position = node1.getPositionVector2D()
                node2_position = node2.getPositionVector2D()
                if include_displacements:
                    node1_disp = node1.getDisplacements()
                    node2_disp = node2.getDisplacements()
                    for k in range(2):
                        node1_position[k] += node1_disp[k]
                        node2_position[k] += node2_disp[k]
                lines.append([(node1_position[0], node1_position[1]), (node2_position[0], node2_position[1])])
        line_collection = mc.LineCollection(lines, colors=color_in, linewidths=3)
        self.subPlot.add_collection(line_collection)

    def plotProcesses(self):
        # start with dirichlet point process
        dirichlet_point = self.process_data.getDirichletPointProcessVector()
        for i in range(len(dirichlet_point)):
            dirichlet_info = dirichlet_point[i].getProcessInfo()
            node_index = dirichlet_info['node_number'] - 1
            node_position = self.node_vector[node_index].getPositionVector2D()
            disp_vector = dirichlet_info['disp_vector']
            # x disp
            if disp_vector[0] != None:
                self.drawTriangle(node_position, 'leftX','green')
            if disp_vector[1] != None:
                self.drawTriangle(node_position, 'upY','green')

        # now consider with neumann point process
        neumann_point = self.process_data.getNeumannPointProcessVector()
        for i in range(len(neumann_point)):
            neumann_info = neumann_point[i].getProcessInfo()
            node_index = neumann_info['node_number'] - 1
            node_position = self.node_vector[node_index].getPositionVector2D()
            force_vector = neumann_info['force_vector']
            # x disp
            if force_vector[0] != None:
                if force_vector[0] > 0:
                    self.drawArrow(node_position, 'leftX','red')
                if force_vector[0] < 0:
                    self.drawArrow(node_position, 'rightX','red')
            if force_vector[1] != None:
                if force_vector[1] < 0:
                    self.drawArrow(node_position, 'downY','red')
                if force_vector[1] > 0:
                    self.drawArrow(node_position, 'upY','red')

    def drawTriangle(self, main_point, direction, color_in):
        p2 = []
        p3 = []
        if direction == 'leftX':
            # draw triangle to the left of the main point
            x_offset = self.tri_size * np.cos(np.deg2rad(30))
            y_offset = self.tri_size / 2
            p2 = [main_point[0] - x_offset, main_point[1] + y_offset]
            p3 = [main_point[0] - x_offset, main_point[1] - y_offset]
        if direction == 'rightX':
            # draw triangle to the left of the main point
            x_offset = self.tri_size * np.cos(np.deg2rad(30))
            y_offset = self.tri_size / 2
            p2 = [main_point[0] + x_offset, main_point[1] + y_offset]
            p3 = [main_point[0] + x_offset, main_point[1] - y_offset]
        if direction == 'upY':
            # draw triangle below the main point
            x_offset = self.tri_size / 2
            y_offset = self.tri_size * np.cos(np.deg2rad(30))
            p2 = [main_point[0] - x_offset, main_point[1] - y_offset]
            p3 = [main_point[0] + x_offset, main_point[1] - y_offset]
        if direction == 'downY':
            # draw triangle above the main point
            x_offset = self.tri_size / 2
            y_offset = self.tri_size * np.cos(np.deg2rad(30))
            p2 = [main_point[0] - x_offset, main_point[1] + y_offset]
            p3 = [main_point[0] + x_offset, main_point[1] + y_offset]

        tri_points = np.array([(main_point[0], main_point[1]), (p2[0], p2[1]), (p3[0], p3[1])])
        tri = Polygon(tri_points, color = color_in)
        self.subPlot.add_patch(tri)

    def drawArrow(self,main_point,direction,color_in):
        p2 = []
        if direction == 'leftX':
            p2 = [main_point[0]-self.arrow_size, main_point[1]]
        elif direction == 'rightX':
            p2 = [main_point[0]+self.arrow_size, main_point[1]]
        elif direction == 'downY':
            p2 = [main_point[0], main_point[1]+self.arrow_size]
        elif direction == 'upY':
            p2 = [main_point[0], main_point[1]-self.arrow_size]

        #line_collection = mc.LineCollection(line, colors=color_in, linewidths=3)
        #self.subPlot.add_collection(line_collection)
        self.subPlot.plot([main_point[0],p2[0]], [main_point[1],p2[1]], color = color_in, linestyle='-',linewidth = 3)
        #now add an arrowhead
        self.drawTriangle(main_point,direction,color_in)

    def plotDisplacements(self,color_in):
        self.plotElements(color_in,True)

    def plotSIMPresults(self):
        for i in range(len(self.element_vector)):
            element = self.element_vector[i]
            element_node_vector = element.getNodalVector()
            square = []
            for j in range(len(element_node_vector)):
                n1number = int(element_node_vector[j])
                node1 = self.node_vector[n1number - 1]
                node1_position = node1.getPositionVector2D()
                square.append(node1_position)
            square = np.array(square)
            rho = element.getElementDensity()
            r = (1.0-rho)
            b = rho
            color_in = (r,r,r)
            my_square = Polygon(square, color=color_in)
            self.subPlot.add_patch(my_square)