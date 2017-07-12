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
from INP_Circle_ReturnVerticesForVoronoi import INP_Circle_ReturnVerticesForVoronoi
from get_neighbors_links import get_neighbors_links

import networkx as nx
from matplotlib import pyplot as plt

T = 20.
time_steps = 10.
dt = T / time_steps
gamma = 0.01

mesh_basename = "Circle_triangle"

[points, polygons] = INP_Circle_ReturnVerticesForVoronoi(
	mesh_filename = mesh_basename+".inp")

[vertices, links, cells] = createnetwork(points, polygons)

G = nx.Graph()
membrane = []
inside = []

for i in range(len(vertices)) :
	G.add_node(i, pos = (vertices[i].coords[0], vertices[i].coords[1]))
for i in range(len(links)) :
	if links[i].place == "membrane" :
		G.add_edge(links[i].vertices[0].n, links[i].vertices[1].n)
		membrane.append((links[i].vertices[0].n,links[i].vertices[1].n))
	if links[i].place == "inside" :
		G.add_edge(links[i].vertices[0].n, links[i].vertices[1].n)
		inside.append((links[i].vertices[0].n,links[i].vertices[1].n))
pos = nx.get_node_attributes(G, 'pos')

nx.draw_networkx_nodes(G, pos,
	node_color = 'b',
	node_size = 2)
nx.draw_networkx_edges(G, pos,
	edgelist = membrane,
	edge_color = 'black',
	width = 1)
nx.draw_networkx_edges(G, pos,
	edgelist = inside,
	edge_color='green',
	width = 0.5)

plt.axis('equal')
plt.savefig('test1_'+str(i)+'.png')