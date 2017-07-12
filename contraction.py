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

def contraction(
	cell,
	t,
	t_start = 0,
	rate = 0.5,
	duration = 1,
	relaxation = 1,
	t_relaxation = 1):
	
	if t_relaxation >= t_start + duration :
		t_relax = t_relaxation
	else :
		t_relax = t_start + duration

	s = rate/duration*(t-t_start)

	if t_start <= t < t_start + duration:
		for i in range(len(cell.vertices)) :
			cell.vertices[i].state = "free"
			newcoords(cell.vertices[i], [(1-s)*cell.vertices[i].initialcoords[0]+s*cell.bary()[0],
				(1-s)*cell.vertices[i].initialcoords[1]+s*cell.bary()[1]])
			cell.vertices[i].state = "fixed"
	else:
		if t >= t_relax:
			if relaxation == 1 :
				for i in range(len(cell.vertices)):
					cell.vertices[i].state = "free"
				