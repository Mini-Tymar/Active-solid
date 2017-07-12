#coding=utf8

#################################################################
###                                                           ###
### Created by Bastien MARTY, 2017                            ###
###                                                           ###
### École polytechnique, Palaiseau, France                    ###
###                                                           ###
#################################################################

from link import link
from vertice import vertice
from cell import cell

import numpy as np
import math

import networkx as nx
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import colors
def plot_network(
	vertices,
	links,
	cells,
	t,
	folder_basename):

	fig, ax = plt.subplots()
	patches = []
	color2 = []

	cdict1 = {
		'red':	((0.00, 0.00, 0.00),
				 (0.05, 0.00, 0.00),
				 (0.10, 0.00, 0.00),
				 (0.15, 0.00, 0.00),
				 (0.20, 0.00, 0.00),
				 (0.25, 0.00, 0.00),
				 (0.30, 0.04, 0.04),
				 (0.35, 0.16, 0.16),
				 (0.40, 0.36, 0.36),
				 (0.45, 0.64, 0.64),
				 (0.50, 1.00, 1.00),
				 (0.55, 1.00, 1.00),
				 (0.60, 1.00, 1.00),
				 (0.65, 1.00, 1.00),
				 (0.70, 1.00, 1.00),
				 (0.75, 1.00, 1.00),
				 (0.80, 0.98, 0.98),
				 (0.85, 0.92, 0.92),
				 (0.90, 0.82, 0.82),
				 (0.95, 0.68, 0.68),
				 (1.00, 0.50, 0.50)),

		'green':((0.00, 0.00, 0.00),
				 (0.05, 0.01, 0.01),
				 (0.10, 0.04, 0.04),
				 (0.15, 0.09, 0.09),
				 (0.20, 0.16, 0.16),
				 (0.25, 0.25, 0.25),
				 (0.30, 0.36, 0.36),
				 (0.35, 0.49, 0.49),
				 (0.40, 0.64, 0.64),
				 (0.45, 0.81, 0.81),
				 (0.50, 1.00, 1.00),
				 (0.55, 0.64, 0.64),
				 (0.60, 0.36, 0.36),
				 (0.65, 0.16, 0.16),
				 (0.70, 0.04, 0.04),
				 (0.75, 0.00, 0.00),
				 (0.80, 0.00, 0.00),
				 (0.85, 0.00, 0.00),
				 (0.90, 0.00, 0.00),
				 (0.95, 0.00, 0.00),
				 (1.00, 0.00, 0.00)),

		'blue':	((0.00, 0.50, 0.50),
				 (0.05, 0.68, 0.68),
				 (0.10, 0.82, 0.82),
				 (0.15, 0.92, 0.92),
				 (0.20, 0.98, 0.98),
				 (0.25, 1.00, 1.00),
				 (0.30, 1.00, 1.00),
				 (0.35, 1.00, 1.00),
				 (0.40, 1.00, 1.00),
				 (0.45, 1.00, 1.00),
				 (0.50, 1.00, 1.00),
				 (0.55, 0.64, 0.64),
				 (0.60, 0.36, 0.36),
				 (0.65, 0.16, 0.16),
				 (0.70, 0.04, 0.04),
				 (0.75, 0.00, 0.00),
				 (0.80, 0.00, 0.00),
				 (0.85, 0.00, 0.00),
				 (0.90, 0.00, 0.00),
				 (0.95, 0.00, 0.00),
				 (1.00, 0.00, 0.00))
			}
	
	customcolormap = LinearSegmentedColormap('CustomColorMap', cdict1)
	# seismic = plt.get_cmap('seismic') 
	cNorm  = colors.Normalize(vmin=50, vmax=150)
	# scalarMap = cmx.ScalarMappable(norm = cNorm, cmap=seismic)
	# print(scalarMap.get_clim())
	for i in range(len(cells)):
		coordsver = np.zeros((len(cells[i].vertices),2))
		for j in range(len(cells[i].vertices)):
			coordsver[j,0] = cells[i].vertices[j].coordx
			coordsver[j,1] = cells[i].vertices[j].coordy
		color = cells[i].area()/cells[i].A0*100
		color2.append(color)
		patches.append(Polygon(coordsver, True))

	p = PatchCollection(patches, cmap = customcolormap, norm = cNorm , edgecolors = 'black', linewidths = (0.5,))
	p.set_array(np.array(color2))

	ax.add_collection(p)

	plt.axis('equal')
	cbar = plt.colorbar(p)
	cbar.set_label('A/A0 (%)')
	# cbar.ax.set_yticklabels([str(0.),str(modif(0.1)),str(modif(0.2)),str(modif(0.3)),str(modif(0.4)),str(modif(0.5)),str(modif(0.6)),str(modif(0.7)),str(modif(0.8)),str(modif(0.9)), str(1.)])
	plt.savefig(folder_basename+"/test1_"+'{0:04}'.format(t)+".png", dpi = 100)
	plt.clf()