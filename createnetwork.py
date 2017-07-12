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
## Creation of the initial network using the points and polygons given by the Voronoi network

def createnetwork(points, polygons):

	#points : array with all the coordinates of the vertices
	#polygons : array with n-integer-array for each cell that 
	#represent the numero of the vertices that are in this cell

	vertices = []
	links = []
	cells = []

	#Creation of the vertices with the argument 1 for boundary and 0 for bulk
	for i in range(len(points)):
		vertices.append(vertice(i, points[i]))
	#Creation of the cells and adding the vertices
	for i in range(len(polygons)):
		cells.append(cell(i))
		for j in range(len(polygons[i])):
			cells[i].add_vertice(vertices[polygons[i][j]])
		cells[i].orderingvertices()
		cells[i].A0 = cells[i].area()
		cells[i].A_ac = cells[i].A0
		cells[i].K = 10.

	# Finding the vertices on the boundary
	count = np.zeros(len(vertices))
	for i in range(len(cells)):
		for j in range(len(cells[i].vertices)):
			count[cells[i].vertices[j].n] += 1

	for i in range(len(count)):
		if count[i] < 3:
			vertices[i].boundary = True

	for i in range(len(cells)):
		for j in range(len(cells[i].vertices)):
			if cells[i].vertices[j].boundary == True:
				cells[i].boundary = True
			
	#Creation of the links and adding to the cells.
	for i in range(len(cells)):
		for j in range(len(cells[i].vertices)):
			if j != len(cells[i].vertices)-1:
				link_0 = link([cells[i].vertices[j], cells[i].vertices[j+1]])
				cells[i].add_link(link_0)
			else:
				link_0 = link([cells[i].vertices[j], cells[i].vertices[0]])
				cells[i].add_link(link_0)

			if link_0 not in links:
				links.append(link_0)

	return [vertices, links, cells]