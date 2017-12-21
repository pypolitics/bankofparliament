# -*- coding: utf-8 -*-

import json

# thirdparty libs
import igraph as ig
import plotly.offline as offline
import plotly.plotly as py
from plotly.graph_objs import *

parliament = 'http://data.parliament.uk/membersdataplatform/services/mnis/members/query/refDods='
companieshouse = 'https://beta.companieshouse.gov.uk/search?q='
theipsa = 'http://www.theipsa.org.uk/mp-costs/other-published-data/'

def plot_data_to_file(data, plot_file, member_id, dods_id, title, constituency, party, hyperlink=None):
	"""
	"""
	imagepath = 'https://raw.githubusercontent.com/pypolitics/notpolitics/master/lib/data/images/%s.png' % member_id
	parliament_hyperlink = parliament + dods_id + '/' + 'GovernmentPosts|BiographyEntries|Committees'

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
		node_border_color = []
		node_border_size = []
		node_text_size = []
		node_text_color = []

		for lin in data['links']:
			line_color.append(lin['color'])
			line_opacity.append(lin['opacity'])
			line_size.append(lin['size'])

		for node in data['nodes']:
			# clean up category nodes
			nn = node['name']
			nn = nn.replace('_', ' ')
			node_name.append(nn)

			node_color.append(node['color'])
			node_opacity.append(node['opacity'])
			node_size.append(node['size'])
			node_hovertext.append(node['hovertext'])
			node_hyperlink.append(node['hyperlink'])
			node_text_size.append(node['node_text_size'])
			node_text_color.append(node['node_text_color'])

			node_border_size.append(node['border_style']['size'])
			node_border_color.append(node['border_style']['color'])

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
		               line = Line(color = line_color, width = 2),
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
		                             line = Line(color = node_border_color, width = node_border_size),
		                             ),
		               text = node_name,
		               textposition='middle',
		               hoverinfo = 'text',
		               hovertext = node_hovertext,
		               customdata = node_hyperlink,
		               textfont=Font(size=node_text_size, color=node_text_color, family="Abel")
		               )
		traces.append(trace2_2d)

		axis = dict(showbackground=False,
		          showline=False,
		          zeroline=False,
		          showgrid=False,
		          showticklabels=False,
		          title=''
		          )

		# these images do not yet exist, need to make them
		# pin an image to the middle of the first marker
		images = [dict(source= imagepath,
						xref= "x",
						yref= "y",
						x= Xe[0], # first index
						y= Ye[0], # first index
						sizex= 1.5,
						sizey= 1.5,
						sizing="contain",
						xanchor= "center",
						yanchor= "middle",)
		]
		# set to nothing for now
		images = []

		layout = Layout(
			autosize=True,
			showlegend=False,
			xaxis=XAxis(axis),
			yaxis = YAxis(axis),
			margin=Margin(
				l=20,
				r=20,
				b=20,
				t=20,
				pad=4
			),
			hovermode='closest',
			dragmode='pan',
			plot_bgcolor='rgba(0,0,0,0)',
			paper_bgcolor='rgba(0,0,0,0)',
			hidesources=True,
			font=Font(size=14, color="#444", family="Abel"),
			annotations=Annotations([
				Annotation(
					showarrow=False,
					text='<a style="color: black; font-weight: 100; font-size: 12px;">Data sources: </a><a href="%s">theyworkforyou.com</a>,  <a href="%s">data.parliament.uk</a>,  <a href="%s%s">beta.companieshouse.gov.uk</a>,  <a href="%s">theipsa.org.uk</a>' % (hyperlink, parliament_hyperlink, companieshouse, title.replace(' ', '+'), theipsa), 
					xref='paper',
					yref='paper',
					x=0,
					y=0,
					font=Font(
						size=12, family="Abel")
					),
				Annotation(
					showarrow=False,
					text='<a style="color: black; font-weight: 200;">Registered financial interests and expenses</a>',
					xref='paper',
					yref='paper',
					x=0.5,
					y=0.96,
					font=Font(
						size=14, color="#444", family="Abel")
					),
				Annotation(
					showarrow=False,
					text='<a style="color: black; font-weight: 200;"><b>%s,</b> %s, %s</a>' %(title.title(), constituency.title(), party.title()),
					xref='paper',
					yref='paper',
					x=0.5,
					y=1,
					font=Font(
						size=18, color="#444", family="Abel")
					),
				Annotation(
					showarrow=False,
					text='<a style="color:red">►</a>',
					xref='paper',
					yref='paper',
					x=1,
					y=0.97,
					captureevents=True,
					font=Font(
						size=34, color="red", family="Abel")
				)
			]),
			images=images
				)

		data = Data(traces)
		# fig = Figure(data=data, layout=layout)
		# html = offline.plot(fig, auto_open=True)
		# return

		# save data and layout to json
		json_data = {'data' : data, 'layout' : layout}
		with open(plot_file, "w") as f:
			json.dump(json_data, f)

