#coding=utf8

#################################################################
###                                                           ###
### Created by Bastien MARTY, 2017                            ###
###                                                           ###
### École polytechnique, Palaiseau, France                    ###
###                                                           ###
#################################################################

## Represents all the differents cells in the network they can have an infinite
## number of vertices and links.
##
## There is a force applied on the vertices due to the change of the cell area


from vertice import vertice
from link import link
from newcoords import newcoords
import math

class cell:

	# Initialization during creation of the network
	def __init__(self, _n:int):
		self._n = _n
		self.vertices = []
		self.links = []
		self.A0 = 0.
		self.A_ac = 0.
		self.K = 0.
		self.boundary = False

	# Unique n°
	@property
	def n(self):
		return self._n

	# Add a vertice to the list of vertices
	def add_vertice(self, vertice:vertice):
		self.vertices.append(vertice)

	# Add a link to the list of links
	def add_link(self, link:link):
		self.links.append(link)

	# New print function
	def __repr__(self):
		return "cell: n({}), vertices({}), links({})".format(
			self.n, self.vertices, self.links)

	# Give the barycenter of the cell
	def bary(self):
		N = len(self.vertices)
		baryx = 0.
		baryy = 0.
		for i in range(N):
			baryx += self.vertices[i].coordx
			baryy += self.vertices[i].coordy
		return [1/N*baryx, 1/N*baryy]

	# Order the vertices : using the barycenter and in a trigonometric way
	def orderingvertices(self):
		orderedvertices = self.vertices
		bary = self.bary()
		thetas = []
		for i in range(len(self.vertices)):
			thetas.append(0.)

		# Calculation of all the angles (can be easier with atan2)
		for i in range(len(thetas)):
			if math.asin((orderedvertices[i].coordy - bary[1])/(((orderedvertices[i].coordx -bary[0])**2 + (orderedvertices[i].coordy -bary[1])**2)**0.5)) > 0:
				epsilon = 0
			else:
				epsilon = 2*math.pi
			thetas[i] = abs(epsilon - math.acos((orderedvertices[i].coordx - bary[0])/(((orderedvertices[i].coordx -bary[0])**2 + (orderedvertices[i].coordy -bary[1])**2)**0.5)))
		
		# Order the vertices by increasing angle
		for i in range(len(thetas)):
			test = thetas[i]
			test2 = orderedvertices[i]
			j = i-1
			while j >= 0 and thetas[j] > test:
				thetas[j+1] = thetas[j]
				orderedvertices[j+1] = orderedvertices[j]
				j = j-1
			thetas[j+1] = test
			orderedvertices[j+1] = test2

		self.vertices = orderedvertices


	# Calculation of the are of the cells using a simple formula :
	# A = 1/2 * SUM(i in len(vertices)) (r_i ^ r_i+1).e_z
	# with the last term : r_n ^ r_1,    ^ is the vector product  and . the scalar product
	# and r_i = vector position of the vertice i and e_z an unit vector orthogonal to the cell.
	# I don't know if this formula works for non convex cells. With a simple sketch we can assume it works.
	def area(self):
		self.orderingvertices()
		A_2 = 0.
		for i in range(len(self.vertices)):
			if i != len(self.vertices)-1:
				A_2 = A_2 + (self.vertices[i].coordx*self.vertices[i+1].coordy - self.vertices[i].coordy*self.vertices[i+1].coordx)
			else:
				A_2 = A_2 + (self.vertices[i].coordx*self.vertices[0].coordy - self.vertices[i].coordy*self.vertices[0].coordx)

		return 0.5*A_2

	# Give the force done by the cell on the vertices
	# Force : F = K(A(t)-A_0)
	def get_force(self, vertice):
		if vertice not in self.vertices:
			print("Error the vertice is not in this cell")
		else :
			A = vertice
			B = self.bary()
			ABx = B[0] - A.coordx
			ABy = B[1] - A.coordy
			theta = math.atan2(ABy,ABx)
			#Fx = math.cos(theta)*(math.hypot(ABx,ABy))**3*(self.K*(self.area()-self.A0))
			#Fx = math.sin(theta)*(math.hypot(ABx,ABy))**3*(self.K*(self.area()-self.A0))
			Fx = math.cos(theta)*(self.K*(self.area()-self.A_ac))
			Fy = math.sin(theta)*(self.K*(self.area()-self.A_ac))

		return [Fx, Fy]

