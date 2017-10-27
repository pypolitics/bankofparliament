# -*- coding: utf-8 -*-

# thirdparty libs
import igraph as ig
import plotly.offline as offline
import plotly.plotly as py
from plotly.graph_objs import *

def plot_data_to_file(data, filename , title, dot_width=0.5, div=True, width=1100, height=700):
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

		# LINE
		line_color = []
		line_opacity = []
		line_size = []

		# NODE
		node_color = []
		node_opacity = []
		node_size = []
		node_name = []
		node_hovertext = []
		node_hyperlink = []

		for lin in data['links']:
			line_color.append(lin['color'])
			line_opacity.append(lin['opacity'])
			line_size.append(lin['size'])

		for node in data['nodes']:
			# clean up category nodes
			nn = node['name'].split(' Categories')[0]
			nn = nn.replace('_', ' ')
			node_name.append(nn)

			node_color.append(node['color'])
			node_opacity.append(node['opacity'])
			node_size.append(node['size'])
			node_hovertext.append(node['hovertext'])
			node_hyperlink.append(node['hyperlink'])

		# create a Kamada-Kawai layout
		layt = G.layout('kk', dim=2)

		# node co-ordinates
		Xn = [layt[k][0] for k in range(N)]# x-coordinates of nodes
		Yn = [layt[k][1] for k in range(N)]# y-coordinates

		Xe = []
		Ye = []

		for e in Edges:
		    Xe += [layt[e[0]][0],layt[e[1]][0], None]# x-coordinates of edge ends
		    Ye += [layt[e[0]][1],layt[e[1]][1], None]

		traces = []
		trace1_2d = Scatter(x = Xe,
		               y = Ye,
		               mode = 'lines',
		               visible = True,
		               line = Line(color = line_color, width = 1),
		               hoverinfo = 'none',
		               opacity = 0.2,
		               name = 'lines'
		               )
		traces.append(trace1_2d)

		trace2_2d = Scatter(x = Xn,
		               y = Yn,
		               mode = 'markers+text',
		               name = 'nodes',
		               marker = Marker(symbol = 'dot',
		                             size = node_size,
		                             color = node_color,
		                             opacity = node_opacity,
		                             colorscale = 'Viridis',
		                             line = Line(color = 'rgb(50,50,50)', width = dot_width),
		                             ),
		               text = node_name,
		               textposition='middle',
		               hoverinfo = 'text',
		               hovertext = node_hovertext,
		               customdata = node_hyperlink
		               )
		traces.append(trace2_2d)

		axis = dict(showbackground=False,
		          showline=False,
		          zeroline=False,
		          showgrid=False,
		          showticklabels=False,
		          title=''
		          )

		layout = Layout(
			# title=title,
			width=width,
			height=height,
			showlegend=False,
			xaxis=XAxis(axis),
			yaxis = YAxis(axis),
			# margin=Margin(t=0),
			hovermode='closest',
			plot_bgcolor='rgba(0,0,0,0)',
			paper_bgcolor='rgba(0,0,0,0)',
			hidesources=True,
			)

		# plot to file
		data = Data(traces)
		fig = Figure(data=data, layout=layout)
		if div:
			# add javascript script
			js = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>\n'
			# hyper = '<a href="url">link text</a>\n'
			html = offline.plot(fig, include_plotlyjs=False, output_type='div')
			html = js + html

			# write it out
			with open(filename, "a") as f:
				f.write(html.encode("utf8"))
		else:
			offline.plot(fig, filename=filename, auto_open=False)
