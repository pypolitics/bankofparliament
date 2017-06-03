#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, os, operator, locale, pprint
from optparse import OptionParser
from utils import get_companies_house_person, get_request, filter_by_first_last_name, filter_by_appointment_counts, get_appointments

locale.setlocale( locale.LC_ALL, '' )

json_dump_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'json', 'members_dump.json')
images_directory = os.path.join(os.path.dirname(__file__), '..', 'images')
companies_house_user = 'ZCCtuxpY7uvkDyxLUz37dCYFIgke9PKfhMlEGC-Q'

def main(mps, options):
	"""
	Main
	"""
	mps = sort_by_options(mps, options)

	feeback(mps, options)


def feeback(mps, options):
	""""""

	# now print by options specified on commandline
	for member in mps:
		name = member['name']
		income = locale.currency(member['mp_income'], grouping=True)
		wealth = locale.currency(member['mp_wealth'], grouping=True)
		gifts = locale.currency(member['mp_gifts'], grouping=True)
		donations = locale.currency(member['mp_donations'], grouping=True)
		annual = locale.currency(member['mp_annual'], grouping=True)
		forname = member['forname']
		surname = member['surname']
		member_id = member['member_id']

		names = [forname, surname, name]

		print '*'*150
		print name, '(' + member['party'] + ')', member['constituency']
		print 'Income :', income, ' |  Wealth :', wealth, ' |  Gifts :', gifts, ' |  Donations :', donations, ' |  Annual :', annual
		print os.path.abspath(os.path.join(images_directory, '%s_%s_%s.png' % (forname, surname, member_id)))
		print '*'*150
		print ''

		print_register_of_intrests(member)

		data = get_companies_house_person(user=companies_house_user, names=names, addresses=[])
		data = filter_by_first_last_name(data, forname, surname, name)
		data = filter_by_appointment_counts(data)
		data = get_appointments(user=companies_house_user, data=data, status=['active'])

		print_companies_house_info(data)

		# now we have an idea of the active appointments of people with the exact same
		# name as the member of parliament

		# we should check with the shareholding data in the member dictionary
		# it's a start at least

def print_register_of_intrests(member):
	"""
	Function to print out the register of intrests
	"""
	for category in member['categories']:

		category_amount = category['category_amount']

		# if its currency, format it
		if category['isCurrency']:
			print '\t', category['category_description'], '', locale.currency(category_amount, grouping=True)
		else:
			print '\t', category['category_description']


		for item in category['items']:

			item_amount = item['amount']

			if category['isCurrency']:
				print '\t\t', item['pretty'], locale.currency(item_amount, grouping=True)
			else:
				print '\t\t', item['pretty']

def print_companies_house_info(data):
	"""
	Function to print out companies house matches
	"""

	print '-'*100
	print 'Companies House Lookup'
	print '-'*100
	print ''
	for matched_person in data:
		print matched_person['title']
		print matched_person['appointments']
		for status in matched_person['appointments'].keys():

			active_appointments = matched_person['appointments'][status]

			for app in active_appointments:

				role = app['officer_role']
				company_links = app['links']
				company_name = app['appointed_to']['company_name']
				company_number = app['appointed_to']['company_number']
				company_status = app['appointed_to']['company_status']
				
				if app.has_key('resigned_on'):
					resigned_on = app['resigned_on']
				else:
					resigned_on = None
				if app.has_key('occupation'):
					occupation = app['occupation']
				else:
					occupation = None

				address_string = ''
				address = app['address']
				keys = ['address_line_1', 'address_line_2', 'locality', 'postal_code']

				for k in keys:
					if address.has_key(k):
						address_string += '%s, ' % address[k]


				print '\t%s, %s, %s' % (company_name, company_status, role)
				print '\t\t%s' % address_string


def sort_by_options(mps, options):
	"""
	Sort by options
	"""

	# sort by options specified on commandline
	if options.sortby == 'wealth':
		mps = sorted(mps, key=operator.itemgetter('mp_wealth'), reverse=False)
	
	elif options.sortby == 'income':
		mps = sorted(mps, key=operator.itemgetter('mp_income'), reverse=False)
	
	elif options.sortby == 'gifts':
		mps = sorted(mps, key=operator.itemgetter('mp_gifts'), reverse=False)
	
	elif options.sortby == 'donations':
		mps = sorted(mps, key=operator.itemgetter('mp_donations'), reverse=False)		

	elif options.sortby == 'annual':
		mps = sorted(mps, key=operator.itemgetter('mp_annual'), reverse=False)	

	else:
		mps = sorted(mps, key=operator.itemgetter('%s' % options.sortby), reverse=False)

	return mps

def read_json_file():
	"""
	Read file from json_dump_location
	"""
	with open(json_dump_location) as json_data:
		return json.load(json_data)

if __name__ == "__main__":
	"""
	Commandline run
	"""
	parser = OptionParser()

	# parser.add_option("--summary", help="Summary print", action="store_true", default=True)
	# parser.add_option("--detailed", help="Detailed print", action="store_true", default=False)
	parser.add_option("--sortby", help="Sort By", action="store", default='income')

	# parse the comand line
	(options, args) = parser.parse_args()

	# return a list (of dicts) of mps
	mps = read_json_file()
	# print mps

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

	main(mps, options)
