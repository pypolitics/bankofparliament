#!/usr/bin/env python
# -*- coding: utf-8 -*-

# thirdparty libs
import igraph as ig
import plotly.offline as offline
import plotly.plotly as py
from plotly.graph_objs import *
from optparse import OptionParser
import os, sys, json
import operator, copy
from fuzzywuzzy import fuzz
import textwrap

sys.path.append('../lib/python')
from constants import PARTY_COLOURS
from plotting import plot_3d_data_to_file
from plot_utils import clean_name, make_node, make_link

orange_darker = '#f7a55d'
orange_lighter = '#fac99e'

yellow_darker = '#fff570'
yellow_lighter = '#fff899'

pink_darker = '#ffbaf4'
pink_lighter = 'rgb(255, 235, 251)'

grey_darker = '#b8bab8'
grey_lighter = '#d8dad8'
grey_lighter_white = '#e5e6e5'

green_darker = '#00ff99'
green_lighter = '#4dffb8'

dark_blue = '#9966ff'

data_lines = {
				'line' : {'color' : grey_darker, 'opacity' : 0.2, 'size' : 8, 'name' : None},
				}

data_nodes = {  'mp'                : {'color' : 'black', 'opacity' : 1, 'size' : 20, 'symbol' : 'circle'},

				'visit_company'              : {'color' : dark_blue, 'opacity' : 1, 'size' : 10, 'symbol' : 'diamond'},
				'visit_person'              : {'color' : dark_blue, 'opacity' : 1, 'size' : 10, 'symbol' : 'circle'},

				'gift_company'              : {'color' : dark_blue, 'opacity' : 1, 'size' : 10, 'symbol' : 'diamond'},
				'gift_person'              : {'color' : dark_blue, 'opacity' : 1, 'size' : 10, 'symbol' : 'circle'},

				'donor_company'              : {'color' : dark_blue, 'opacity' : 1, 'size' : 10, 'symbol' : 'diamond'},
				'donor_company_resigned'     : {'color' : grey_darker, 'opacity' : 1, 'size' : 10, 'symbol' : 'diamond'},
				'donor_company_dissolved'    : {'color' : grey_darker, 'opacity' : 1, 'size' : 10, 'symbol' : 'diamond'},
				'donor_person'               : {'color' : dark_blue, 'opacity' : 1, 'size' : 10, 'symbol' : 'circle'},
				'donor_company_officer'      : {'color' : grey_darker, 'opacity' : 0.2, 'size' : 10, 'symbol' : 'circle'},

				'declared_company'              : {'color' : green_darker, 'opacity' : 1, 'size' : 10, 'symbol' : 'diamond'},
				'undeclared_company'            : {'color' : orange_darker, 'opacity' : 1, 'size' : 10, 'symbol' : 'diamond'},
				'undeclared_active_company'     : {'color' : 'red', 'opacity' : 1, 'size' : 10, 'symbol' : 'diamond'},
				'undeclared_inactive_company'   : {'color' : grey_darker, 'opacity' : 0.5, 'size' : 10, 'symbol' : 'diamond'},

				'active_person'           : {'color' : yellow_darker, 'opacity' : 0.5, 'size' : 5, 'symbol' : 'circle'},
				'inactive_person'           : {'color' : grey_darker, 'opacity' : 0.5, 'size' : 5, 'symbol' : 'circle'},
				'active_officer'           : {'color' : orange_darker, 'opacity' : 0.5, 'size' : 5, 'symbol' : 'circle'},
				'inactive_officer'           : {'color' : grey_darker, 'opacity' : 0.5, 'size' : 5, 'symbol' : 'circle'},

				}

def reverse_name(name):

	if ', ' in name:
		spl = name.split(', ')
		return '%s %s' % (spl[1], spl[0])
	else:
		return name

