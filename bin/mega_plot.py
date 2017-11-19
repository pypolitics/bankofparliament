# -*- coding: utf-8 -*-

# thirdparty libs
import igraph as ig
import plotly.offline as offline
import plotly.plotly as py
from plotly.graph_objs import *
from optparse import OptionParser
import os, sys, json
import operator, copy
import sys
sys.path.append('../lib/python')
from constants import party_colours

orange_darker = '#f7a55d'
orange_lighter = '#fac99e'

yellow_darker = '#fff570'
yellow_lighter = '#fff899'

pink_darker = '#ffbaf4'
pink_lighter = 'rgb(255, 235, 251)'

grey_darker = '#b8bab8'
grey_lighter = '#d8dad8'

green_darker = '#00ff99'
green_lighter = '#4dffb8'

data_lines = {  'major' : {'color' : 'white', 'opacity' : 1, 'size' : 4, 'name' : None},
                # 'minor' : {'color' : 'rgb(25, 3, 79)', 'opacity' : 0, 'size' : 4, 'name' : None},

                'income_line' : {'color' : orange_darker, 'opacity' : 0.4, 'size' : 8, 'name' : None},
                'wealth_line' : {'color' : grey_darker, 'opacity' : 0.4, 'size' : 8, 'name' : None},
                'freebies_line' : {'color' : yellow_darker, 'opacity' : 0.4, 'size' : 8, 'name' : None},
                'miscellaneous_line' : {'color' : pink_darker, 'opacity' : 0.4, 'size' : 8, 'name' : None},
                'expenses_line' : {'color' : green_darker, 'opacity' : 0.4, 'size' : 8, 'name' : None},

                }

data_nodes = {  'mp'                : {'color' : grey_lighter, 'opacity' : 1, 'size' : 30},
				'item'              : {'color' : grey_lighter, 'opacity' : 1, 'size' : 10},

                'income_item'        : {'color' : orange_lighter, 'opacity' : 0.9, 'size' : 30},
                'income_sub'        : {'color' : orange_darker, 'opacity' : 1, 'size' : 40},
                'income_cat'        : {'color' : orange_darker, 'opacity' : 1, 'size' : 60},

                'freebies_item'        : {'color' : yellow_lighter, 'opacity' : 0.9, 'size' : 30},
                'freebies_sub'        : {'color' : yellow_darker, 'opacity' : 1, 'size' : 40},
                'freebies_cat'        : {'color' : yellow_darker, 'opacity' : 1, 'size' : 60},

                'wealth_item'        : {'color' : grey_lighter, 'opacity' : 0.9, 'size' : 30},
                'wealth_sub'        : {'color' : grey_darker, 'opacity' : 1, 'size' : 40},
                'wealth_cat'        : {'color' : grey_darker, 'opacity' : 1, 'size' : 60},

                'miscellaneous_item'        : {'color' : pink_lighter, 'opacity' : 0.9, 'size' : 30},
                'miscellaneous_sub'        : {'color' : pink_darker, 'opacity' : 1, 'size' : 40},
                'miscellaneous_cat'        : {'color' : pink_darker, 'opacity' : 1, 'size' : 60},

                'expenses_item'        : {'color' : green_lighter, 'opacity' : 0.9, 'size' : 30},
                'expenses_sub'        : {'color' : green_darker, 'opacity' : 1, 'size' : 40},
                'expenses_cat'        : {'color' : green_darker, 'opacity' : 1, 'size' : 60},

                }

def main(mps):
	"""
	"""

	data = {'nodes' : [], 'links' : []}

	node_main = make_node(data_nodes['mp'], name='House of Commons', hovertext="House of Commons", node_type='mp')
	main_copy = copy.copy(node_main)
	main_copy['color'] = 'white'
	# data['nodes'].append(main_copy)

	print 'Make nodes'
	for mp in mps:
		# print '\n%s' % mp['name']
		# main_copy['size'] +=0.1
		splits = mp['name'].split(' ')
		first = splits[0]
		last = ' '.join(splits[1:])
		label = '<b>%s<br>%s' % (first, last)

		node_mp = make_node(data_nodes['mp'], name=label, hovertext='%s' % mp['name'], node_type='mp')
		node_copy = copy.copy(node_mp)
		node_copy['color'] = party_colours[mp['party'].lower()]
		data['nodes'].append(node_copy)

		link = make_link(data_lines['major'], nodes = data['nodes'], source=node_copy, target=node_copy, amount=0)
		l = copy.copy(link)
		data['links'].append(l)

		for cat in mp['categories']:

			# if cat['category_description'] in ['Indirect Donations', 'Direct Donations', 'Gifts', 'Vists Outside UK', 'Gifts Outside UK', 'Shareholdings', 'Other Shareholdings']:
			if cat['category_description'] in ['Indirect Donations', 'Direct Donations', 'Gifts', 'Vists Outside UK', 'Gifts Outside UK']:

				for item in cat['items']:

					node_item = make_node(data_nodes['item'], name=item['pretty'], hovertext=item['pretty'], node_type='mp')
					node_item_copy = copy.copy(node_item)

					if node_item_copy not in data['nodes']:
						# print '\t\tNot in nodes : %s' % item['pretty']
						data['nodes'].append(node_item_copy)
					# else:
						# print '\t\tMatched a node : %s' % item['pretty']

					link = make_link(data_lines['major'], nodes = data['nodes'], source=node_copy, target=node_item_copy, amount=item['amount'])
					l = copy.copy(link)
					data['links'].append(l)

	print 'Find sizes'
	# find the total node amounts
	amounts = []
	for node in data['nodes']:
		node['amount'] = 0
		if node['name'] != 'House of Commons':

			for link in data['links']:
				# if the links target is the node, add to amount and store that amount in list
				if link['target'] == data['nodes'].index(node):

					node['amount'] += link['amount']
					amounts.append(link['amount'])

	# scale the nodes, by their amounts
	current_min = min(amounts)
	current_max = max(amounts)
	new_min = 10
	new_max = 100

	for n in data['nodes']:
		size_value = int(translate(int(n['amount']), current_min, current_max, new_min, new_max))
		n['size'] = size_value
		n['name'] = n['name'] + u' £' + "{:,}".format(n['amount'])

	plot(data)

