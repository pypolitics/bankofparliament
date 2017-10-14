# -*- coding: utf-8 -*-

# thirdparty libs
import igraph as ig
import plotly.offline as offline
import plotly.plotly as py
from plotly.graph_objs import *

def plot_data_to_file(data, filename , title, dot_width=0.5):
	"""
	"""

	# number of nodes
	N = len(data['nodes'])

	# number of links
	L = len(data['links'])
	if L > 0:
		# for every link, create a tuple of source and target (ids, of nodes)
		Edges = [(data['links'][k]['source'], data['links'][k]['target']) for k in range(L)]

		# create graph of lines
		G = ig.Graph(Edges, directed=False)

		labels=[]
		group=[]
		sizes = []
		opacity = []

		# LINE
		# 'minor' : {'color' : colors[light_grey], 'opacity' : 0.5, 'size' : 4, 'name' : None, 'size_scaler' : 0},
		line_color = []
		line_opacity = []
		line_size = []

		# NODE
		# 'reg_donor_company' : {'color' : colors[light_orange], 'opacity' : 1, 'size' : 40, 'name' : None, 'size_scaler' : 0},
		node_color = []
		node_opacity = []
		node_size = []
		node_name = []

		for lin in data['links']:
			line_color.append(lin['color'])
			line_opacity.append(lin['opacity'])
			line_size.append(lin['size'])

		for node in data['nodes']:
			node_name.append(node['name'])
			node_color.append(node['color'])
			node_opacity.append(node['opacity'])
			node_size.append(node['size'])

		# create a Kamada-Kawai layout
		layt = G.layout('kk', dim=3)
		# layt_2d = G.layout('kk', dim=2)

		# node co-ordinates
		Xn = [layt[k][0] for k in range(N)]# x-coordinates of nodes
		Yn = [layt[k][1] for k in range(N)]# y-coordinates
		Zn = [layt[k][2] for k in range(N)]# z-coordinates

		Xe = []
		Ye = []
		Ze = []

		for e in Edges:
		    Xe += [layt[e[0]][0],layt[e[1]][0], None]# x-coordinates of edge ends
		    Ye += [layt[e[0]][1],layt[e[1]][1], None]
		    Ze += [layt[e[0]][2],layt[e[1]][2], None]

		# lines
		trace1 = Scatter3d(x = Xe,
		               y = Ye,
		               z = Ze,
		               mode = 'lines',
		               line = Line(color = line_color, width = line_size),
		               hoverinfo = 'none'
		               )

		# nodes
		trace2 = Scatter3d(x = Xn,
		               y = Yn,
		               z = Zn,
		               mode = 'markers',
		               name = 'actors',
		               marker = Marker(symbol = 'dot',
		                             size = node_size,
		                             color = node_color,
		                             opacity = node_opacity,
		                             colorscale = 'Viridis',
		                             line = Line(color = 'rgb(50,50,50)', width = dot_width)),
		               text = node_name,
		               hoverinfo = 'text'
		               )


		axis = dict(showbackground=False,
		          showline=False,
		          zeroline=False,
		          showgrid=False,
		          showticklabels=False,
		          title=''
		          )

		layout = Layout(
			title=title,
			width=1200,
			height=800,
			showlegend=False,
			scene=Scene(
				xaxis=XAxis(axis),
				yaxis=YAxis(axis),
				zaxis=ZAxis(axis)),
			margin=Margin(t=30),
			hovermode='closest',
			)

		data = Data([trace1, trace2])
		fig = Figure(data=data, layout=layout)
		offline.plot(fig, filename=filename, auto_open=False)
