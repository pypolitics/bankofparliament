# local libs

from categories import Category
import pprint
from items import CompaniesItem
# from utils import regex_for_registered, regex_for_amount

base_url = 'https://beta.companieshouse.gov.uk'

class CompaniesHouseUser(Category):
	def __init__(self, user):
		"""
		Companies House User
		"""
		# self.user = user
		self.title = user['title']
		self.address = user['address_snippet']

		# base_url = 'https://beta.companieshouse.gov.uk'
		self.url = base_url + user['links']['self']

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

		for appointment in user['appointments']['items']:

			company_status = 'N/A'
			company_name = 'N/A'
			officer_role = 'N/A'
			resigned_on = 'N/A'

			if appointment['appointed_to'].has_key('company_status'):
				company_status = appointment['appointed_to']['company_status'].title()

			if appointment['appointed_to'].has_key('company_name'):
				company_name = appointment['appointed_to']['company_name'].title()

			if appointment.has_key('officer_role'):
				officer_role = appointment['officer_role'].title()

			if appointment.has_key('resigned_on'):
				resigned_on = appointment['resigned_on'].title()
			
			amount = 0
			next_id = len(self.items) + 1
			item_id = '%04d' % next_id
			raw_string = '%s, %s, %s' % (officer_role, company_name, company_status)
			pretty = '%s, %s, %s' % (officer_role, company_name, company_status)
			registered = ''

			item = CompaniesItem(item_id, self.category_id, raw_string, pretty, registered, amount)

			# info on the appointment, the company name, status and the role held, also the resignation date
			item.company_status = company_status
			item.company_name = company_name
			item.officer_role = officer_role
			item.resigned_on = resigned_on
			item.url = base_url + appointment['links']['company']

			self.items.append(item)
