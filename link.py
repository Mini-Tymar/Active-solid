#coding=utf8

#################################################################
###                                                           ###
### Created by Bastien MARTY, 2017                            ###
###                                                           ###
### École polytechnique, Palaiseau, France                    ###
###                                                           ###
#################################################################
from vertice import vertice
import math

## The links are the springs between all the vertices, there are to types
## the one which are inside the cell and the one which are on the membrane.
##
## We will implement the different kind of forces and integrator here.
##
## We can only choose the stiffness HERE

class link:

	# Initialization during creation of the network
	def __init__(self,vertices:[vertice, vertice]):
		self.vertices = vertices
		# Initial lenght
		self.l_0 = math.hypot(vertices[1].coordx-vertices[0].coordx, vertices[1].coordy-vertices[0].coordy)
		self.l_ac = self.l_0
		# Stiffness 
		self.k = 20.
		self.k_ac = 0.

	# New print function
	def __repr__(self):
		return "link: vertices({}), k({}), l_0({})".format(
			self.vertices, self.k, self.l_0)

	# New equality function
	def __eq__(self, other):
		return(self.vertices == other.vertices or self.vertices == [other.vertices[1], other.vertices[0]])

	# Give the force done by the link on the given vertice
	# Force : F = k(l(t)-l_0)) + k_ac(l(t)-l_ac)
	def get_force(self, vertice):
		check = (vertice == self.vertices[0]) # check if the vertice is the 1st or 2nd
		if vertice not in self.vertices:
			print("Error the link is not attached to this vertice")
		else :
			# sometimes the check is a list of booleans I don't know why
			if type(check) == bool:
				if vertice == self.vertices[0]:
					A = vertice
					B = self.vertices[1]
				else :
					A = vertice
					B = self.vertices[0]
			else:
				if all(vertice == self.vertices[0]):
					A = vertice
					B = self.vertices[1]
				else :
					A = vertice
					B = self.vertices[0]
			ABx = B.coordx - A.coordx
			ABy = B.coordy - A.coordy
			# Calcul of the forces : very simple spring
			theta = math.atan2(ABy, ABx) # Give the angle in [0, 2Pi[
			Fx = math.cos(theta)*((self.k +self.k_ac)*math.hypot(ABx, ABy)-self.k*self.l_0 - self.k_ac*self.l_ac)
			Fy = math.sin(theta)*((self.k +self.k_ac)*math.hypot(ABx, ABy)-self.k*self.l_0 - self.k_ac*self.l_ac)

		return [Fx, Fy]