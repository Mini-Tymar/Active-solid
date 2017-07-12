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

import networkx as nx
from matplotlib import pyplot as plt

# Plotting of the network using networkx

def plot_network(
	vertices,
	links,
	t,
	folder_basename):

	G = nx.Graph()
	membrane = []
	inside = []

	# Creation of all the nodes equivalent of vertices
	for i in range(len(vertices)) :
		G.add_node(i, pos = (vertices[i].coords[0], vertices[i].coords[1]))
	
	# Creation of all the links wit a different colro for the ones inside
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

	figure = plt.gcf()
	# If we change the size and the dpi we can change the resolution.
	figure.set_size_inches(12,12)
	plt.axis('equal')
	plt.savefig(folder_basename+"/test1_"+str(t)+".png", dpi = 100)
	plt.clf()