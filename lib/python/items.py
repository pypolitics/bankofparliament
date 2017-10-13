
# system libs
import os

# local libs
from utils import PrettyPrintUnicode

base_url = 'https://beta.companieshouse.gov.uk'

class Item():
	def __init__(self, item_id, category_id, raw_string, pretty, registered, amount):
		"""
		Basic Item Class
		"""
		self.item_id = item_id
		self.category_id = category_id
		self.raw_string = raw_string
		self.pretty = pretty
		self.registered = registered
		self.amount = amount
		self.nouns = []

		self.isIncome = False
		self.isWealth = False
		self.isGift = False
		self.isDonation = False

		# pluck out nouns, maybe we make a word cloud out of it
		# or
		# use it them to query companies house, land registry
		# self._get_nouns()

	def _get_nouns(self):
		"""
		Use nlp to find nouns
		"""
		from textblob import TextBlob
		blob = TextBlob(self.raw_string)

		for word, tag in blob.tags:
			if tag in ['NNP', 'NN']:
				self.nouns.append(word.lemmatize())

	def pprint(self):
		"""
		Petty prints using custom pprint class, formatting unicode characters
		"""
		PrettyPrintUnicode().pprint(self.data)

	@property
	def data(self):
		"""
		Returns the class variables as a key/pair dict
		"""
		return vars(self)

class AppointmentsItem():
	def __init__(self, appointment):
		"""
		Basic Item Class
		"""

		self.appointment = appointment
		self.company_status = 'N/A'
		self.company_name = 'N/A'
		self.company_number = 'N/A'
		self.officer_role = 'N/A'
		self.resigned_on = 'N/A'
		self.url = base_url + appointment['links']['company']

		if appointment['appointed_to'].has_key('company_status'):
			self.company_status = appointment['appointed_to']['company_status'].title()

		if appointment['appointed_to'].has_key('company_name'):
			self.company_name = appointment['appointed_to']['company_name'].title()

		if appointment.has_key('officer_role'):
			self.officer_role = appointment['officer_role'].title()

		if appointment.has_key('resigned_on'):
			self.resigned_on = appointment['resigned_on'].title()

		if appointment.has_key('appointed_to'):
			self.company_number = appointment['appointed_to']['company_number']

		self.keywords = self.company_name.split(' ')
		self.company = CompaniesItem(appointment).data

	def pprint(self):
		"""
		Petty prints using custom pprint class, formatting unicode characters
		"""
		PrettyPrintUnicode().pprint(self.data)

	@property
	def data(self):
		"""
		Returns the class variables as a key/pair dict
		"""
		return vars(self)

class CompaniesItem():
	def __init__(self, appointment):
		"""
		Basic Item Class
		"""

	def pprint(self):
		"""
		Petty prints using custom pprint class, formatting unicode characters
		"""
		PrettyPrintUnicode().pprint(self.data)

	@property
	def data(self):
		"""
		Returns the class variables as a key/pair dict
		"""
		return vars(self)

class SalaryItem(Item):
	def __init__(self, item_id, category_id, raw_string, pretty, registered, amount):
		"""
		SalaryItem
		"""

		Item.__init__(self, item_id, category_id, raw_string, pretty, registered, amount)

		self.isIncome = True

class AdditionalSalaryItem(Item):
	def __init__(self, item_id, category_id, raw_string, pretty, registered, amount):
		"""
		AdditionalSalaryItem
		"""

		Item.__init__(self, item_id, category_id, raw_string, pretty, registered, amount)

		self.isIncome = True

class DirectDonationsItem(Item):
	def __init__(self, item_id, category_id, raw_string, pretty, registered, amount):
		"""
		DirectDonationsItem
		"""

		Item.__init__(self, item_id, category_id, raw_string, pretty, registered, amount)

		self.isDonation = True

class IndirectDonationsItem(Item):
	def __init__(self, item_id, category_id, raw_string, pretty, registered, amount):
		"""
		IndirectDonationsItem
		"""

		Item.__init__(self, item_id, category_id, raw_string, pretty, registered, amount)

		self.isDonation = True

class FamilyItem(Item):
	def __init__(self, item_id, category_id, raw_string, pretty, registered, amount):
		"""
		FamilyItem
		"""

		Item.__init__(self, item_id, category_id, raw_string, pretty, registered, amount)

class FamilyLobbyistsItem(Item):
	def __init__(self, item_id, category_id, raw_string, pretty, registered, amount):
		"""
		FamilyLobbyistsItem
		"""

		Item.__init__(self, item_id, category_id, raw_string, pretty, registered, amount)

class MiscellaneousItem(Item):
	def __init__(self, item_id, category_id, raw_string, pretty, registered, amount):
		"""
		MiscellaneousItem
		"""

		Item.__init__(self, item_id, category_id, raw_string, pretty, registered, amount)

class ShareholdingsItem(Item):
	def __init__(self, item_id, category_id, raw_string, pretty, registered, amount, company, link):
		"""
		ShareholdingsItem
		"""

		Item.__init__(self, item_id, category_id, raw_string, pretty, registered, amount)

		self.isWealth = True
		self.link = link
		self.company = company

class OtherShareholdingsItem(Item):
	def __init__(self, item_id, category_id, raw_string, pretty, registered, amount, company, link):
		"""
		OtherShareholdingsItem
		"""

		Item.__init__(self, item_id, category_id, raw_string, pretty, registered, amount)

		self.isWealth = True
		self.link = link
		self.company = company

class GiftsItem(Item):
	def __init__(self, item_id, category_id, raw_string, pretty, registered, amount):
		"""
		GiftsItem
		"""

		Item.__init__(self, item_id, category_id, raw_string, pretty, registered, amount)

		self.isGift = True

class GiftsOutsideUKItem(Item):
	def __init__(self, item_id, category_id, raw_string, pretty, registered, amount):
		"""
		GiftsOutsideUKItem
		"""

		Item.__init__(self, item_id, category_id, raw_string, pretty, registered, amount)

		self.isGift = True

class VisitsOutsideUKItem(Item):
	def __init__(self, item_id, category_id, raw_string, pretty, registered, amount):
		"""
		VisitsOutsideUKItem
		"""

		Item.__init__(self, item_id, category_id, raw_string, pretty, registered, amount)

		self.isGift = True

class EmploymentItem(Item):
	def __init__(self, item_id, category_id, raw_string, pretty, registered, amount):
		"""
		EmploymentItem
		"""

		Item.__init__(self, item_id, category_id, raw_string, pretty, registered, amount)

		self.isIncome = True

class PropertyItem(Item):
	def __init__(self, item_id, category_id, raw_string, pretty, registered, amount):
		"""
		PropertyItem
		"""

		Item.__init__(self, item_id, category_id, raw_string, pretty, registered, amount)

		# could be either wealth or income or both
