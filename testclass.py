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
from newcoords import newcoords
from createnetwork import createnetwork
from INP_Circle_returnverticesandpolygons import INP_Circle_returnverticesandpolygons #use for quadrangle network
from INP_Circle_ReturnVerticesForVoronoi import INP_Circle_ReturnVerticesForVoronoi
from get_neighbors_links import get_neighbors_links
from get_neighbors_cells import get_neighbors_cells
from plot_network import plot_network
from contraction import contraction
from contractiondyn import contractiondyn
from csvfloat import csvfloat
from query_yes_no import query_yes_no

import sys
import os
import math
import csv
import networkx as nx
import shutil
from matplotlib import pyplot as plt

### The different vertices are updated dynamically, when we update the coordinates of a vertice it will
### automatically update the coordinates of that vertice inside the cells and links.

### We cannot change the stiffness here => see link class and cell class
### If we increase the stiffness we have to reduce dt => stability problem
### The gamma is not really important right now (just a factor in front of the overall stiffness). Can be important
### if we implement more complex links.

T = 10.   # end time
dt = 0.01
gamma = 0.02
areathreshold = 1.05
rate = 0
# Index of the contracted cell
no = '?'
nbrsnap = 200
Tsnap = round(T*1000/nbrsnap)

# Name of the INP file (output of GMSH) that we use to create the Voronoi net
mesh_basename = "Circle_triangle"
# Folder name to save the plots
folder_basename = "6 pull left and right K=10 Kafter10 rate = "+str(rate)+" area threshold = "+str(areathreshold)+"A2 = A0 k20 relax lo "+str(T)+"s "+str(dt)+"dt gamma"+str(gamma)+" cell n"+str(no)

if os.path.exists(folder_basename) == True:
	A = query_yes_no("The folder already exists. Do you want to overwrite it ?")
	if A == 1:
		shutil.rmtree(folder_basename)
		os.mkdir(folder_basename)
	else :
		sys.exit("Program stopped")
else :
	os.mkdir(folder_basename)


# Creation of CSV file for easy use of results with Excel
f_coords = open(folder_basename+"/coordsexcel.csv","w")
f_forces = open(folder_basename+"/forcesexcel.csv","w")
f_areas = open(folder_basename+"/areaexcel.csv","w")
w_coords = csv.writer(f_coords, delimiter=";")
w_forces = csv.writer(f_forces, delimiter=";")
w_areas = csv.writer(f_areas, delimiter=";")

# Creation of CSV file for data post processing using Numpy
fn_coords = open(folder_basename+"/coordsnumpy.csv","w")
fn_forces = open(folder_basename+"/forcesnumpy.csv","w")
fn_areas = open(folder_basename+"/areasnumpy.csv","w")
wn_coords = csv.writer(fn_coords, delimiter=",")
wn_forces = csv.writer(fn_forces, delimiter=",")
wn_areas = csv.writer(fn_areas, delimiter=",")

# Creation of the Voronoi Network return the vertices and polygons (each polygons contains the n°
# of the different vertices)
[points, polygons] = INP_Circle_ReturnVerticesForVoronoi(
	mesh_filename = mesh_basename+".inp")

# Creation of the real vertices, cells and links
[vertices, links, cells] = createnetwork(points, polygons)
# for i in range(len(vertices)):
# 	if vertices[i].boundary == True:
# 		vertices[i].state = "fixed"

# For all vertices find the links attached to it (neighbors)
neighborslink = []
neighborscell = []
for i in range(len(vertices)) :
	neighborslink.append(get_neighbors_links(vertices[i], cells))
	neighborscell.append(get_neighbors_cells(vertices[i], cells))

#### find the neighbors of the center of the contraction
# neighborscontraction = [no]
# for i in range(len(cells)):
# 	for j in range(len(cells[no].vertices)):
# 		if cells[no].vertices[j] in cells[i].vertices and i not in neighborscontraction :
# 			neighborscontraction.append(i)

