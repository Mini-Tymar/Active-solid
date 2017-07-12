#coding=utf8

#################################################################
###                                                           ###
### Created by Bastien MARTY, 2017                            ###
###                                                           ###
### École polytechnique, Palaiseau, France                    ###
###                                                           ###
#################################################################
from vertice import vertice

## Special way to define the new coords af a vertice, allow us to fix some and let free others

def newcoords(
	vertice,
	newcoords:[float,float]):

	if vertice.state == "free":
		vertice.coords = newcoords
		vertice.coordx = newcoords[0]
		vertice.coordy = newcoords[1]
	#else:
		#print("Coordinates not changed ! The coordinates of the vertice "+str(vertice.n)+" are fixed and are: "+str(vertice.coords))
