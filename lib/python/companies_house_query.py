from pprint import pprint
from fuzzywuzzy import fuzz
from utils import get_request, getlink, filter_by_name_string, contains_keywords

companies_house_user = 'ZCCtuxpY7uvkDyxLUz37dCYFIgke9PKfhMlEGC-Q'

class CompaniesHouseUserSearch():
	def __init__(self, query, query_type='officers', limit='50', headers={}):
		"""Query companies house"""

		url = 'https://api.companieshouse.gov.uk/search/%s?q=%s&items_per_page=%s' % (query_type, query.lower(), limit)
		self.url = url.replace(' ', '+')

		request = get_request(url=self.url, user=companies_house_user, headers=headers)
		self.data = request.json()

		if self.data.has_key('items'):
			self.data = self.data['items']
		else:
			self.data = {}

	def _get_appointments(self, record):
		"""Get the appointments of the found officer"""
		return getlink(record, 'self')

	def identify(self, keywords, month, year, first, middle, last, display):
		"""Try to identify the companies house officer record as the requested mp."""

		count_threshold = 2
		self.matched = []

		for record in self.data:

			match_count = 0

			# look for date of birth
			match_dob = None
			if record.has_key('date_of_birth'):
				if record['date_of_birth']['month'] == month and record['date_of_birth']['year'] == year:
					match_dob = True
					match_count += 1
				else:
					match_dob = False
					match_count -= 1

			# look for keywords in the appointments
			# this is a lengthy proceedure, but necessary to be able to match keywords.
			# the user record doesnt contain any keys that would contains values like, politician, parliament
			match_keywords = None
			appointments = self._get_appointments(record)['items']
			for app in appointments:
				to_search = []
				if app.has_key('occupation'):
					to_search += app['occupation'].split(' ')

				if app.has_key('address'):
					for each in app['address'].values():
						to_search += each.split(' ')

				if contains_keywords(to_search, keywords):
					match_keywords = True
					match_count += 1

			# look for display name first
			if filter_by_name_string(record, display) != []:
				match_display = True
			else:
				match_display = False

			# look for first last name
			if filter_by_name_string(record, '%s %s' % (first, last)) != []:
				match_fl = True
			else:
				match_fl = False

			# look for first middle last name
			if filter_by_name_string(record, '%s %s %s' % (first, middle, last)) != []:
				match_fml = True
			else:
				match_fml = False

			# only count a name match once
			if True in [match_display, match_fl, match_fml]:
				match_count += 1

			if match_count >= count_threshold:

				record['appointments'] = appointments
				record['matches'] = {}
				record['matches']['match_dob'] = match_dob
				record['matches']['match_keywords'] = match_keywords
				record['matches']['match_display'] = match_display
				record['matches']['match_fl'] = match_fl
				record['matches']['match_fml'] = match_fml
				record['matches']['match_count'] = match_count

				self.matched.append(record)

class CompaniesHouseOfficer():
	def __init__(self, record):
		"""Verified Companies House Officer Class"""

		if record.has_key('address'):
			self.address = record['address']
		else:
			self.address = None

		if record.has_key('address_snippet'):
			self.address_snippet = record['address_snippet']
		else:
			self.address_snippet = None

		if record.has_key('date_of_birth'):
			self.date_of_birth = record['date_of_birth']
		else:
			self.date_of_birth = {'month' : '?', 'year' : '?'}

		if record.has_key('links'):
			self.links = record['links']
		else:
			self.links = None

		if record.has_key('title'):
			self.title = record['title']
		else:
			self.title = None

		self._get_appointments(record)

	def _get_appointments(self, record):
		"""Get appointment classes from dicts"""

		# we actually already have the appointments. needed them to identify the searched person.
		self.appointments = [CompaniesHouseAppointment(i, officer=self) for i in record['appointments']]

	def __str__(self):
		return 'Officer : %s, Address : %s, Date of Birth : %s/%s' % (self.title, self.address_snippet, self.date_of_birth['month'], self.date_of_birth['year'])

class CompaniesHouseAppointment():
	def __init__(self, data, officer):
		"""Companies House Appointments Class"""

		self._officer = officer

		if data.has_key('name'):
			self.name = data['name']
		else:
			self.name = None

		if data.has_key('appointed_on'):
			self.appointed_on = data['appointed_on']
		else:
			self.appointed_on = None

		if data.has_key('links'):
			self.links = data['links']
		else:
			self.links = None

		if data.has_key('resigned_on'):
			self.resigned_on = data['resigned_on']
		else:
			self.resigned_on = None

		if data.has_key('officer_role'):
			self.officer_role = data['officer_role']
		else:
			self.officer_role = None

		if data.has_key('occupation'):
			self.occupation = data['occupation']
		else:
			self.occupation = None

		self._get_company(data)

	def _get_company(self, data):
		"""Get company class from dict"""

		self.company = CompaniesHouseCompany(getlink(data, 'company'), self._officer)

	def __str__(self):
		return 'Appointment: Name : %s, Officer Role : %s, Resigned : %s, Occupation : %s' % (self.name, self.officer_role, self.resigned_on, self.occupation)

