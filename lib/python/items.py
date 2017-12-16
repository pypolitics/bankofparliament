# -*- coding: utf-8 -*-

# system libs
import os, re, pprint

# local libs
from utils import PrettyPrintUnicode, getlink, cleanup_raw_string, read_unincorporated
from companies_house_query import CompaniesHouseUserSearch, CompaniesHouseCompanySearch, CompaniesHouseOfficer
from constants import KEYWORDS
from fuzzywuzzy import fuzz

# import patches
from patches.companies_house import urls, people
from patches.trade_unions import trade_union
from patches.charities import charities
from patches.clubs import clubs
from patches.others import others
from patches.foreign_governments import foreign_governments

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

		self.donor = str(self.donor)
		company_number = None
		people_links = []
		found = False


		# ugly hack corrections
		if self.donor in ['Tresco Estate', 'James Hay', 'Think BDW Ltd']:
			self.status = 'company'

		if self.status == 'company, no 10120655':
			company_number = 10120655

		if 'Armed Forces Parliamentary Trust' == self.donor:
			self.status = 'other'
		if u'Buck’s Club 1919' in self.donor:
			self.donor = "Buck's Club 1919"
			self.status = 'members'
		if u'Pratt’s Club' in self.donor:
			self.donor = "Pratt's Club"
			self.status = 'members'
		if 'carlton club' in self.donor.lower():
			self.donor = 'Carlton Club'
			self.status = 'members'
		if 'National Liberal Club' in self.donor:
			self.donor = 'National Liberal Club'
			self.status = 'members'
		if 'The Public Interest Foundation (UK charity)' == self.donor:
			self.status = 'charity'

		# apply patches
		if self.donor in urls.keys():
			company_number = urls[self.donor].split('/')[-1]

		if self.donor in people.keys():
			people_links = people[self.donor]

		if not company_number:
			# use the supplied company number from the register of interests
			# if 'company' in self.status:
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
				found = True
			else:
				self.company = {'company_name' : self.donor, 'company_number' : 'N/A', 'company_status' : 'Active'}
				self.link = ''

		else:

			if 'individual' in self.status.lower() or 'private' in self.status.lower():
				# found = True
				# for individuals, we store the appointments, then the company, officers etc as children
				# of the appointment

				if people_links != []:

					for pl in people_links:
						bit = pl.split('https://beta.companieshouse.gov.uk')[-1]
						appointments = getlink({'links' : {'self' : '%s' % bit}}, 'self')
						for i in appointments['items']:
							if i not in self.appointments:
								self.appointments.append(i)

					# just take the last one
					self.link = pl
					found = True

				for app in self.appointments:
					# add the company, officers and persons record to appointment record
					app['company'] = getlink(app, 'company')
					app['officers'] = getlink(app['company'], 'officers')['items']
					app['persons_with_significant_control'] = getlink(app['company'], 'persons_with_significant_control')['items']

			# eveything below here, should generate a company / entity
			elif 'trade' in self.status.lower():
				self.type = 'union'
				if self.donor in trade_union.keys():
					self.donor = trade_union[self.donor]
					found = True

			elif 'charity' in self.status.lower():
				self.type = 'charity'
				if self.donor in charities.keys():
					self.donor = charities[self.donor]
					found = True

			elif 'unincorporated' in self.status.lower():
				self.type = 'club'
				if self.donor in clubs.keys():
					self.donor = clubs[self.donor]
					found = True

			elif 'members' in self.status.lower():
				self.type = 'club'
				if self.donor in clubs.keys():
					self.donor = clubs[self.donor]
					found = True

			elif 'friendly' in self.status.lower():
				self.type = 'club'
				if self.donor in clubs.keys():
					self.donor = clubs[self.donor]
					found = True

			elif 'other' in self.status.lower():
				self.type = 'other'
				if self.donor in others.keys():
					self.donor = others[self.donor]
					found = True

			elif 'trust' in self.status.lower():
				self.type = 'other'
				if self.donor in others.keys():
					self.donor = others[self.donor]
					found = True

			elif 'provident' in self.status.lower():
				self.type = 'company'
				if self.donor in others.keys():
					self.donor = others[self.donor]
					found = True

			elif 'visit' in self.status:
				# TODO
				self.type = 'visit'


			else:
				# we dont have a company number, so do a company search
				if 'llp' in self.status.lower() or 'limited' in self.status.lower():
					self.type = 'company'
				else:
					self.type = 'other'

				# these are the remaining things to search - can only do a company search really
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

		# print self.donor, self.address
		# if 'sw1p 3ql' in self.address.lower():
		# 	print '*'*100
		# 	print '55 TUFTON STREET: %s' % self.donor
		# 	print '*'*100

		if found:
			pass
			# print '\tFOUND %s: %s' % (self.status.upper(), self.donor)
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

		if self.company == {'items' : []}:
			self.company = {'company_name' : pretty, 'company_number' : 'N/A', 'company_status' : 'N/A'}

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

		if self.company == {'items' : []}:
			self.company = {'company_name' : pretty, 'company_number' : 'N/A', 'company_status' : 'N/A'}

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