def main(mps):
	"""
	"""

	data = {'nodes' : [], 'links' : []}

	for mp in mps:
		print '\nProcessing Plot : %s' % mp['name']
		person_id = mp['person_id']
		
		hyperlink = 'https://www.theyworkforyou.com/mp/%s#register' % person_id

		# get main node
		splits = mp['name'].split(' ')
		first = splits[0]
		last = ' '.join(splits[1:])

		# for some reason, cant do html formatting for 3d scatter plots
		label = '%s %s' % (first, last)
		label = ''

		node_main = make_node(data_nodes['mp'], name=label, hovertext='<b>%s</b>' % mp['name'], node_type='mp', hyperlink=None)
		node_main_copy = copy.copy(node_main)
		node_main_copy['color'] = PARTY_COLOURS[mp['party'].lower()]
		data['nodes'].append(node_main_copy)

		for category in mp['categories']:

			valid_categories = ['shareholding', 'companies', 'visit', 'gift', 'donation']

			# if 'shareholding' in category['category_type'] or 'companies' in category['category_type'] or 'visit' in category['category_type'] or 'gift' in category['category_type'] or 'donation' in category['category_type']:
			if 'shareholding' in category['category_type'] or 'visit' in category['category_type'] or 'gift' in category['category_type'] or 'donation' in category['category_type']:

				for item in category['items']:
					url = item['link']

					# textwrap the hovertext
					pretty = item['pretty']
					wrapped = textwrap.wrap(pretty, 50)

					# build the tooltip
					hovertext = ''
					hovertext += '</br>'
					if item.has_key('status'):

						hovertext += '</br><b>Donor Name:</b> %s' % item['donor'].title()

						if item['company'].has_key('company_number'):
							if item['company']['company_number'] != 'N/A':
								hovertext += '</br><b>Donor Company Number:</b> %s' % item['company']['company_number']

					else:
						if item['company'].has_key('company_name'):
							hovertext += '</br><b>Company Name:</b> %s' % item['company']['company_name'].title()
						if item['company'].has_key('company_number'):
							hovertext += '</br><b>Company Number:</b> %s' % item['company']['company_number']

					# find the correct node type, there are lots now...
					if 'companies' in category['category_type']:
						if item['company']['company_status'] == 'active':
							n = 'undeclared_active_company'
						else:
							n = 'undeclared_inactive_company'
						n = 'declared_company'

					elif 'visit' in category['category_type']:
						n = 'visit_company'

					elif 'donation' in category['category_type'] or 'gift' in category['category_type']:
						if 'individual' in item['status']:
							n = 'donor_person'
						else:
							n = 'donor_company'

					elif 'shareholding' in category['category_type']:
						n = 'declared_company'

					wrapped = textwrap.wrap(item['company']['company_name'], 60)
					label = wrapped[0].title()
					label = ''

					item_node = make_node(data_nodes[n], name=label, hovertext=hovertext, node_type=category, hyperlink=url)
					item_copy = copy.copy(item_node)
					item_copy['amount'] = item['amount']

					# hyperlinked node - add a border
					if url != 'https://beta.companieshouse.gov.uk':
						item_copy['border_style'] = {'color' : 'gray', 'size' : 2}

					found = False
					for each in data['nodes']:
						if hovertext == each['hovertext']:
							item_copy = each
							item_copy['size'] += 1
							found = True

					if not found:
						data['nodes'].append(item_copy)

					link = make_link(data_lines['line'], nodes = data['nodes'], source=node_main_copy, target=item_copy)
					l = copy.copy(link)
					if l not in data['links']:
						data['links'].append(l)

					# ################################################################################################################
					# # COMPANIES HOUSE STUFF ONLY
					# # significant persons
					# if item.has_key('persons'):

					# 	for person in item['persons']:

					# 		name = clean_name(person['name'])
					# 		name = reverse_name(name)
					# 		hovertext = '%s' % name.title()
					# 		label = name.title()
					# 		label = ''

					# 		if url:
					# 			url = item['link'] + '/persons-with-significant-control/'

					# 		if person.has_key('ceased_on'):
					# 			n = 'inactive_person'
					# 		else:
					# 			n = 'active_person'

					# 		person_node = make_node(data_nodes[n], name=label, hovertext=hovertext, node_type=category, hyperlink=url)
					# 		person_copy = copy.copy(person_node)

					# 		# fuzzy logic a cleaned name for match with mp
					# 		# set our threshold at 90%
					# 		ratio = fuzz.token_set_ratio(name, mp['name'])

					# 		if ratio > 90:
					# 			person_copy['color'] = PARTY_COLOURS[mp['party'].lower()]
					# 			person_copy['opacity'] = 1

					# 			# lets check they dont already exist
					# 		found = person_copy
					# 		for each in data['nodes']:
					# 			if fuzz.token_set_ratio(hovertext, each['hovertext']) >= 90:
					# 				found = each
					# 				if not each['node_type'] == 'mp':
					# 					each['size'] += 3

					# 		if found == person_copy:
					# 			data['nodes'].append(found)

					# 		link = make_link(data_lines['line'], nodes = data['nodes'], source=item_copy, target=found)
					# 		l = copy.copy(link)
					# 		if l not in data['links']:
					# 			data['links'].append(l)

					# if item.has_key('officers'):

					# 	for person in item['officers']:

					# 		if person.has_key('resigned_on'):
					# 			n = 'inactive_person'
					# 		else:
					# 			n = 'active_person'

					# 		name = clean_name(person['name'])
					# 		name = reverse_name(name)
					# 		hovertext = '%s' % name.title()
					# 		label = ''

					# 		if url:
					# 			url = 'https://beta.companieshouse.gov.uk/' + person['links']['officer']['appointments']

					# 		person_node = make_node(data_nodes[n], name=label, hovertext=hovertext, node_type=category, hyperlink=url)
					# 		person_copy = copy.copy(person_node)

					# 		# fuzzy logic a cleaned name for match with mp
					# 		# set our threshold at 90%
					# 		ratio = fuzz.token_set_ratio(name, mp['name'])

					# 		if ratio > 90:
					# 			person_copy['color'] = PARTY_COLOURS[mp['party'].lower()]
					# 			person_copy['opacity'] = 1

					# 		# lets check they dont already exist
					# 		found = person_copy
					# 		for each in data['nodes']:
					# 			if fuzz.token_set_ratio(hovertext, each['hovertext']) >= 90:
					# 				found = each
					# 				if not each['node_type'] == 'mp':
					# 					each['size'] += 3

					# 		# found hasnt changed - so, no match was make, add the node
					# 		if found == person_copy:
					# 			data['nodes'].append(found)

					# 		link = make_link(data_lines['line'], nodes = data['nodes'], source=item_copy, target=found)
					# 		l = copy.copy(link)
					# 		if l not in data['links']:
					# 			data['links'].append(l)

					# if item.has_key('appointments'):
					# 	for appointment in item['appointments']:

					# 		url = item['link']

					# 		hovertext = ''
					# 		hovertext += '</br>'
					# 		if appointment['appointed_to'].has_key('company_name'):
					# 			hovertext += '</br><b>Donor Company:</b> %s' % appointment['appointed_to']['company_name'].title()

					# 		if appointment['appointed_to'].has_key('company_number'):
					# 			hovertext += '</br><b>Donor Company Number:</b> %s' % appointment['appointed_to']['company_number']

					# 		if appointment['appointed_to'].has_key('company_status'):
					# 			if appointment['appointed_to']['company_status'].lower() != 'active':
					# 				n = 'donor_company_dissolved'
					# 			else:
					# 				n = 'donor_company'

					# 		if appointment.has_key('resigned_on'):
					# 			n = 'donor_company_dissolved'

					# 		label = ''

					# 		app_node = make_node(data_nodes[n], name=label, hovertext=hovertext, node_type=category, hyperlink=url)
					# 		app_copy = copy.copy(app_node)

					# 		found = False
					# 		for each in data['nodes']:
					# 			if hovertext == each['hovertext']:
					# 				app_copy = each
					# 				found = True

					# 		if not found:
					# 			data['nodes'].append(app_copy)

					# 		link = make_link(data_lines['line'], nodes = data['nodes'], source=item_copy, target=app_copy)
					# 		l = copy.copy(link)
					# 		if l not in data['links']:
					# 			data['links'].append(l)


					# 		# OFFICERS OF APPOINTMENT
					# 		for person in appointment['officers']:

					# 			if person.has_key('resigned_on'):
					# 				n = 'inactive_person'
					# 			else:
					# 				n = 'active_person'

					# 			name = clean_name(person['name'])
					# 			name = reverse_name(name)
					# 			hovertext = '%s' % name.title()
					# 			label = ''

					# 			if url:
					# 				url = 'https://beta.companieshouse.gov.uk/' + person['links']['officer']['appointments']

					# 			person_node = make_node(data_nodes['donor_company_officer'], name=label, hovertext=hovertext, node_type=category, hyperlink=url)
					# 			person_copy = copy.copy(person_node)

					# 			# fuzzy logic a cleaned name for match with mp
					# 			# set our threshold at 90%
					# 			ratio = fuzz.token_set_ratio(name, mp['name'])

					# 			if ratio > 90:
					# 				person_copy['color'] = PARTY_COLOURS[mp['party'].lower()]
					# 				person_copy['opacity'] = 1

					# 			# lets check they dont already exist
					# 			found = person_copy
					# 			for each in data['nodes']:
					# 				if fuzz.token_set_ratio(hovertext, each['hovertext']) >= 90:
					# 					found = each
					# 					if not each['node_type'] == 'mp':
					# 						each['size'] += 2

					# 			# found hasnt changed - so, no match was make, add the node
					# 			if found == person_copy:
					# 				data['nodes'].append(found)

					# 			link = make_link(data_lines['line'], nodes = data['nodes'], source=app_copy, target=found)
					# 			l = copy.copy(link)
					# 			if l not in data['links']:
					# 				data['links'].append(l)

					# 		for person in appointment['persons_with_significant_control']:

					# 			name = clean_name(person['name'])
					# 			name = reverse_name(name)
					# 			hovertext = '%s' % name.title()
					# 			label = name.title()
					# 			label = ''

					# 			if url:
					# 				url = item['link'] + '/persons-with-significant-control/'

					# 			if person.has_key('ceased_on'):
					# 				n = 'inactive_person'
					# 			else:
					# 				n = 'active_person'

					# 			person_node = make_node(data_nodes[n], name=label, hovertext=hovertext, node_type=category, hyperlink=url)
					# 			person_copy = copy.copy(person_node)

					# 			# fuzzy logic a cleaned name for match with mp
					# 			# set our threshold at 90%
					# 			ratio = fuzz.token_set_ratio(name, mp['name'])

					# 			if ratio > 90:
					# 				person_copy['color'] = PARTY_COLOURS[mp['party'].lower()]
					# 				person_copy['opacity'] = 1

					# 				# lets check they dont already exist
					# 			found = person_copy
					# 			for each in data['nodes']:
					# 				if fuzz.token_set_ratio(hovertext, each['hovertext']) >= 90:
					# 					found = each
					# 					if not each['node_type'] == 'mp':
					# 						each['size'] += 2

					# 			if found == person_copy:
					# 				data['nodes'].append(found)

					# 			link = make_link(data_lines['line'], nodes = data['nodes'], source=item_copy, target=found)
					# 			l = copy.copy(link)
					# 			if l not in data['links']:
					# 				data['links'].append(l)


	plot_3d_data_to_file(data, '','', '', 'All MPs', 'All Constituencies', 'All Parties', '')

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
	parser.add_option("--from_index", help="Carry on from index", action="store", default=0)


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

	if options.from_index:
		# index the list from a given int
		mps = mps[int(options.from_index):]

	main(mps)
