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
		for node in data['nodes']:
			labels.append(node['name'])
			group.append(node['group'])
			sizes.append(node['size'])

		# create a Kamada-Kawai layout
		layt = G.layout('kk', dim=3)

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

		trace1 = Scatter3d(x=Xe,
		               y=Ye,
		               z=Ze,
		               mode='lines',
		               line=Line(color='rgb(125,125,125)', width=2),
		               hoverinfo='none'
		               )
		trace2 = Scatter3d(x=Xn,
		               y=Yn,
		               z=Zn,
		               mode='markers',
		               name='actors',
		               marker=Marker(symbol='dot',
		                             size=sizes,
		                             color=group,
		                             colorscale='Viridis',
		                             line=Line(color='rgb(50,50,50)', width=dot_width)
		                             ),
		               text=labels,
		               hoverinfo='text'
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
		         height=1000,
		         showlegend=False,
		         scene=Scene(
		         xaxis=XAxis(axis),
		         yaxis=YAxis(axis),
		         zaxis=ZAxis(axis),
		        ),
		     margin=Margin(
		        t=100
		    ),
		    hovermode='closest',
		    # annotations=Annotations([
		    #        Annotation(
		    #        showarrow=False,
		    #         text="Data source: <a href='http://bost.ocks.org/mike/miserables/miserables.json'>[1] miserables.json</a>",
		    #         xref='paper',
		    #         yref='paper',
		    #         x=0,
		    #         y=0.1,
		    #         xanchor='left',
		    #         yanchor='bottom',
		    #         font=Font(
		    #         size=14
		    #         )
		    #         )
		    #     ]),    
		)

		data = Data([trace1, trace2])
		fig = Figure(data=data, layout=layout)
		offline.plot(fig, filename=filename, auto_open=False)
