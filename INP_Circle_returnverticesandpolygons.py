#coding=utf8

#################################################################
###                                                           ###
### Created by Bastien MARTY, 2017                            ###
###                                                           ###
### École polytechnique, Palaiseau, France                    ###
###                                                           ###
#################################################################

### Read Abaqus File from a CIRCLE and return the vertices and polygons

def INP_Circle_returnverticesandpolygons(
        mesh_filename,
        verbose=0):

    points = []
    polygons = []

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
                    points.append([float(coord) for coord in splitted_line[1:4]])
                elif (context == "reading elems"):
                    splitted_line = line.split(",")
                    polygons.append([int(coord)-2 for coord in splitted_line[1:5]])
                    

        if line.startswith("1, "):
            context = "reading nodes"
        elif line.startswith("*ELEMENT"):
            if (("TYPE=CPS4" in line) or ("type=CPS4" in line) or ("TYPE=CPE4" in line) or ("type=CPE4" in line)):
                context = "reading elems"            
            else:
                print("Warning: elements not read: "+line+".")

    #we destroy the z coordinate that equals 0 evrywhere
    for i in range(len(points)):
        points[i].remove(points[i][-1])
    return [points,polygons]