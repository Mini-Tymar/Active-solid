#coding=utf8

#################################################################
###                                                           ###
### Created by Bastien MARTY, 2017                            ###
###                                                           ###
### École polytechnique, Palaiseau, France                    ###
###                                                           ###
#################################################################

import csv
import numpy as np
import matplotlib.pyplot as plt
import math


folder_basename = ""
no = 203
neighborscellsno = [201,202,205,348,349]
linecellsno = [36, 37, 64, 90, 113, 114, 146, 149, 150, 163, 165, 169, 170, 202, 203, 239, 240, 243, 353, 356, 357]

f_coords = open(folder_basename+"coordsnumpy.csv","r")
r_coords = csv.reader(f_coords, delimiter=",")
f_areas = open(folder_basename+"areasnumpy.csv","r")
r_areas = csv.reader(f_areas, delimiter=",")

data_file = open(folder_basename+"area"+str(no)+"andneighbors.dat","w")


rows_coords = []
for row in r_coords:
	rows_coords.append(row)

rows_areas = []
for row in r_areas:
	rows_areas.append(row)

coords = []
time = []
areas = []
areaschangerate = []
areasnormalized = []
for i in range(1,len(rows_coords)):
	time.append(float(rows_coords[i][0]))	
	coordsi = []
	for j in range(1,len(rows_coords[i])):
		coordsi.append(float(rows_coords[i][j]))
	coords.append(coordsi)
for i in range(1,len(rows_areas)):
	area_i = []
	areaschangerate_i = []
	areasnormalized_i = []
	for j in range(1,len(rows_areas[i])):
		area_i.append(float(rows_areas[i][j]))
		areasnormalized_i.append(float(rows_areas[i][j])/float(rows_areas[1][j]))
		if i != 1:
			areaschangerate_i.append((float(rows_areas[i][j])-float(rows_areas[i-1][j]))/(float(time[i-1])-float(time[i-2])))
		else :
			areaschangerate_i.append(0.0)
	areas.append(area_i)
	areaschangerate.append(areaschangerate_i)
	areasnormalized.append(areasnormalized_i)


# for i in range(len(time)):
# 	data_file.write(str(time[i])+" "+str(areasnormalized[i][no])+" "+"".join([str(areasnormalized[i][n])+" " for n in linecellsno])+"\n")
# 	data_file.flush()

for i in range(len(time)):
	data_file.write(str(time[i])+" "+str(areasnormalized[i][no])+" "+"".join([str(areasnormalized[i][n])+" " for n in neighborscellsno])+"\n")
	data_file.flush()

data_file.close()
################### AREA ON A LINE



# time = np.array(time)
# coords = np.array(coords)
# areas = np.array(areas)
# nbr_timestep = len(time)
# nbr_vertices = int(len(coords[0])/2)
# coordsx = np.zeros((nbr_timestep, nbr_vertices))
# coordsy = np.zeros((nbr_timestep, nbr_vertices))
# displacementx = np.zeros((nbr_timestep, nbr_vertices))
# displacementy = np.zeros((nbr_timestep, nbr_vertices))

# for i in range(nbr_timestep):
# 	for j in range(nbr_vertices):
# 		displacementx[i][j] = coords[0][2*j]-coords[i][2*j]
# 		displacementy[i][j] = coords[0][2*j+1]-coords[i][2*j+1]
# 		coordsx[i][j] = coords[i][2*j]
# 		coordsy[i][j] = coords[i][2*j+1]




# displacementnorm = (displacementx**2+displacementy**2)**0.5

# #plt.axis('equal')
# #plt.scatter(coordsx[0],coordsy[0],c=displacementnorm[50])
# #plt.show()


# averagedis = (np.sum(displacementnorm, axis = 0)/nbr_timestep)
# maxdis = (np.max(displacementnorm, axis =0))
# maximum = (np.max(maxdis))
# dis_ten = []
# index_max = np.where(displacementnorm == maximum)[1][0]


# for i in range(nbr_vertices):
# 	if (np.max(displacementnorm, axis =0))[i] >= maximum/10:
# 		dis_ten.append(i)

# length = []
# for i in range(len(dis_ten)):
# 	length.append(math.hypot(coordsx[0][index_max]-coordsx[0][dis_ten[i]], coordsy[0][index_max]-coordsy[0][dis_ten[i]]))





