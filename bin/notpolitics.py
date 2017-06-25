#!/usr/bin/env python
# system libs
import locale, ast, os, operator, json, sys, pprint
from bs4 import BeautifulSoup
from optparse import OptionParser

sys.path.append('../lib/python')

# local libs
from categories.employment import Employment
from categories.family import FamilyLobbyists, Family
from categories.miscellaneous import Miscellaneous
from categories.land_and_property import Property
from categories.shareholdings import OtherShareholdings, Shareholdings
from categories.gifts import GiftsOutsideUK, Gifts
from categories.visits import VisitsOutsideUK
from categories.donations import DirectDonations, IndirectDonations
from categories.salary import Salary
from categories.companies_house import CompaniesHouseUser
from utils import get_all_mps, get_request, get_house_of_commons_member
from companies import get_companies_house_users, get_appointments, get_companies, get_other_officers, get_filling_history, value_recurse, contains_mp

# locale.setlocale( locale.LC_ALL, '' )
theyworkyou_apikey = 'DLXaKDAYSmeLEBBWfUAmZK3j'
companies_house_user = 'ZCCtuxpY7uvkDyxLUz37dCYFIgke9PKfhMlEGC-Q'
xml_data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'regmem2017-04-10.xml')

request_wait_time = 3600.0

class MemberOfParliament():
	def __init__(self, member, index=None):
		"""Class holding the individual member of parliament"""

		self.index = index

		# list holding category classes
		self.categories = []

		# set the member
		self.setMember(member)

		# get more info on the member
		self.getPerson()

		# get full info on mp
		self.getMPInfo()

		# make sense of the html info, regarding registered intrests
		self.getMPIntrests()
		# print 'after getMPIntrests'
		# print '%s %s (%s) %s' % (self.first_name, self.last_name, self.party, self.constituency)

		self.getExtendedData()
		# print 'after getExtendedData'

		# print '\n%s %s (%s) %s [%s/%s]' % (self.first_name, self.last_name, self.party, self.constituency, len(self.mps), len(self.companies_users))
		# self.getMPExpenses()
		self.getMPCompanies()
		print '\n%s - %s %s (%s) %s [%s/%s]' % (self.index, self.first_name, self.last_name, self.party, self.constituency, len(self.mps), len(self.companies_users))
		return

		# return
		# print '%s %s (%s) %s [%s/%s]' % (self.first_name, self.last_name, self.party, self.constituency, len(self.companies_users), len(self.apps))

		for user in self.mps:
			if user['mp_found']:
				####################################################################################
				# print ''
				print '\t' + '*'*100
				print '\tCompanies House User'
				print '\t' + '*'*100
				print '\tName         : %s' % user['title']
				print '\tAddress      : %s' % user['address_snippet']
				# print 'MP           : %s' % user['mp_found']
				print '\tAPPOINTMENTS : %s' % len(user['appointments']['items'])
				print '\t' + '*'*100
				# print ''

				# for appointment in user['appointments']['items']:
				# 	####################################################################################
				# 	print '\n\t' + '-'*96
				# 	print '\tCompanies House Appointment'
				# 	print '\t' + '-'*96

				# 	company_status = appointment['appointed_to']['company_status'].title()
				# 	company_name = appointment['appointed_to']['company_name'].title()
				# 	officer_role = appointment['officer_role'].title()

				# 	print '\t%s, %s, %s' % (officer_role, company_name, company_status)

					# ####################################################################################
					# print '\n\t\t' + '-'*92
					# print '\t\tCompanies House Company'
					# print '\t\t' + '-'*92

					# address = 'N/A'
					# locality = 'N/A'
					# postal_code = 'N/A'

					# if appointment['company'].has_key('registered_office_address'):
					# 	if appointment['company']['registered_office_address'].has_key('address_line_1'):
					# 		address = appointment['company']['registered_office_address']['address_line_1']
					# 	if appointment['company']['registered_office_address'].has_key('locality'):
					# 		locality = appointment['company']['registered_office_address']['locality']
					# 	if appointment['company']['registered_office_address'].has_key('postal_code'):
					# 		postal_code = appointment['company']['registered_office_address']['postal_code']

					# print '\t\tRegistered Address : %s, %s, %s' % (address, locality, postal_code)
					# # pprint.pprint(appointment['companies'])
					# # if appointment['companies'].has_key('links'):
					# # 	print '\t\tLinks : %s' % appointment['companies']['links']

					# if appointment.has_key('other_officers'):
					# 	####################################################################################
					# 	print '\n\t\t' + '-'*92
					# 	print '\t\tCompanies House Company Officers'
					# 	print '\t\t' + '-'*92
					# 	for officer in appointment['other_officers']['items']:

					# 		officer_name = 'N/A'
					# 		officer_role = 'N/A'
					# 		officer_occupation = 'N/A'

					# 		if officer.has_key('name'):
					# 			officer_name = officer['name']
							
					# 		if officer.has_key('officer_role'):
					# 			officer_role = officer['officer_role']
							
					# 		if officer.has_key('occupation'):
					# 			officer_occupation = officer['occupation']

					# 		print '\t\t%s, %s, %s' % (officer_name, officer_role, officer_occupation)
					# 		# pprint.pprint(officer)

					# # pprint.pp

					# if appointment.has_key('filing_history'):
					# 	####################################################################################
					# 	print '\n\t\t' + '-'*92
					# 	print '\t\tCompanies House Company Filing History'
					# 	print '\t\t' + '-'*92

					# 	for filing in appointment['filing_history']['items']:

					# 		filing_category = filing['category']
					# 		description = filing['description']
					# 		date = filing['date']

					# 		print '\t\t%s, %s, %s' % (filing_category, description, date)

		# print ''

	def setMember(self, member):
		"""Set the member variables from the given member dictionary"""

		self.name = member['name'].decode('latin-1').encode("utf-8")
		self.member_id = member['member_id']
		self.person_id = member['person_id']
		self.party = member['party'].decode('latin-1').encode("utf-8")
		self.constituency = member['constituency'].decode('latin-1').encode("utf-8")

		if member.has_key('office'):
			self.office = member['office']
		else:
			self.office = None
			
	def getPerson(self):
		"""Method to set more variables"""

		url = 'https://www.theyworkforyou.com/api/getPerson?key=%s&id=%s&output=js' % (theyworkyou_apikey, self.person_id)
		request = get_request(url=url, user=None, headers={})

		# literal eval the json request into actual json
		self.person = ast.literal_eval(request.content)
		self.person = self.person[0]

		self.first_name = self.person['given_name'].decode('latin-1').encode("utf-8")
		self.last_name = self.person['family_name'].decode('latin-1').encode("utf-8")

	def getMPInfo(self):
		"""Method queries theyworkforyou again, for the full info on a given member of parliament"""
		
		url = 'https://www.theyworkforyou.com/api/getMPInfo?key=%s&id=%s&output=js' % (theyworkyou_apikey, self.person_id)
		# url = 'https://www.theyworkforyou.com/api/getMP?key=%s&constituency=%s&output=js' % (theyworkyou_apikey, self.constituency)

		request = get_request(url=url, user=None, headers={})

		# literal eval the json request into actual json
		self.full_info = ast.literal_eval(request.content)

	def getExtendedData(self):
		"""Method to parse the full_info variable"""

		self.extended = get_house_of_commons_member(self.constituency)

		if self.extended == {}:
			print '\tFAIL : %s' % self.name

	def getMPCompanies(self):
		"""Method to parse the full_info variable"""

		# these users are crudely sorted - needs more effort on this
		self.companies_users = get_companies_house_users(self.extended)
		self.mps = []

		for user in self.companies_users:

			# add appointments to user dict
			get_appointments(user)

			# add company to appointment dict
			get_companies(user)

			# now check for values which would make me think this person is a member of parliament
			# we have the user dict, the appointment dict and the company dict to search in
			vals = value_recurse(user, vals=[])

			if contains_mp(vals):
				user['mp_found'] = True
			else:
				user['mp_found'] = False
		
		# only select known mps
		for user in self.companies_users:
			if user['mp_found']:

				user = CompaniesHouseUser(user)

				self.mps.append(user)

		# for mp in self.mps:
		# 	# get other officers connected to the company
		# 	get_other_officers(mp)

		# 	# get the filing history of company
		# 	get_filling_history(mp)

	def getMPExpenses(self):
		"""Method to parse the full_info variable"""

		self.expenses = []
		for i in self.full_info.keys():
			if i.startswith('expenses'):
				self.expenses.append(i)

	def getMPIntrests(self):
		"""Method to parse the full_info variable"""

		# annoyingly, the data from theyworkforyou for the registered intrests
		# is in html, use BeautifulSoup to parse into regular text
		if self.full_info.has_key('register_member_interests_html'):
			intrests = self.full_info['register_member_interests_html']
		else:
			return

		soup = BeautifulSoup(intrests, 'html.parser')
		text = soup.text

		# split into lines for iteration
		splits = text.splitlines()

		# create a dictionary of search terms and the corresponding class to initialise when found
		headings = {}
		headings['Employment and earnings'] = Employment() # 1
		headings['Support linked to an MP but received by a local party organisation'] = IndirectDonations() # 2 (a)
		headings['Any other support not included in Category 2(a)'] = DirectDonations() # 2 (b)
		headings['Gifts, benefits and hospitality from UK sources'] = Gifts() # 3
		headings['Visits outside the UK'] = VisitsOutsideUK() # 4
		headings['Gifts and benefits from sources outside the UK'] = GiftsOutsideUK() # 5
		headings['Land and property portfolio'] = Property() # 6
		headings["Shareholdings: over 15% of issued share capital"] = Shareholdings(companies_house_user, names=[self.first_name, self.last_name]) #7 (i)
		headings["Other shareholdings, valued at more than"] = OtherShareholdings() #7 (ii)
		headings['Miscellaneous'] = Miscellaneous() # 8
		headings['Family members employed and paid from parliamentary expenses'] = Family() # 9
		headings['Family members engaged in lobbying'] = FamilyLobbyists() # 10

		# loop over the lines, if a heading (category) is found add subsequent
		# lines to that category class, until the next heading (category) is found

		# we use the keys of the dictionary above to define the category headings
		# the value of each search key is the relevant category class
		last_heading = None
		for i in splits:
			header = False
			for h in headings.keys():
				if h in i:
					header = True
					last_heading = h

			if header:
				pass
			else:
				if last_heading:
					# add the raw data entry to the category class
					headings[last_heading].add_entry(i)

		# now run the parse method of the category class, this parses the raw data text
		# generated by BeautifulSoup
		for each in headings.keys():
			headings[each].parse()

		# store dictionary values (classes), as MemberOfParliament class variable
		self.salary = Salary(self.office, self.first_name, self.last_name, self.party)

		self.employment = headings['Employment and earnings']
		self.indirect = headings['Support linked to an MP but received by a local party organisation']
		self.direct = headings['Any other support not included in Category 2(a)']
		self.gifts = headings['Gifts, benefits and hospitality from UK sources']
		self.visits_outside_uk = headings['Visits outside the UK'] 
		self.gifts_outside_uk = headings['Gifts and benefits from sources outside the UK'] 
		self.property = headings['Land and property portfolio']
		self.shareholdings = headings["Shareholdings: over 15% of issued share capital"]
		self.other_shareholdings = headings["Other shareholdings, valued at more than"]
		self.miscellaneous = headings['Miscellaneous']
		self.family = headings['Family members employed and paid from parliamentary expenses']
		self.family_lobbyists = headings['Family members engaged in lobbying']

		# append to categories list, iterable
		self.categories.append(self.employment)
		self.categories.append(self.indirect)
		self.categories.append(self.direct)
		self.categories.append(self.gifts)
		self.categories.append(self.visits_outside_uk)
		self.categories.append(self.gifts_outside_uk)
		self.categories.append(self.property)
		self.categories.append(self.shareholdings)
		self.categories.append(self.other_shareholdings)
		self.categories.append(self.miscellaneous)
		self.categories.append(self.family)
		self.categories.append(self.family_lobbyists)
		self.categories.append(self.salary)

	@property
	def total_wealth(self):
		"""total wealth of mp"""
		value = 0
		for category in self.categories:
			if category.category_wealth > 0:
				value += category.category_wealth
		return value

	@property
	def total_income(self):
		"""total income of mp"""
		value = 0
		for category in self.categories:
			if category.category_income > 0:
				value += category.category_income
		return value

	@property
	def total_gifts(self):
		"""total gifts of mp"""
		value = 0
		for category in self.categories:
			if category.category_gifts > 0:
				value += category.category_gifts
		return value

	@property
	def total_donations(self):
		"""total donations of mp"""
		value = 0
		for category in self.categories:
			if category.category_donations > 0:
				value += category.category_donations

		return value

	@property
	def total_expenses(self):
		"""total expenses of mp"""
		value = 0
		# for category in self.categories:
		# 	if category.expenses > 0:
		# 		value += category.expenses
		return value

	@property
	def total_annual(self):
		"""total annual of mp"""

		return self.total_income + self.total_gifts + self.total_expenses + self.total_donations

	@property
	def data(self):
		"""build a data dictionary of values required for dumping to json"""
		data = {}
		data['name'] = self.name
		data['party'] = self.party
		data['constituency'] = self.constituency
		data['forname'] = self.first_name
		data['surname'] = self.last_name
		data['member_id'] = self.member_id
		data['person_id'] = self.person_id

		data['categories'] = []

		for category in self.categories:
			cat_data = category.data
			temp = []
			
			for item in category.items:
				temp.append(item.data)

			cat_data['items'] = temp
			data['categories'].append(cat_data)

		data['companies_house'] = []

		for mp in self.mps:
			mp_data = mp.data
			temp = []

			for appointment in mp.items:
				temp.append(appointment.data)

			mp_data['items'] = temp
			data['companies_house'].append(mp_data)

		data['mp_income'] = self.total_income
		data['mp_wealth'] = self.total_wealth
		data['mp_gifts'] = self.total_gifts
		data['mp_donations'] = self.total_donations
		data['mp_annual'] = self.total_annual

		return data

def main(mps, options):

	# fully parsed list of mps
	# mps = [MemberOfParliament(member).data for member in mps]
	mp_list = []
	for member in mps:
		mp_list.append(MemberOfParliament(member, mps.index(member)).data)

	mps = mp_list

	if options.json:
		# write out to file
		json_dump_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lib', 'data', 'members_dump.json')

		with open(json_dump_location, 'w') as jsonfile:
			json.dump(mps, jsonfile)

		import pprint
		# pprint.pprint(mps)

if __name__ == "__main__":
	parser = OptionParser()
	parser.add_option("--json", help="Dump to Json file", action="store_true", default=True)

	# parse the comand line
	(options, args) = parser.parse_args()

	# return a list (of dicts) of mps
	mps = get_all_mps(theyworkyou_apikey)
	searched = []

	# TODO: fix this crude arg porser
	if args:
		for member in args:
			for i in mps:
				if member.lower() in i['name'].lower():
					searched.append(i)
				elif member.lower() in i['party'].lower():
					searched.append(i)
				elif member.lower() in i['constituency'].lower():
					searched.append(i)

		mps = searched

	main(mps, options)

