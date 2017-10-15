# -*- coding: utf-8 -*-

# thirdparty libs
import igraph as ig
import plotly.offline as offline
import plotly.plotly as py
from plotly.graph_objs import *

# html_top = os.path.join(os.path.dirname(__file__), '../lib/html/network_top.html')
# html_tail = os.path.join(os.path.dirname(__file__), '../lib/html/network_tail.html')

def plot_data_to_file(data, filename , title, dot_width=0.5, div=True):
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
		# layt = G.layout('kk', dim=3)
		layt = G.layout('kk', dim=2)

		# node co-ordinates
		Xn = [layt[k][0] for k in range(N)]# x-coordinates of nodes
		Yn = [layt[k][1] for k in range(N)]# y-coordinates
		# Zn = [layt[k][2] for k in range(N)]# z-coordinates

		Xe = []
		Ye = []
		# Ze = []

		for e in Edges:
		    Xe += [layt[e[0]][0],layt[e[1]][0], None]# x-coordinates of edge ends
		    Ye += [layt[e[0]][1],layt[e[1]][1], None]
		    # Ze += [layt[e[0]][2],layt[e[1]][2], None]

		# lines
		# trace1 = Scatter3d(x = Xe,
		#                y = Ye,
		#                z = Ze,
		#                mode = 'lines',
		#                line = Line(color = line_color, width = line_size),
		#                hoverinfo = 'none'
		#                )
		# print line_opacity
		# print help(Scatter)
		trace1_2d = Scatter(x = Xe,
		               y = Ye,
		               mode = 'lines',
		               visible = True,
		               line = Line(color = line_color, width = 1),
		               hoverinfo = 'none',
		               opacity = 0.2
		               )

		# nodes
		# trace2 = Scatter3d(x = Xn,
		#                y = Yn,
		#                z = Zn,
		#                mode = 'markers',
		#                name = 'actors',
		#                marker = Marker(symbol = 'dot',
		#                              size = node_size,
		#                              color = node_color,
		#                              opacity = node_opacity,
		#                              colorscale = 'Viridis',
		#                              line = Line(color = 'rgb(50,50,50)', width = dot_width)),
		#                text = node_name,
		#                hoverinfo = 'text'
		#                )

		trace2_2d = Scatter(x = Xn,
		               y = Yn,
		               mode = 'markers',
		               name = 'actors',
		               marker = Marker(symbol = 'dot',
		                             size = node_size,
		                             color = node_color,
		                             opacity = node_opacity,
		                             colorscale = 'Viridis',
		                             line = Line(color = 'rgb(50,50,50)', width = dot_width),
		                             ),
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

		# layout = Layout(
		# 	title=title,
		# 	width=1200,
		# 	height=800,
		# 	showlegend=False,
		# 	showgrid=False,
		# 	scene=Scene(
		# 		xaxis=XAxis(axis),
		# 		yaxis=YAxis(axis),
		# 		# zaxis=ZAxis(axis)
		# 		),
		# 	margin=Margin(t=30),
		# 	hovermode='closest',
		# 	)

		layout = Layout(
			# title=title,
			width=1100,
			height=600,
			showlegend=False,
			# showgrid=False,
			xaxis=XAxis(axis),
			yaxis = YAxis(axis),
			# scene=Scene( xaxis=XAxis(axis), yaxis=YAxis(axis), bgcolor='#eee'),
			margin=Margin(t=0),
			hovermode='closest',
			plot_bgcolor='rgba(0,0,0,0)',
			paper_bgcolor='rgba(0,0,0,0)',
			hidesources=True,
			)

		# data = Data([trace1, trace2])
		# fig = Figure(data=data, layout=layout)
		data = Data([trace1_2d, trace2_2d])
		fig = Figure(data=data, layout=layout)
		# print fig
		if div:
			# add javascript script
			js = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
			html = offline.plot(fig, include_plotlyjs=False, output_type='div')
			html = js+html

			# write it out
			with open(filename, "a") as f:
				f.write(html.encode("utf8"))
		else:
			offline.plot(fig, filename=filename, auto_open=False)
