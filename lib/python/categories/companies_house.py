# local libs

from categories import Category
import pprint
from items import AppointmentsItem

base_url = 'https://beta.companieshouse.gov.uk'

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
		self.items = []

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