#coding=utf8

#################################################################
###                                                           ###
### Created by Bastien MARTY, 2017                            ###
###                                                           ###
### École polytechnique, Palaiseau, France                    ###
###                                                           ###
#################################################################

from vertice import vertice
from link import link
from newcoords import newcoords
import math

# Define the way of the contraction of a cell.
# We can choose the start, the rate ([0,1[), the duration and if we want a relaxation or keep the vertices fixed

def contractiondyn(
	cells,
	contractible_cells,
	contracting_cells,
	t,
	rate = 0.5,
	duration = 1,
	relaxation = 1,
	t_relaxation = 1):
	

	remove_cells = []
	for i in range(len(contractible_cells)):
		for j in range(len(contracting_cells)):
			if contractible_cells[i] == contracting_cells[j][0]:
				remove_cells.append(contractible_cells[i])

	for i in range(len(remove_cells)):
		contractible_cells.remove(remove_cells[i])

	for i in contractible_cells:
		contracting_cells.append([i,t])

	remove_cells = []
	for i in range(len(contracting_cells)):
		if contracting_cells[i][1] <= t < contracting_cells[i][1] + duration:
			cells[contracting_cells[i][0]].A_ac = rate*cells[contracting_cells[i][0]].A0
			# cells[contracting_cells[i][0]].K = 150
		else:
			cells[contracting_cells[i][0]].A_ac = cells[contracting_cells[i][0]].A0
			cells[contracting_cells[i][0]].K = 10
			remove_cells.append(contracting_cells[i])

	for i in range(len(remove_cells)):
		contracting_cells.remove(remove_cells[i])

	return contracting_cells