def plot(data, dot_width=0.5):
	"""
	"""
	color = 'rgb(4, 13, 35)'
	print 'Start plot'
	# number of nodes
	N = len(data['nodes'])

	# number of links
	L = len(data['links'])

	print N
	print L

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
		               line = Line(color = 'white', width = 1),
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
			# title=title,
			width=1300,
			height=800,
			showlegend=False,
			# plot_bgcolor='rgba(0,0,0,0)',
			# paper_bgcolor='rgba(0,0,0,0)',
			plot_bgcolor=color,
			paper_bgcolor=color,
			# plot_bgcolor='black',
			# paper_bgcolor='black',
			scene=Scene(
				xaxis=XAxis(axis),
				yaxis=YAxis(axis),
				zaxis=ZAxis(axis)),
			margin=Margin(t=1),
			hovermode='closest',
			)

		data = Data([trace1, trace2])
		fig = Figure(data=data, layout=layout)

		print 'Now Plot'
		html = offline.plot(fig, auto_open=True)

node_id = 0
def make_node(node, name, hovertext, node_type, hyperlink=None, unique=False):
    """"""
    if unique:
        global node_id
        node_id += 1
        node['id'] = node_id

    node['name'] = name
    node['hovertext'] = hovertext
    node['node_type'] = node_type
    node['hyperlink'] = hyperlink
    node['border_style'] = {'color' : 'rgb(50,50,50)', 'size' : 0.5}
    return node

def make_link(link, nodes, source, target, amount):
    """"""

    link['source'] = nodes.index(source)
    link['target'] = nodes.index(target)
    link['amount'] = amount
    # print link
    return link

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def sort_by_options(mps, options):
    """
    Sort by options
    """

    # sort by options specified on commandline
    if options.sortby == 'name':
        mps = sorted(mps, key=operator.itemgetter('name'))

    elif options.sortby == 'wealth':
        mps = sorted(mps, key=operator.itemgetter('mp_wealth'), reverse=True)

    elif options.sortby == 'income':
        mps = sorted(mps, key=operator.itemgetter('mp_income'), reverse=True)

    elif options.sortby == 'gifts':
        mps = sorted(mps, key=operator.itemgetter('mp_gifts'), reverse=True)

    elif options.sortby == 'donations':
        mps = sorted(mps, key=operator.itemgetter(
            'mp_donations'), reverse=True)

    elif options.sortby == 'annual':
        mps = sorted(mps, key=operator.itemgetter('mp_annual'), reverse=True)

    else:
        mps = sorted(mps, key=operator.itemgetter(
            '%s' % options.sortby))

    return mps

def read_json_file():
    """
    Read file from json_dump_location
    """
    json_dump_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lib', 'data', 'members')
    data = []
    for mp in os.listdir(json_dump_location):
        f = os.path.join(json_dump_location, mp)
        with open(f) as json_data:
            data.append(json.load(json_data))

    return data

def run():
    """"""
    mps = read_json_file()
    mps = sorted(mps, key=operator.itemgetter('name'))
    main(mps)

if __name__ == "__main__":
    """
    Commandline run
    """
    parser = OptionParser()
    parser.add_option("--sortby", help="Sort By", action="store", default='surname')

    # parse the comand line
    (options, args) = parser.parse_args()

    # return a list (of dicts) of mps
    mps = read_json_file()
    searched = []

    # TODO: fix this crude arg porser
    if args:
        for member in args:
            for i in mps:
                if member.lower() in i['name'].lower():
                    searched.append(i)
                if member.lower() in i['party'].lower():
                    searched.append(i)
                if member.lower() in i['constituency'].lower():
                    searched.append(i)

        mps = searched

    mps = sort_by_options(mps, options)
    main(mps)
