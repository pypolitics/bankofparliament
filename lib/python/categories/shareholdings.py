# local libs
from categories import Category
from items import ShareholdingsItem, OtherShareholdingsItem
from utils import regex_for_registered, regex_for_amount, regex_for_percent, cleanup_raw_string, getlink
from companies_house_query import CompaniesHouseCompanySearch

class Shareholdings(Category):
	def __init__(self, extended, keywords, month, year, first, middle, last, display):
		"""
		Shareholdings

		TODO: regex for percentage share, then lookup companies house
		then use that value for item amount 

		"""
		self.month = month
		self.year = year
		self.first = first
		self.middle = middle
		self.last = last

		# Init the class, then set some class specific variables
		Category.__init__(self)

		# category info
		self.category_id = 8
		self.category_type = 'shareholdings'
		self.category_description = 'Shareholdings'
		self.isCurrency = False

	def do_logic(self, raw_string):
		"""
		Method performing the logic of parsing raw data into item class
		"""

		matched_company = {}

		next_id = len(self.items) + 1
		item_id = '%04d' % next_id

		# not much we can really split on
		pretty = raw_string.split(' (Registered')[0]
		registered = regex_for_registered(raw_string)
		amount = 1
		amount = regex_for_percent(raw_string)

		company_search_string = cleanup_raw_string(raw_string)
		# print 'Search String : %s' % company_search_string 

		companies = CompaniesHouseCompanySearch(queries=[company_search_string], limit='50')

		company_found = False

		for i in companies.data:

			if not company_found:
				# print '\tCompany Name : ', i['title']
				company = getlink(i, 'self')
				officers = getlink(company, 'officers')['items']
				persons = getlink(company, 'persons_with_significant_control')['items']

				for per in persons:

					if per.has_key('name'):
						name = per['name']
						spl = name.split(',')
						first = spl[-1].lower()
						last = spl[0].lower()
					else:
						name = ''

					if per.has_key('date_of_birth'):
						date_of_birth = per['date_of_birth']
						month = date_of_birth['month']
						year = date_of_birth['year']
					else:
						date_of_birth = ''
						month = ''
						year = ''

					match_count = 0
					matches = {}
					if self.first.lower() in name.lower():
						match_count += 1
						matches['first'] = True
					if self.last.lower() in name.lower():
						match_count += 1
						matches['last'] = True
					if self.month == month:
						match_count += 1
						matches['month'] = True
					if self.year == year:
						match_count += 1
						matches['year'] = True

					# count the matches
					if match_count == 4:

						matched_company = company
						company_found = True
						break

				if not company_found:
					for off in officers:

						if off.has_key('name'):
							name = off['name']
							spl = name.split(',')
							first = spl[-1].lower()
							last = spl[0].lower()
						else:
							name = ''

						if off.has_key('occupation'):
							occupation = off['occupation']
						else:
							occupation = ''

						if off.has_key('date_of_birth'):
							date_of_birth = off['date_of_birth']
							month = date_of_birth['month']
							year = date_of_birth['year']
						else:
							date_of_birth = ''
							month = ''
							year = ''

						match_count = 0
						matches = {}
						if self.first.lower() in name.lower():
							match_count += 1
							matches['first'] = True
						if self.last.lower() in name.lower():
							match_count += 1
							matches['last'] = True
						if self.month == month:
							match_count += 1
							matches['month'] = True
						if self.year == year:
							match_count += 1
							matches['year'] = True

						# count the matches
						if match_count == 4:

							matched_company = company
							company_found = True
							break


		if matched_company != {}:
			link = matched_company['links']['self']
			url = 'https://beta.companieshouse.gov.uk%s' % link
		else:
			url = ''
			company = {}
		self.items.append(ShareholdingsItem(item_id, self.category_id, raw_string, pretty, registered, amount, company, url))

	@property
	def data(self):
		"""
		Returns the class variables as a key/pair dict
		"""
		return vars(self)

class OtherShareholdings(Category):
	def __init__(self, extended, keywords, month, year, first, middle, last, display):
		"""
		Miscellaneous
		"""
		self.month = month
		self.year = year
		self.first = first
		self.middle = middle
		self.last = last

		# Init the class, then set some class specific variables
		Category.__init__(self)

		# category info
		self.category_id = 9
		self.category_type = 'shareholdings'
		self.category_description = 'Other Shareholdings'
		self.isCurrency = True

	def do_logic(self, raw_string):
		"""
		Method performing the logic of parsing raw data into item class
		"""
		matched_company = {}

		next_id = len(self.items) + 1
		item_id = '%04d' % next_id

		# not much we can really split on
		pretty = raw_string.split(' (Registered')[0]
		registered = regex_for_registered(raw_string)
		amount = regex_for_amount(raw_string)
		if amount == 0:
			amount = 70000

		company_search_string = cleanup_raw_string(raw_string)
		# print 'Search String : %s' % company_search_string 

		companies = CompaniesHouseCompanySearch(queries=[company_search_string], limit='50')

		company_found = False

		for i in companies.data:

			if not company_found:
				# print '\tCompany Name : ', i['title']
				company = getlink(i, 'self')
				officers = getlink(company, 'officers')['items']
				persons = getlink(company, 'persons_with_significant_control')['items']

				for per in persons:

					if per.has_key('name'):
						name = per['name']
						spl = name.split(',')
						first = spl[-1].lower()
						last = spl[0].lower()
					else:
						name = ''

					if per.has_key('date_of_birth'):
						date_of_birth = per['date_of_birth']
						month = date_of_birth['month']
						year = date_of_birth['year']
					else:
						date_of_birth = ''
						month = ''
						year = ''

					match_count = 0
					matches = {}
					if self.first.lower() in name.lower():
						match_count += 1
						matches['first'] = True
					if self.last.lower() in name.lower():
						match_count += 1
						matches['last'] = True
					if self.month == month:
						match_count += 1
						matches['month'] = True
					if self.year == year:
						match_count += 1
						matches['year'] = True

					if match_count == 4:

						matched_company = company
						company_found = True
						break

				if not company_found:
					for off in officers:

						if off.has_key('name'):
							name = off['name']
							spl = name.split(',')
							first = spl[-1].lower()
							last = spl[0].lower()
						else:
							name = ''

						if off.has_key('occupation'):
							occupation = off['occupation']
						else:
							occupation = ''

						if off.has_key('date_of_birth'):
							date_of_birth = off['date_of_birth']
							month = date_of_birth['month']
							year = date_of_birth['year']
						else:
							date_of_birth = ''
							month = ''
							year = ''

						match_count = 0
						matches = {}
						if self.first.lower() in name.lower():
							match_count += 1
							matches['first'] = True
						if self.last.lower() in name.lower():
							match_count += 1
							matches['last'] = True
						if self.month == month:
							match_count += 1
							matches['month'] = True
						if self.year == year:
							match_count += 1
							matches['year'] = True

						if match_count == 4:

							matched_company = company
							company_found = True
							break

		if matched_company != {}:
			link = matched_company['links']['self']
			url = 'https://beta.companieshouse.gov.uk%s' % link
		else:
			url = ''
			company = {}
		self.items.append(ShareholdingsItem(item_id, self.category_id, raw_string, pretty, registered, amount, company, url))

	@property
	def data(self):
		"""
		Returns the class variables as a key/pair dict
		"""
		return vars(self)