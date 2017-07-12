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

# Give all the links attached to a vertice

def get_neighbors_cells(vertice, cells):

	neighbors = []

	# Go through all the cells and find all the links attached to the vertice
	for i in range(len(cells)) :
		if vertice in cells[i].vertices :
			neighbors.append(cells[i])

	# Remove the links in double
	i = 0
	while i < len(neighbors) :
		if neighbors[i] in neighbors[0:i] :
			neighbors.remove(neighbors[i])
		else:
			i += 1

	return neighbors
