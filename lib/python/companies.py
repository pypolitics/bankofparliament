# -*- coding: utf-8 -*-
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

from utils import get_request

# system libs
import requests, time, ast, locale, pprint, re, shutil, os
from datetime import datetime
import xml.etree.cElementTree as ElementTree
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

companies_house_user = 'ZCCtuxpY7uvkDyxLUz37dCYFIgke9PKfhMlEGC-Q'

def get_companies_house_users(member):
	"""Get data from companies house"""

	# id
	member_id = member['@Member_Id']

	# names
	first_name = member['BasicDetails']['GivenForename'].lower()
	last_name = member['BasicDetails']['GivenSurname'].lower()
	# print type(first_name)
	# print type(last_name)
	# print first_name, last_name

	first_name = first_name
	last_name = last_name
	names = [first_name, last_name]
	# print names
	# party / constituency
	party = member['Party']['#text']
	constituency = member['MemberFrom']

	# ADDRESSES
	# get all the addresses
	addresses = member['Addresses']['Address']
	physical_addresses = []

	if type(addresses) == dict:
		addresses = [addresses]

	for i in addresses:
		if i['IsPhysical'] == 'True':
			address = {}

			for k in i.keys():
				# x = x.lower().replace(',','')
				if i[k]:
					if k.startswith('Address'):
						for x in i[k].split(' '):
							x = x.lower().replace(',','')
							if x not in physical_addresses:
								physical_addresses.append(x)
					if k == 'Postcode':
						physical_addresses.append(i[k])
						for x in i[k].split(' '):
							x = x.lower().replace(',','')
							if x not in physical_addresses:
								physical_addresses.append(x)

	# NAMES
	# get all the names
	basic_details = member['BasicDetails']
	middle_name = ''
	if member['BasicDetails']['GivenMiddleNames']:
		middle_name = member['BasicDetails']['GivenMiddleNames'].lower()
		names.append(member['BasicDetails']['GivenMiddleNames'].lower())

	list_as = ''
	if member['ListAs']:
		for x in member['ListAs'].split(' '):
			x = x.lower().replace(',','')
			list_as = x
			if x not in names:
				names.append(x)

	full_title = ''
	if member['FullTitle']:
		for x in member['FullTitle'].split(' '):
			x = x.lower().replace(',','')
			full_title = x
			if x not in names:
				names.append(x)

	display_as = ''
	if member['DisplayAs']:
		for x in member['DisplayAs'].split(' '):
			x = x.lower().replace(',','')
			display_as = x
			if x not in names:
				names.append(x)

	preferred_names = member['PreferredNames']['PreferredName']
	if type(preferred_names) == dict:
		preferred_names = [preferred_names]
	
	for i in preferred_names:

		if i['AddressAs']:
			for x in i['AddressAs'].split(' '):
				x = x.lower().replace(',','')
				if x not in names:
					names.append(x)

		if i['Forename']:
			for x in i['Forename'].split(' '):
				x = x.lower().replace(',','')
				if x not in names:
					names.append(x)

		if i['HonouraryPrefixes']:
			# print i['HonouraryPrefixes']
			if type(i['HonouraryPrefixes']['HonouraryPrefix']) == list:
				for x in i['HonouraryPrefixes']['HonouraryPrefix']:
					x = x['Name'].lower().replace(',','')
					if x not in names:
						names.append(x)
			else:
				names.append(i['HonouraryPrefixes']['HonouraryPrefix']['Name'])

		if i['MiddleNames']:
			for x in i['MiddleNames'].split(' '):
				x = x.lower().replace(',','')
				if x not in names:
					names.append(x)

		if i['Surname']:
			for x in i['Surname'].split(' '):
				x = x.lower().replace(',','')
				if x not in names:
					names.append(x)

		if i['Title']:
			for x in i['Title'].split(' '):
				x = x.lower().replace(',','')
				if x not in names:
					names.append(x)

		if i['Suffix']:
			for x in i['Suffix'].split(' '):
				x = x.lower().replace(',','')
				if x not in names:
					names.append(x)

	for i in names:
		if ' ' in i:
			spl = i.split(' ')
			for s in spl:
				names.append(s)
			names.remove(i)

	remove = ['mp', 'mr', 'mrs', 'miss', 'ms']
	for i in names:
		if i in remove:
			names.remove(i)

	# get the date of birth
	dob = member['DateOfBirth']

	#############################################################################################################################
	# basic search
	if middle_name != '':
		url = 'https://api.companieshouse.gov.uk/search/officers?q=%s+%s+%s&items_per_page=100' % (first_name, middle_name, last_name)
	else:
		url = 'https://api.companieshouse.gov.uk/search/officers?q=%s+%s&items_per_page=100' % (first_name, last_name)

	url = url.replace(' ', '+')

	# r = requests.get(url, auth=(companies_house_user, ''))

	r = get_request(url=url, user=companies_house_user, headers={})

	data = r.json()

	data = decoded(data)

	data = filter_by_first_last_name(data, first_name, middle_name, last_name)
	data = filter_by_appointment_counts(data)
	data = fuzzy_filter(data, first_name, middle_name, last_name, addresses)

	# these are the matched companieshouse users - queried by name only, filtered a little bit
	return data