# #### find the cell on a line
# linecontraction = [no]
# xline = cells[no].bary()[0]
# yline = cells[no].bary()[1]
# for i in range(len(cells)):
# 	left = False
# 	right = False
# 	for j in range(len(cells[i].vertices)):
# 		if cells[i].vertices[j].coordx < xline and cells[i].vertices[j].coordy > yline:
# 			left = True
# 		if cells[i].vertices[j].coordx > xline and cells[i].vertices[j].coordx > yline:
# 			right = True
# 	if left == True and right == True:
# 		linecontraction.append(i)


# sys.exit("Stop here")

t = 0.
t2 = 0.

# Initialization of the CSV file
writing = ['t (ms)']
for i in range(len(vertices)):
	writing.append("x"+str(i))
	writing.append("y"+str(i))
w_coords.writerow(writing)
wn_coords.writerow(writing)
writing = ['t (ms)']
for i in range(len(vertices)):
	writing.append("Fx"+str(i))
	writing.append("Fy"+str(i))
w_forces.writerow(writing)
wn_forces.writerow(writing)
writing = ['t (ms)']
for i in range(len(cells)):
	writing.append("A"+str(i))
w_areas.writerow(writing)
wn_areas.writerow(writing)

# Plot initial network
plot_network(vertices,links,cells,0000,folder_basename)

# Writing of the initial network in CSV file
writing = [0]
writing_n = [0]
for i in range(len(vertices)):
	writing.append(csvfloat(vertices[i].coordx))
	writing.append(csvfloat(vertices[i].coordy))
	writing_n.append(float(vertices[i].coordx))
	writing_n.append(float(vertices[i].coordy))
w_coords.writerow(writing)
wn_coords.writerow(writing_n)
writing = [0]
for i in range(len(vertices)):
	writing.append(0)
	writing.append(0)
w_forces.writerow(writing)
wn_forces.writerow(writing)
writing = [0]
writing_n = [0]
for i in range(len(cells)):
	writing.append(csvfloat(cells[i].area()))
	writing_n.append(float(cells[i].area()))
w_areas.writerow(writing)
wn_areas.writerow(writing_n)

# Initial conditions :
########### 1
# We contract a cell and keep it's vertices fixed

# bary = cells[no].bary()
# for i in range(len(cells[no].vertices)) :
# 	newcoords(cells[no].vertices[i], [(cells[no].vertices[i].coordx+bary[0])/2, (cells[no].vertices[i].coordy+bary[1])/2])
# 	cells[no].vertices[i].state = "fixed"

########### 2
# We change the stiffness to have to section, one with an higher stiffness than the other and contraction at the bottom
# Change in the Area Stiffness

# for i in range(len(cells)):
# 	if cells[i].bary()[0] > 25.:
# 		cells[i].K = 5*cells[i].K
# 	if 26 > cells[i].bary()[0] > 25 and cells[i].bary()[1] < 17 :
# 		no = i

########### 3
# We want to pull the organism on the left and right side 
pullleft = []
pullright = []
for i in range(len(vertices)):
	if vertices[i].coordx < 17 and vertices[i].boundary == True and 26.5 > vertices[i].coordy > 23.5:
		pullleft.append(i)
	if vertices[i].coordx > 33 and vertices[i].boundary == True and 26.5 > vertices[i].coordy > 23.5:
		pullright.append(i)


#Plot modified network
plot_network(vertices,links,cells,00,folder_basename)
writing = [00]
for i in range(len(vertices)):
	writing.append(csvfloat(vertices[i].coordx))
	writing.append(csvfloat(vertices[i].coordy))
w_coords.writerow(writing)
writing = [00]
for i in range(len(vertices)):
	writing.append(float(vertices[i].coordx))
	writing.append(float(vertices[i].coordy))
wn_coords.writerow(writing)

