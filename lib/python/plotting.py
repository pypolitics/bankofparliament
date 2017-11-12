# -*- coding: utf-8 -*-

import json

# thirdparty libs
import igraph as ig
import plotly.offline as offline
import plotly.plotly as py
from plotly.graph_objs import *

def plot_data_to_file(data, plot_file, member_id, title, constituency, hyperlink=None, dot_width=0.5, div=True, width=1100, height=619, write=False):
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
		# node_hyperlink = []

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
			# node_hyperlink.append(node['hyperlink'])

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
		               # customdata = node_hyperlink
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
			autosize=True,
			width=width,
			height=height,
			showlegend=False,
			xaxis=XAxis(axis),
			yaxis = YAxis(axis),
			margin=Margin(t=0),
			hovermode='closest',
			plot_bgcolor='rgba(0,0,0,0)',
			paper_bgcolor='rgba(0,0,0,0)',
			hidesources=True,
			annotations=Annotations([
				Annotation(
					showarrow=False,
					text="Data source: <a href='%s'>theyworkforyou</a>" % hyperlink,
					xref='paper',
					yref='paper',
					x=0,
					y=0,
					font=Font(
						size=12)
					),
				Annotation(
					showarrow=False,
					text='<a><b>%s,</b> %s</a>' %(title.title(), constituency.title()),
					xref='paper',
					yref='paper',
					x=0.5,
					y=1,
					font=Font(
						size=14, color="#444")
				)
			]),



			)

		# plot to file
		data = Data(traces)
		fig = Figure(data=data, layout=layout)

		offline.plot(fig, filename='/Users/elliott/Documents/pypolitics/notpolitics/misc/plot.html', auto_open=True)
		return
		# save data and layout to json
		json_data = {'data' : data, 'layout' : layout}
		with open(plot_file, "w") as f:
			json.dump(json_data, f)

		if div:
			# add javascript script
			js = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>\n'
			html = offline.plot(fig, include_plotlyjs=False, output_type='div')
			html = js + html

			# write it out
			if write:
				with open(plot_file.replace('json', 'html'), "a") as f:
					f.write(html.encode("utf8"))
			return html
		else:
			offline.plot(fig, filename=filename, auto_open=False)