def contains_mp(vals):

	search_for = ['parliament', 'politician', 'commons']

	for search in search_for:
		for v in vals:
			if search in v.lower():
				# print 'MP FOUND! : %s' % v
				return True
	return False


def value_recurse(data, vals=[]):

	# make data a list
	if isinstance(data, dict):
		data = [data]
	elif isinstance(data, list):
		data = data
	else:
		data = [data]

	# list of dicts
	for d in data:

		# ok, data is a list, but what of its contents
		if isinstance(d, dict):
			for k, v in d.iteritems():

				if isinstance(v, dict):
					value_recurse([v], vals)
				elif isinstance(v, list):
					value_recurse(v, vals)
				else:
					vals.append(str(v))

		elif isinstance(d, list):
			value_recurse(d, vals)
		
		else:
			vals.append(str(d))

	return vals


def decoded(data):
	for i in data['items']:
		# print i['title'], type(i['title'])
		i['title'].encode('utf-8')

	return data

def fuzzy_filter(data, first_name, middle_name, last_name, addresses):

	ratio_threshold = 90

	top_ratio = []
	for i in data:

		title = i['title'].lower()
		name = '%s %s' % (first_name, last_name)
		if middle_name != '':
			name = '%s %s %s' % (first_name, middle_name, last_name)

		ratio = fuzz.token_sort_ratio(name, title)

		if int(ratio) >= ratio_threshold:
			i['fuzzy_ratio'] = ratio
			top_ratio.append(i)
	
	return top_ratio

def filter_by_first_last_name(data, first_name, middle_name, last_name):

	matched_people = []

	for i in data['items']:
		# print i['title'], type(i['title']), first_name, last_name
		if first_name in i['title'].lower():
			# if middle_name in i['title'].lower():
			if last_name in i['title'].lower():
				matched_people.append(i)

	return matched_people

def filter_by_appointment_counts(data, count=0):

	matched_people = []

	for i in data:

		if i['appointment_count'] > count:
			matched_people.append(i)

	return matched_people

def get_other_officers(user):

	for appointment in user['appointments']['items']:
		if appointment['company'].has_key('links'):

			links = appointment['company']['links']
			if links.has_key('officers'):

				other_officers_link = links['officers']

				url = 'https://api.companieshouse.gov.uk%s' % other_officers_link
				# other_officers = requests.get(url, auth=(companies_house_user, ''))
				other_officers = get_request(url=url, user=companies_house_user, headers={})


				try:
					other_officers = other_officers.json()

					appointment['other_officers'] = other_officers
				
				except:
					pass

def get_filling_history(user):
	# query company for filing_history

	for appointment in user['appointments']['items']:
		if appointment['company'].has_key('links'):

			links = appointment['company']['links']

			if links.has_key('filing_history'):

				filing_history_link = links['filing_history']

				url = 'https://api.companieshouse.gov.uk%s' % filing_history_link
				# filing_history = requests.get(url, auth=(companies_house_user, ''))
				filing_history = get_request(url=url, user=companies_house_user, headers={})


				try:
					filing_history = filing_history.json()
					appointment['filing_history'] = filing_history
				
				except:
					pass

def get_companies(user):
	# query for company of appointment, store under 'company' key of appointment dict

	for appointment in user['appointments']['items']:

		company_number = appointment['appointed_to']['company_number']
		url = 'https://api.companieshouse.gov.uk/company/%s' % company_number

		# companies = requests.get(url, auth=(companies_house_user, ''))
		companies = get_request(url=url, user=companies_house_user, headers={})

		
		try:
			companies = companies.json()
			appointment['company'] = companies
		
		except:
			appointment['company'] = {}
			appointment['company']['items'] = []

def get_appointments(user):
	# query for appointments and store under 'appointments' key of user dict

	self_link = user['links']['self']
	url = 'https://api.companieshouse.gov.uk%s' % self_link

	# appointments = requests.get(url, auth=(companies_house_user, ''))
	appointments = get_request(url=url, user=companies_house_user, headers={})

	
	try:
		appointments = appointments.json()
		user['appointments'] = appointments

	except:
		user['appointments'] = {}
		user['appointments']['items'] = []
