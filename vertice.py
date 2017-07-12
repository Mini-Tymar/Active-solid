#coding=utf8

#################################################################
###                                                           ###
### Created by Bastien MARTY, 2017                            ###
###                                                           ###
### École polytechnique, Palaiseau, France                    ###
###                                                           ###
#################################################################

## Represent all the vertices in the network.

class vertice:

	# Initialization of the vertice during the cration of the network
	def __init__(self,_n:int,coords:[float,float]):
		self._n = _n
		self.coords = coords
		self.coordx = coords[0]
		self.coordy = coords[1]
		self.state = "free"  # Allow us or not to change the coords
		self.initialcoords = coords # Store the initial coordinates
		self.boundary = False

	# # Define if the vertice is on the boundary or not (cannot be changed dynamically)
	# @property
	# def boundary(self):
	# 	return self._boundary

	# Unique n°
	@property
	def n(self):
		return self._n

	# New print function
	def __repr__(self):
		return "vertice : n({}), coords({}), boundary({})".format(
			self.n, self.coords, self.boundary)

	# New equality function
	def __eq__(self, other):
		return (self.n == other.n and self.coords == other.coords)