contracting_cells = []
# Time loop
while t < T :
	x_new = []
	y_new = []
	coordsexcel_t = []
	forcesexcel_t = []
	areasexcel_t = []
	coordsnumpy_t = []
	forcesnumpy_t = []
	areasnumpy_t = []
	elastic_energy_t = []


	contractible_cells = []
	for i in range(len(cells)):
		areasexcel_t.append(csvfloat(cells[i].area()))
		areasnumpy_t.append(float(cells[i].area()))
		if cells[i].area() > cells[i].A0 * areathreshold and cells[i].boundary == False:
			contractible_cells.append(i)

	###################
	# initial contraction
	# if t2 == 100:
	# 	contractible_cells.append(no)
		
	# pull left and right
	if len(contractible_cells) == 0:
		for i in pullleft:
			newcoords(vertices[i], [vertices[i].coordx-0.1, vertices[i].coordy])
		for i in pullright:
			newcoords(vertices[i], [vertices[i].coordx+0.1, vertices[i].coordy])


	###################
	# We choose which cell we want to contract and when
	contracting_cells = contractiondyn(cells, contractible_cells, contracting_cells, t, relaxation = 1, rate = rate)

	# Calculate the forces and the new coordinates of all the vertices
	for i in range(len(vertices)):
		Fx = 0.
		Fy = 0.
		for j in range(len(neighborslink[i])):
			Fx += neighborslink[i][j].get_force(vertices[i])[0]
			Fy += neighborslink[i][j].get_force(vertices[i])[1]
		for j in range(len(neighborscell[i])):
			Fx += neighborscell[i][j].get_force(vertices[i])[0]
			Fy += neighborscell[i][j].get_force(vertices[i])[1]

		x_new.append(vertices[i].coordx + dt * 1/2 * gamma * Fx)
		y_new.append(vertices[i].coordy + dt * 1/2 * gamma * Fy)

		# Storage of the data
		forcesexcel_t.append(csvfloat(Fx))
		forcesexcel_t.append(csvfloat(Fy))
		coordsexcel_t.append(csvfloat(vertices[i].coordx))
		coordsexcel_t.append(csvfloat(vertices[i].coordy))

		forcesnumpy_t.append(float(Fx))
		forcesnumpy_t.append(float(Fy))
		coordsnumpy_t.append(float(vertices[i].coordx))
		coordsnumpy_t.append(float(vertices[i].coordy))



	# Update all the vertices
	for i in range(len(vertices)):
		newcoords(vertices[i], [x_new[i], y_new[i]])

	# Calcul of the elastic_energy, NOT USE RIGHT NOW
	#for i in range(len(links)):
	#	l = math.hypot(links[i].vertices[1].coordx-links[i].vertices[0].coordx, links[i].vertices[1].coordy-links[i].vertices[0].coordy)
	#	elastic_energy_t.append(float(1/2*links[i].k*(links[i].l_0-l)**2+1/2*links[i].k_ac*(links[i].l_ac-l)**2))
	
	# Update time	
	t += dt
	t2 = round(t*1000)   #time in ms
	
	# Plot network at time t
	if t2%Tsnap == 0 :
		plot_network(vertices,links,cells,t2,folder_basename)
	
	# Writing data in CSV file
	coordsexcel_t.insert(0, t2)
	w_coords.writerow(coordsexcel_t)
	forcesexcel_t.insert(0, t2)
	w_forces.writerow(forcesexcel_t)
	areasexcel_t.insert(0, t2)
	w_areas.writerow(areasexcel_t)

	coordsnumpy_t.insert(0, t2)
	wn_coords.writerow(coordsnumpy_t)
	forcesnumpy_t.insert(0, t2)
	wn_forces.writerow(forcesnumpy_t)
	areasnumpy_t.insert(0, t2)
	wn_areas.writerow(areasnumpy_t)


	print("t = "+str(t2)+"ms")


f_coords.close()
f_forces.close()