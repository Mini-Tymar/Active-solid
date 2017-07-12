#coding=utf8

#################################################################
###                                                           ###
### Created by Bastien MARTY, 2017                            ###
###                                                           ###
### École polytechnique, Palaiseau, France                    ###
###                                                           ###
#################################################################

from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np
import copy

### Read Abaqus File from a CIRCLE and return the vertices and polygons of a Voronoi network

def INP_Circle_ReturnVerticesForVoronoi(
        mesh_filename,
        verbose=0):

    points = []
    center = []

    # Read the INP file
    mesh_file = open(mesh_filename, "r")

    context = ""
    for line in mesh_file:
        if line.startswith("**") : continue

        line = line.strip("\n ,")
        #mypy.my_print(verbose-1, "line =", line)

        if (context != ""):
            if line.startswith("*"):
                context = ""
            else:
                if (context == "reading nodes"):
                    splitted_line = line.split(",")
                    points.append([float(coord) for coord in splitted_line[1:3]])

        if line.startswith("*NODE"):
            context = "reading nodes"

    center = points[0]
    points.remove(points[0])

    points = np.array(points)
    vor = Voronoi(points)

    vertices = vor.vertices.tolist()
    polygons = vor.regions

    # Remove the polygons that are at the edge of the Voronoi regions (infinite area)
    polygons.remove(polygons[0])
    polygondelete = []
    for i in range(len(polygons)):
        if -1 in polygons[i]:
            polygondelete.append(polygons[i])
    for i in range(len(polygondelete)):
        polygons.remove(polygondelete[i])

    # Remove the vertices that have only one polygon on the boundary
    count = np.zeros(len(vertices))
    for i in range(len(polygons)):
        for j in range(len(polygons[i])):
            count[polygons[i][j]] += 1

    vertices_save = list(vertices)
    for i in range(len(vertices_save)):
        if count[i] < 2 :
            vertices.remove(vertices_save[i])

    polygons_save = copy.deepcopy(polygons)
    for i in range(len(polygons_save)):
        for j in range(len(polygons_save[i])):
            if count[polygons_save[i][j]] < 2:
                polygons[i].remove(polygons_save[i][j])

    i = 0
    while i <len(vertices):
        check = False
        for j in range(len(polygons)):
            if i in polygons[j]:
                check = True
                i += 1
        if check == False :
            for j in range(len(polygons)):
                for k in range(len(polygons[j])):
                    if polygons[j][k] > i:
                        polygons[j][k] -= 1
    ##

    points = list(vertices)
    return [points, polygons]