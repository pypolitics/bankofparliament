
# system libs
import os, re, pprint

# local libs
from utils import PrettyPrintUnicode, getlink, cleanup_raw_string
from companies_house_query import CompaniesHouseUserSearch, CompaniesHouseCompanySearch, CompaniesHouseOfficer
from constants import KEYWORDS
from fuzzywuzzy import fuzz
from companies_house_patches import urls, people

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

	def lookup(self):

		company_number = None
		people_links = []
		found = False

		# apply patches
		if self.donor in urls.keys():
			company_number = urls[self.donor].split('/')[-1]
		if self.donor in people.keys():
			people_links = people[self.donor]

		if not company_number:
			# use the supplied company number from the register of interests
			if 'company' in self.status:
				company_number_search = re.search('registration [0-9|a-z|A-Z]+', self.status)
				if company_number_search:
					company_number = company_number_search.group().split('registration ')[-1]

					# needs padding to 8 digits, if it starts with an int
					if re.match('[0-9]', company_number):
						company_number = '%08d' % (int(company_number))

		self.company = {'company_name' : self.donor, 'company_number' : 'N/A', 'company_status' : 'Active'}
		self.persons = []
		self.officers = []
		self.link = None
		self.appointments = []

		if company_number:

			# we have a company number, no need to search for it
			self.company = getlink({'links' : {'self' : '/company/%s' % str(company_number)}}, 'self')
			persons = getlink(self.company, 'persons_with_significant_control')
			self.persons = persons['items']
			officers = getlink(self.company, 'officers')
			self.officers = officers['items']

			if not self.company.has_key('errors'):
				self.link = 'https://beta.companieshouse.gov.uk' + self.company['links']['self']
			else:
				self.link = ''
			found = True

		else:

			if 'individual' in self.status:

				# for individuals, we store the appointments, then the company, officers etc as children
				# of the appointment

				if people_links != []:

					for pl in people_links:
						bit = pl.split('https://beta.companieshouse.gov.uk')[-1]
						appointments = getlink({'links' : {'self' : '%s' % bit}}, 'self')
						for i in appointments['items']:
							if i not in self.appointments:
								self.appointments.append(i)

					self.link = pl
					found = True

				else:
					# individuals have private addresses - only way of identifying is by name
					officers = CompaniesHouseUserSearch([self.donor])

					dob_month = None
					dob_year = None

					for officer in officers.data:

						name_ratio = fuzz.token_sort_ratio(officer['title'].lower(), self.donor)

						match = False
						if name_ratio == 100:
							match = True
							if officer.has_key('date_of_birth'):
								dob_month = officer['date_of_birth']['month']
								dob_year = officer['date_of_birth']['year']

						elif name_ratio > 70:
							if officer.has_key('date_of_birth'):
								month = officer['date_of_birth']['month']
								year = officer['date_of_birth']['year']

								if month == dob_month and year == dob_year:
									match = True

						if match:
							appointments = getlink(officer, 'self')['items']
							if self.appointments != []:
								for i in appointments:
									if i not in self.appointments:
										self.appointments.append(i)
							else:
								self.appointments = appointments

							self.link = 'https://beta.companieshouse.gov.uk' + officer['links']['self']
							found = True

				for app in self.appointments:
					# print app['links']
					app['company'] = getlink(app, 'company')
					app['officers'] = getlink(app['company'], 'officers')['items']
					app['persons_with_significant_control'] = getlink(app['company'], 'persons_with_significant_control')['items']

			# eveything below here, should generate a company / entity
			elif 'trade' in self.status.lower():
				pass
				# found = True

			# elif 'visit' in self.status:
			# 	pass
				# found = True

			elif 'charity' in self.status.lower():
				pass
				# found = True

			elif 'unincorporated' in self.status.lower():
				pass
				# found = True

			# elif 'members' in self.status.lower():
			# 	pass
			# 	# found = True

			# elif 'other' in self.status.lower():
			# 	pass
			# 	# found = True

			# elif 'friendly' in self.status.lower():
			# 	pass
			# 	# found = True

			# elif 'limited' in self.status.lower():
			# 	pass
			# 	# found = True

			# elif 'llp' in self.status.lower():
			# 	pass
			# 	# found = True

			else:
				pass
				# these are the remaining things to search
				companies = CompaniesHouseCompanySearch([self.donor])

				for i in companies.data:

					# we need the name and address to fuzzy match

					name_ratio = fuzz.token_set_ratio(i['title'].lower(), self.donor)

					if name_ratio > 90:
						if i['address_snippet']:

							addr_ratio = fuzz.token_set_ratio(i['address_snippet'].lower(), self.address)

							# if the address matches enough
							if addr_ratio > 90:

								self.link = 'https://beta.companieshouse.gov.uk' + i['links']['self']
								self.company = getlink(i, 'self')
								persons = getlink(self.company, 'persons_with_significant_control')
								self.persons = persons['items']
								officers = getlink(self.company, 'officers')
								self.officers = officers['items']
								# print 'FOUND %s: , %s' % (self.status.upper(), self.company['company_name'])
								found = True
								break

		if found:
			pass
			print '\tFOUND %s: %s' % (self.status.upper(), self.company['company_name'])
		else:
			# pass
			print '\tMISSING %s: %s' % (self.status.upper(), self.donor)


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

		self.company = getlink(company, 'self')
		persons = getlink(self.company, 'persons_with_significant_control')
		self.persons = persons['items']
		officers = getlink(self.company, 'officers')
		self.officers = officers['items']

		# TODO - check the total results against the number of results returned, may
		# need to query again for the remainder

class OtherShareholdingsItem(Item):
	def __init__(self, item_id, category_id, raw_string, pretty, registered, amount, company, link):
		"""
		OtherShareholdingsItem
		"""

		Item.__init__(self, item_id, category_id, raw_string, pretty, registered, amount)

		self.isWealth = True
		self.link = link

		self.company = getlink(company, 'self')
		persons = getlink(self.company, 'persons_with_significant_control')
		self.persons = persons['items']
		officers = getlink(self.company, 'officers')
		self.officers = officers['items']

		# TODO - check the total results against the number of results returned, may
		# need to query again for the remainder

class GiftsItem(Item):
	def __init__(self, item_id, category_id, raw_string, pretty, registered, amount):
		"""
		GiftsItem
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
