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
from scipy.spatial import ConvexHull

## Creation of the initial network using the points and polygons given by the Voronoi network

def createnetwork(points, polygons):

	#points : array with all the coordinates of the vertices
	#polygons : array with n-integer-array for each cell that 
	#represent the numero of the vertices that are in this cell

	vertices = []
	links = []
	cells = []

	# Find the boundary vertices
	boundary = ConvexHull(points)

	#Creation of the vertices with the argument 1 for boundary and 0 for bulk
	for i in range(len(points)):
		if i in boundary.vertices:
			vertices.append(vertice(i, points[i], 1))
		else :
			vertices.append(vertice(i, points[i], 0))

	#Creation of the cells and adding the vertices
	for i in range(len(polygons)):
		cells.append(cell(i))
		for j in range(len(polygons[i])):
			cells[i].add_vertice(vertices[polygons[i][j]])
		cells[i].orderingvertices()

	#Creation of the links and adding to the cells.
	for i in range(len(cells)):
		for j in range(len(cells[i].vertices)):
			if j != len(cells[i].vertices)-1:
				link_0 = link([cells[i].vertices[j], cells[i].vertices[j+1]], "membrane")
				cells[i].add_link(link_0)
			else:
				link_0 = link([cells[i].vertices[j], cells[i].vertices[0]], "membrane")
				cells[i].add_link(link_0)

			if link_0 not in links:
				links.append(link_0)


		for j in range(len(cells[i].vertices)):
			if j == 0:
				for k in range(2,len(cells[i].vertices)-1):
					link_0 = link([cells[i].vertices[j], cells[i].vertices[k]], "inside")
					cells[i].add_link(link_0)
					links.append(link_0)
			else:
				for k in range(j+2,len(cells[i].vertices)):
					link_0 = link([cells[i].vertices[j], cells[i].vertices[k]], "inside")
					cells[i].add_link(link_0)
					links.append(link_0)


	return [vertices, links, cells]