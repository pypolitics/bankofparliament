# local libs

from categories import Category
import pprint
from items import ShareholdingsItem
from companies_house_query import CompaniesHouseUserSearch, CompaniesHouseCompanySearch, CompaniesHouseOfficer
from constants import KEYWORDS
from utils import get_request, getlink, filter_by_name_string
from fuzzywuzzy import fuzz

base_url = 'https://beta.companieshouse.gov.uk'

class CompaniesHouse(Category):
	def __init__(self, month, year, first, middle, last, display):
		"""
		Companies House User
		"""

		self.month = month
		self.year = year
		self.first = first
		self.middle = middle
		self.last = last
		self.display = display

		self.names = ['%s %s' % (first, last)]
		if not self.display in self.names:
			self.names.append(self.display)
		if middle != '':
			self.names.append('%s %s %s' % ( first, middle, last))

		self.items = []

		# category info
		self.category_type = 'companies_house'
		self.category_id = 14
		self.category_description = 'Companies House'
		self.isCurrency = False

		self.category_income = 0
		self.category_wealth = 0
		self.category_gifts = 0
		self.category_donations = 0
		self.category_amount = 0

		self.do_logic()

	def do_logic(self):
		"""
		OK. Here we need to do two separate things, look for officers that match the name and for companies that match the name.

		ADD TO SELF.ITEMS

		"""

		next_id = len(self.items) + 1
		item_id = '%04d' % next_id

		companies = CompaniesHouseCompanySearch(self.names)
		companies.get_data(keywords=KEYWORDS, month=self.month, year=self.year, first=self.first, middle=self.middle, last=self.last, display=self.display)

		if len(companies.matched_officers) > 0 or len(companies.matched_persons) > 0:

			for i in companies.matched_companies:
				company = getlink(i, 'self')
				# check for errors
				if not company.has_key('errors'):
					# print '\tAdding Company Search Company : %s' % company['company_name']

					raw_string = ' '.join(self.names)
					pretty = raw_string
					registered = ''
					amount = 0
					url = base_url + company['links']['self']

					self.items.append(ShareholdingsItem(item_id, self.category_id, raw_string, pretty, registered, amount, company, url))

		users = CompaniesHouseUserSearch(self.names)
		users.identify(keywords=KEYWORDS, month=self.month, year=self.year, first=self.first, middle=self.middle, last=self.last, display=self.display)

		for i in users.matched:

			for app in i['appointments']:
				company = getlink(app, 'company')
				# check for errors
				if not company.has_key('errors'):
					# print '\tAdding Officer Search Company : %s' % company['company_name']

					raw_string = ' '.join(self.names)
					pretty = raw_string
					registered = ''
					amount = 0
					url = base_url + company['links']['self']

					self.items.append(ShareholdingsItem(item_id, self.category_id, raw_string, pretty, registered, amount, company, url))

	@property
	def data(self):
		"""
		Returns the class variables as a key/pair dict
		"""
		return vars(self)

class CompaniesHouseUser(Category):
	def __init__(self, user):
		"""
		Companies House User
		"""
		self.title = user['title']
		self.dob = user['dob_str']

		# lists of raw entries and parsed entries (dictionaries)
		self.raw_entries = []
		self.entries = []
		self.items = [{'links' : {'self' : ''}}]

		# category info
		self.category_type = 'companies_house'
		self.category_id = 14
		self.category_description = 'Companies House'
		self.isCurrency = False

		self.do_logic(user)

	def do_logic(self, user):
		"""
		Method performing the logic of parsing raw data into dictionary
		"""

		for appointment in user['appointments']:

			item = AppointmentsItem(appointment)
			self.items.append(item)

	@property
	def data(self):
		"""
		Returns the class variables as a key/pair dict
		"""
		return vars(self)