class CompaniesHouseCompany():
	def __init__(self, data, officer):
		"""
		Companies House Company Class

		Company class holds the officers, persons of significance and filing history classes
		"""

		self._officer = officer
		self.officers = []
		self.persons = []
		self.filing = []

		if data.has_key('registered_office_address'):
			self.registered_office_address = data['registered_office_address']
		else:
			self.registered_office_address = None

		if data.has_key('type'):
			self.type = data['type']
		else:
			self.type = None

		if data.has_key('company_name'):
			self.company_name = data['company_name']
		else:
			self.company_name = None

		if data.has_key('company_number'):
			self.company_number = data['company_number']
		else:
			self.company_number = None

		if data.has_key('company_status'):
			self.company_status = data['company_status']
		else:
			self.company_status = None

		if data.has_key('sic_codes'):
			self.sic_codes = data['sic_codes']
		else:
			self.sic_codes = None

		if data.has_key('links'):
			self.links = data['links']
		else:
			self.links = None

		if data.has_key('previous_company_names'):
			self.previous_company_names = data['previous_company_names']
		else:
			self.previous_company_names = None

		if data.has_key('has_charges'):
			self.has_charges = data['has_charges']
		else:
			self.has_charges = None

		if data.has_key('has_insolvency_history'):
			self.has_insolvency_history = data['has_insolvency_history']
		else:
			self.has_insolvency_history = None

		self._get_officers(data)
		self._get_filing_history(data)
		self._get_persons(data)

	def _get_officers(self, data):
		"""Get officers from dict"""

		officer_dicts = getlink(data, 'officers')['items']
		for officer in officer_dicts:

			# fix the dict to work CompaniesHouseOfficer class

			# setting the appointments to [], ensures we dont recurse all through the companieshouse db
			officer['appointments'] = []
			officer['title'] = officer['name']
			officer['address_snippet'] = ' '.join(officer['address'].values())
			self.officers.append(CompaniesHouseOfficer(officer))

	def _get_filing_history(self, data):
		"""Get filing history of company from dict"""

		filing_dicts = getlink(data, 'filing_history')['items']
		for filing in filing_dicts:
			self.filing.append(CompaniesHouseFiling(filing))

	def _get_persons(self, data):
		"""Get persons with significant control from dict"""

		persons_dicts = getlink(data, 'persons_with_significant_control')['items']
		for person in persons_dicts:

			x = CompaniesHousePerson(person)

			if self.match_significant_to_self(person):
				x.isOfficer = True

			self.persons.append(x)

	def match_significant_to_self(self, person):
		""""""

		fuzzy_threshold = 80
		count_threshold = 2

		# dob
		if person.has_key('date_of_birth'):
			dob = person['date_of_birth']
		else:
			dob = None

		# name
		remove_titles = ['mr', 'mrs', 'ms', 'dr', 'sir']
		if person.has_key('name'):
			name = person['name']

			words = []
			for word in name.split(' '):
				if word.lower() not in remove_titles:
					if word != '':
						words.append(word)
			name = ' '.join(words)

		else:
			name = None

		# count the matches
		count = 0
		if self._officer.date_of_birth == dob:
			count += 1

		if fuzz.partial_ratio(self._officer.title.lower(), name.lower()) >= fuzzy_threshold:
			count += 1

		# decide
		if count >= count_threshold:
			return True
		else:
			return False

	def __str__(self):
		return 'Company : Name : %s, Company Status : %s, Company Number : %s' % (self.company_name, self.company_status, self.company_number)

class CompaniesHouseFiling():
	def __init__(self, data):
		"""Companies House Filing History Class"""

		if data.has_key('category'):
			self.category = data['category']
		else:
			self.category = None

		if data.has_key('date'):
			self.date = data['date']
		else:
			self.date = None

		if data.has_key('description'):
			self.description = data['description']
		else:
			self.description = None

		if data.has_key('description_values'):
			self.description_values = data['description_values']
		else:
			self.description_values = None

		if data.has_key('links'):
			self.links = data['links']
		else:
			self.links = None

	def __str__(self):
		return 'Filing : %s' % (self.description)

class CompaniesHousePerson():
	def __init__(self, data):
		"""Companies House Significant Person Class"""

		if data.has_key('name'):
			self.name = data['name']
		else:
			self.name = None

		if data.has_key('natures_of_control'):
			self.natures_of_control = data['natures_of_control']
		else:
			self.natures_of_control = None

		if data.has_key('address'):
			self.address = data['address']
		else:
			self.address = None

		if data.has_key('date_of_birth'):
			self.date_of_birth = data['date_of_birth']
		else:
			self.date_of_birth = None

		self.isOfficer = False

	def __str__(self):
		return 'Significant : %s, Address : %s, Date of Birth : %s/%s' % (self.name, ' '.join(self.address.values()), self.date_of_birth['month'], self.date_of_birth['year'])

########################################################################################################################

users = CompaniesHouseUserSearch('Nadhim Zahawi')
users.identify(keywords=['elliott'], month=6, year=1967, first='nadhim', middle='', last='zahawi', display='Mr Nadhim Zahawi')

for m in users.matched:
	user = CompaniesHouseOfficer(m)

	print user
	for app in user.appointments:
		print ''
		print '\t', app
		print '\t', app.company
		print '\tPersons : %s, Filings : %s, Officers : %s' % (len(app.company.persons), len(app.company.filing), len(app.company.officers))
		print ''

		for person in app.company.persons:
			if person.isOfficer:
				print '\t\t', person
			else:
				print '\t\tOther', person

		print ''
		for officer in app.company.officers:
			print '\t\t', officer

		print ''
		for filing in app.company.filing:
			print '\t\t', filing
