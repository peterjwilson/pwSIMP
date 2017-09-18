# Python imports
import tkinter as tk
from tkinter import messagebox
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import collections  as mc
import seaborn as sp
import numpy as np


class visualisationWindow:
    def __init__(self,master_system_data,frame):
        self.system_data = master_system_data
        self.geom_data = master_system_data.getGeometryData()
        self.element_vector = self.geom_data.getElementVector()
        self.node_vector = self.geom_data.getNodeVector()
        self.my_frame = frame

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
        # plot entities
        self.plotNodes()
        self.plotElements()

        # finalize and update
        plot_bounds = self.geom_data.getSystemExtremities()
        self.addPlotFat(plot_bounds,20.0)
        self.subPlot.axis(plot_bounds)
        self.MatplotCanvas.show()
        self.MatplotToolbar.update()

    def setPlotNodeNumbers(self,boolean_in):
        self.plot_node_numbers = boolean_in



    def addPlotFat(self,plot_bounds,percentage_fat):
        xspan = plot_bounds[1] - plot_bounds[0]
        xhalf = xspan/2.0
        xmid = plot_bounds[0] + xhalf

        yspan = plot_bounds[3] - plot_bounds[2]
        yhalf = yspan/2.0
        ymid = plot_bounds[2] + yhalf

        multiplier = (100.0+percentage_fat)/100.0
        plot_bounds[0] = xmid - xhalf*multiplier
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
        self.subPlot.plot(node_x_positions, node_y_positions, markeredgecolor = '#77B5FE', linestyle='None',linewidth=2.0,
             markersize = 7.0, marker='o', markeredgewidth = 3.0, markerfacecolor= '#77B5FE')

        if self.plot_node_numbers:
            for i in range(len(self.node_vector)):
                node_label = str(i + 1)
                self.subPlot.text(node_x_positions[i], node_y_positions[i],node_label,color='red')

    def plotElements(self):
        lines = []
        for i in range(len(self.element_vector)):
            element = self.element_vector[i]
            element_node_vector = element.getNodalVector()
            for j in range(len(element_node_vector)):
                n1 = element_node_vector[j]
                n2 = element_node_vector[(j+1)%len(element_node_vector)]
                node1_position = n1.getPositionVector2D()
                node2_position = n2.getPositionVector2D()
                lines.append([(node1_position[0],node1_position[1]),(node2_position[0],node2_position[1])])
        #line = [node1_position,node2_position]
        line_collection = mc.LineCollection(lines, colors='grey', linewidths=3)
        self.subPlot.add_collection(line_collection)
        #self.subPlot.plot(node1_position, node2_position, color = 'grey', linestyle='-',linewidth=3.0, marker='None')
        #self.MatplotCanvas.show()