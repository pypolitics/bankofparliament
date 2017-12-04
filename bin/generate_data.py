#!/usr/bin/env python
# system libs
import locale, ast, os, operator, json, sys, pprint, re
from bs4 import BeautifulSoup
from optparse import OptionParser
import time
from datetime import datetime
from datetime import date

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
from categories.companies_house import CompaniesHouse
from utils import get_all_mps, get_request, get_house_of_commons_member

sys.path.append(os.path.abspath(os.path.expanduser('~/.apikeys')))
from apikeys import theyworkyou_apikey, companies_house_user

xml_data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'regmem2017-04-10.xml')

request_wait_time = 3600.0

class MemberOfParliament():
	def __init__(self, member, index=None, company_officers=True, company_filing=False, company_persons=True):
		"""Class holding the individual member of parliament"""
		print '\nProcessing : %s' % member['name'].decode('latin-1').encode("utf-8")

		start_time = time.time()

		self.index = str(index+1).zfill(3)
		self.mps = []

		self.company_officers = company_officers
		self.company_filing = company_filing
		self.company_persons = company_persons

		# list holding category classes
		self.categories = []

		# words that might identify a companieshouse officer as being an MP
		self.keywords = ['parliament', 'politician', 'politic', 'house of commons', ' mp ', 'honourable']

		# set the member
		self.setMember(member)

		# get more info on the member
		self.getPerson()

		# get full info on mp
		self.getMPInfo()

		# get a handle on member from : http://data.parliament.uk
		self.getExtendedData()

		# make sense of the html info, regarding registered intrests
		self.getMPIntrests()

		end_time = time.time()
		elapsed = end_time - start_time

		print '%s - %s %s (%s) %s - %s seconds' % (self.index, self.first_name, self.last_name, self.party, self.constituency, int(elapsed))

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
		request = get_request(url=url, user=None, headers={})

		# literal eval the json request into actual json
		full_info = ast.literal_eval(request.content)

		if full_info.has_key('eu_ref_stance'):
			self.eu_ref_stance = full_info['eu_ref_stance']
		else:
			self.eu_ref_stance = ''

		if full_info.has_key('facebook_page'):
			self.facebook = full_info['facebook_page']
		else:
			self.facebook = ''

		if full_info.has_key('twitter_username'):
			self.twitter = full_info['twitter_username']
		else:
			self.twitter = ''

		if full_info.has_key('wrans_departments'):
			self.wrans_departments = full_info['wrans_departments']
		else:
			self.wrans_departments = ''

		if full_info.has_key('wrans_subjects'):
			self.wrans_subjects = full_info['wrans_subjects']
		else:
			self.wrans_subjects = ''

		self.full_info = full_info

	def getExtendedData(self):
		"""Method to query data.parliament.uk for member"""

		self.extended = get_house_of_commons_member(self.constituency)
		y = get_house_of_commons_member(self.constituency, 'GovernmentPosts|BiographyEntries|Committees')

		self.extended['GovernmentPosts'] = y['GovernmentPosts']
		self.extended['BiographyEntries'] = y['BiographyEntries']
		self.extended['Committees'] = y['Committees']

		self.dob = 'Unknown Date of Birth'
		self.month = None
		self.year = None
		self.dods = y['@Dods_Id']

		if self.extended.has_key('DateOfBirth'):
			if type(self.extended['DateOfBirth']) == str:
				dob = datetime.strptime(self.extended['DateOfBirth'], '%Y-%m-%dT%H:%M:%S')
				self.dob = '%s %s' % (dob.strftime('%B'), dob.year)
				self.month = dob.month
				self.year = dob.year

		self.first = self.extended['BasicDetails']['GivenForename'].lower()
		self.last = self.extended['BasicDetails']['GivenSurname'].lower()
		self.display = self.extended['DisplayAs'].lower()

		self.middle = ''
		if self.extended['BasicDetails']['GivenMiddleNames']:
			self.middle = self.extended['BasicDetails']['GivenMiddleNames'].lower()

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
		headings["Shareholdings: over 15% of issued share capital"] = Shareholdings(extended=self.extended, keywords=self.keywords, month=self.month, year=self.year, first=self.first, middle=self.middle, last=self.last, display=self.display) #7 (i)
		headings["Other shareholdings, valued at more than"] = OtherShareholdings(extended=self.extended, keywords=self.keywords, month=self.month, year=self.year, first=self.first, middle=self.middle, last=self.last, display=self.display) #7 (ii)
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

		first_name = self.extended['BasicDetails']['GivenForename'].lower()
		last_name = self.extended['BasicDetails']['GivenSurname'].lower()
		display_as_name = self.extended['DisplayAs'].lower()

		middle_name = ''
		if self.extended['BasicDetails']['GivenMiddleNames']:
			middle_name = self.extended['BasicDetails']['GivenMiddleNames'].lower()

		# faked catergories, for ease of plotting later on
		self.salary = Salary(self.office, self.first_name, self.last_name, self.party)
		self.companieshouse = CompaniesHouse(month=self.month, year=self.year, first=first_name, middle=middle_name, last=last_name, display=display_as_name)

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
		self.categories.append(self.companieshouse)

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
	def total_annual(self):
		"""total annual of mp"""

		return self.total_income + self.total_gifts + self.total_donations

	@property
	def data(self):
		"""build a data dictionary of values required for dumping to json"""
		data = {}
		data['name'] = self.name
		data['party'] = self.party
		data['constituency'] = self.constituency
		data['dob'] = self.dob
		data['month'] = self.month
		data['year'] = self.year
		data['forname'] = self.first_name
		data['surname'] = self.last_name
		data['member_id'] = self.member_id
		data['person_id'] = self.person_id
		data['dods_id'] = self.dods
		data['eu_ref_stance'] = self.eu_ref_stance
		data['twitter'] = self.twitter
		data['facebook'] = self.facebook
		data['wrans_subjects'] = self.wrans_subjects
		data['wrans_departments'] = self.wrans_departments
		data['gender'] = self.extended['Gender']
		data['town_of_birth'] = self.extended['BasicDetails']['TownOfBirth']
		data['country_of_birth'] = self.extended['BasicDetails']['CountryOfBirth']
		data['extended'] = self.extended

		data['categories'] = []

		for category in self.categories:
			cat_data = category.data
			temp = []
			
			for item in category.items:
				temp.append(item.data)

			cat_data['items'] = temp
			data['categories'].append(cat_data)

		vals = self.name.split(' ')
		vals.append(self.constituency)
		vals.append(self.party)
		vals.append(data['eu_ref_stance'])

		for i in data['wrans_subjects'].split(' '):
			vals.append(i)
		for i in data['wrans_departments'].split(' '):
			vals.append(i)

		# government posts
		if self.extended['GovernmentPosts'] != None:
			data['government_posts'] = []

			# list
			if type(self.extended['GovernmentPosts']['GovernmentPost']) == list:
				for i in self.extended['GovernmentPosts']['GovernmentPost']:
					data['government_posts'].append(i['Name'])
					for gov in i['Name'].split(' '):
						vals.append(gov)
						# data['government_posts'].append(gov)

			# dict
			else:
				data['government_posts'].append(self.extended['GovernmentPosts']['GovernmentPost']['Name'])
				for i in self.extended['GovernmentPosts']['GovernmentPost']['Name'].split(' '):
					vals.append(i)
					# data['government_posts'].append(i)

		# biog entries
		if self.extended['BiographyEntries'] != None:
			data['biography_entries'] = []

			# list
			if type(self.extended['BiographyEntries']['BiographyEntry']) == list:
				for i in self.extended['BiographyEntries']['BiographyEntry']:
					data['biography_entries'].append(i['Entry'])
					for bio in i['Entry'].split(' '):
						vals.append(bio)
						# data['biography_entries'].append(bio)
			# dict
			else:
				data['biography_entries'].append(self.extended['BiographyEntries']['BiographyEntry']['Entry'])
				for i in self.extended['BiographyEntries']['BiographyEntry']['Entry'].split(' '):
					vals.append(i)
					# data['biography_entries'].append(i)

		# commitees
		if self.extended['Committees'] != None:
			data['commitees'] = []

			# list
			if type(self.extended['Committees']['Committee']) == list:
				for i in self.extended['Committees']['Committee']:
					data['commitees'].append(i['Name'])
					for com in i['Name'].split(' '):
						vals.append(com)
						# data['commitees'].append(com)
			# dict
			else:
				data['commitees'].append(self.extended['Committees']['Committee']['Name'])
				for i in self.extended['Committees']['Committee']['Name'].split(' '):
					vals.append(i)
					# data['commitees'].append(i)

		for mp in self.mps:
			mp_data = mp.data
			temp = []

			for appointment in mp.items:
				temp.append(appointment.data)

				for k in appointment.keywords:
					vals.append(k)

			mp_data['items'] = temp
			data['companies_house'].append(mp_data)

		data['keywords'] = vals
		data['mp_income'] = self.total_income
		data['mp_wealth'] = self.total_wealth
		data['mp_gifts'] = self.total_gifts
		data['mp_donations'] = self.total_donations
		data['mp_annual'] = self.total_annual

		# write out to file
		json_dump_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lib', 'data', 'members', '%s.json' % self.member_id)

		with open(json_dump_location, 'w') as jsonfile:
			json.dump(data, jsonfile, indent=3)
			print 'Writing : %s' % (json_dump_location)

		return data

def main(mps, options):
	"""main"""

	start_time = time.time()

	# fully parsed list of mps
	mp_list = []

	for member in mps:
		mp_list.append(MemberOfParliament(member, mps.index(member)).data)

	end_time = time.time()
	elapsed = end_time - start_time

	print ''
	if int(elapsed) < 60:
		print 'Total Time : %s seconds' % (int(elapsed))
	else:
		print 'Total Time : %s minutes' % (int(elapsed/60))

if __name__ == "__main__":
	parser = OptionParser()
	parser.add_option("--json", help="Dump to Json file", action="store_true", default=False)
	parser.add_option("--missing", help="Run for missing data files only", action="store_true", default=False)

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

	if options.missing:
		found = []
		json_dump_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lib', 'data', 'members')
		for mp in os.listdir(json_dump_location):
			mem_id = mp.split('.json')[0]
			found.append(mem_id)

		todo = []
		for m in mps:
			if m['member_id'] not in found:
				todo.append(m)

		mps = todo

	main(mps, options)