def plot_3d_data_to_file(data, plot_file, member_id, dods_id, title, constituency, party, hyperlink=None):
	"""
	"""
	imagepath = 'https://raw.githubusercontent.com/pypolitics/notpolitics/master/lib/data/images/%s.png' % member_id
	parliament_hyperlink = parliament + dods_id + '/' + 'GovernmentPosts|BiographyEntries|Committees'

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
		node_border_color = []
		node_border_size = []
		node_symbol = []
		node_id = []

		for lin in data['links']:
			line_color.append(lin['color'])
			line_opacity.append(lin['opacity'])
			line_size.append(lin['size'])

		for node in data['nodes']:
			node_id.append(node['id'])
			# clean up category nodes
			nn = node['name']
			nn = nn.replace('_', ' ')
			node_name.append(nn)

			node_color.append(node['color'])
			node_opacity.append(node['opacity'])
			node_size.append(node['size'])
			node_hovertext.append(node['hovertext'])
			node_hyperlink.append(node['hyperlink'])
			node_symbol.append(node['symbol'])

			node_border_size.append(node['border_style']['size'])
			node_border_color.append(node['border_style']['color'])

		# create a Kamada-Kawai layout
		layt = G.layout('kk', dim=3)

		# node co-ordinates
		Xn = [layt[k][0] for k in range(N)]# x-coordinates of nodes
		Yn = [layt[k][1] for k in range(N)]# y-coordinates
		Zn = [layt[k][2] for k in range(N)]# y-coordinates

		Xe = []
		Ye = []
		Ze = []

		for e in Edges:
		    Xe += [layt[e[0]][0],layt[e[1]][0], None]# x-coordinates of edge ends
		    Ye += [layt[e[0]][1],layt[e[1]][1], None]
		    Ze += [layt[e[0]][2],layt[e[1]][2], None]

		traces = []
		trace1_2d = Scatter3d(x = Xe,
		               y = Ye,
		               z =Ze,
		               mode = 'lines',
		               visible = True,
		               line = Line(color = 'gray', width = 3),
		               hoverinfo = 'none',
		               opacity = 0.4,
		               name = 'lines'
		               )
		traces.append(trace1_2d)

		trace2_2d = Scatter3d(x = Xn,
		               y = Yn,
		               z = Zn,
		               mode = 'markers+text',
		               name = 'nodes',
		               marker = Marker(symbol = node_symbol,
		                             size = node_size,
		                             color = node_color,
		                             # colorscale='Viridis',
		                             opacity = node_opacity,
		                             line = Line(color = node_border_color, width = node_border_size),
		                             ),
		               text = node_name,
		               textposition='middle',
		               hoverinfo = 'text',
		               hovertext = node_hovertext,
		               hoverlabel = {'bgcolor': node_color},
		               customdata = node_hyperlink,
		               textfont=Font(size=18, family="Abel")
		               )
		traces.append(trace2_2d)

		axis = dict(showbackground=False,
		          showline=False,
		          zeroline=False,
		          showgrid=False,
		          showticklabels=False,
		          title='',
		          showspikes=False,
		          )

		# set to nothing for now
		images = []

		# camera view - slight zoom in
		camera = dict(
			up=dict(x=0, y=0, z=1),
			center=dict(x=0, y=0, z=0),
			eye=dict(x=0.1, y=0.1, z=1)
			)

		layout = Layout(
			autosize=True,
			showlegend=False,
			scene=Scene(
				xaxis=XAxis(axis),
				yaxis=YAxis(axis),
				zaxis=ZAxis(axis),
				camera=camera),
			margin=Margin(
				l=20,
				r=20,
				b=20,
				t=20,
				pad=4
			),
			hovermode='closest',
			plot_bgcolor='rgba(0,0,0,0)',
			paper_bgcolor='rgba(0,0,0,0)',
			hidesources=True,
			font=Font(size=14, color="#444", family="Abel"),
			annotations=Annotations([
				Annotation(
					showarrow=False,
					text='<a style="color: rgb(250, 250, 250); font-weight: 100; font-size: 12px;">Data sources: </a><a href="%s%s">beta.companieshouse.gov.uk</a>' % (companieshouse, title.replace(' ', '+')), 
					xref='paper',
					yref='paper',
					x=0,
					y=0,
					font=Font(
						size=12, family="Abel", color='white')
					),
				Annotation(
					showarrow=False,
					text='<a style="color: rgb(250, 250, 250); font-weight: 200;">Political and financial Links</a>',
					xref='paper',
					yref='paper',
					x=0.5,
					y=0.96,
					font=Font(
						size=14, family="Abel", color='white')
					),
				Annotation(
					showarrow=False,
					text='<a style="color: rgb(250, 250, 250); font-weight: 200;"><b>%s,</b> %s, %s</a>' %(title.title(), constituency.title(), party.title()),
					xref='paper',
					yref='paper',
					x=0.5,
					y=1,
					font=Font(
						size=18, color="white", family="Abel")
					),
				Annotation(
					showarrow=False,
					text='<a style="color:red">◀</a>',
					xref='paper',
					yref='paper',
					x=0,
					y=0.97,
					captureevents=True,
					font=Font(
						size=34, color="red", family="Abel")
				)
			]),
			images=images
				)

		data = Data(traces)
		# fig = Figure(data=data, layout=layout)
		# html = offline.plot(fig, auto_open=True)
		# return

		# save data and layout to json
		json_data = {'data' : data, 'layout' : layout}
		with open(plot_file, "w") as f:
			json.dump(json_data, f)
