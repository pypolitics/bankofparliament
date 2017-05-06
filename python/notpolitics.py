#!/usr/bin/env python
# system libs
import locale, ast, os, operator, json
from bs4 import BeautifulSoup
from optparse import OptionParser

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
from utils import get_all_mps, get_request

# locale.setlocale( locale.LC_ALL, '' )
theyworkyou_apikey = 'DLXaKDAYSmeLEBBWfUAmZK3j'
companies_house_user = 'ZCCtuxpY7uvkDyxLUz37dCYFIgke9PKfhMlEGC-Q'
xml_data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'regmem2017-04-10.xml')

request_wait_time = 3600.0

class MemberOfParliament():
	def __init__(self, member):
		"""Class holding the individual member of parliament"""

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

		print '%s %s (%s) %s' % (self.first_name, self.last_name, self.party, self.constituency)

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
		self.full_info = ast.literal_eval(request.content)

	def getMPIntrests(self):
		"""Method to parse the full_info variable"""

		# annoyingly, the data from theyworkforyou for the registered intrests
		# is in html, use BeautifulSoup to parse into regular text
		intrests = self.full_info['register_member_interests_html']
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

		data['mp_income'] = self.total_income
		data['mp_wealth'] = self.total_wealth
		data['mp_gifts'] = self.total_gifts
		data['mp_donations'] = self.total_donations
		data['mp_annual'] = self.total_annual

		return data

def main(mps, options):

	# fully parsed list of mps
	mps = [MemberOfParliament(member).data for member in mps]

	if options.json:
		# write out to file
		json_dump_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'json', 'members_dump.json')

		with open(json_dump_location, 'w') as jsonfile:
			json.dump(mps, jsonfile)

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
				if member.lower() in i['party'].lower():
					searched.append(i)
				if member.lower() in i['constituency'].lower():
					searched.append(i)

		mps = searched

	main(mps, options)

