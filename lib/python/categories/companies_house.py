# local libs

from categories import Category
# from items import CompaniesItem
# from utils import regex_for_registered, regex_for_amount

class CompaniesItem():
	def __init__(self, item_id, category_id, raw_string, pretty, registered, amount):
		"""
		Basic Item Class
		"""
		# print 'CompaniesItem - '
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
		# self.get_nouns()

	# def get_nouns(self):
	# 	"""
	# 	Use nlp to find nouns
	# 	"""
	# 	blob = TextBlob(self.raw_string)

	# 	for word, tag in blob.tags:
	# 		if tag in ['NNP', 'NN']:
	# 			self.nouns.append(word.lemmatize())

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


class CompaniesHouseUser(Category):
	def __init__(self, user):
		"""
		Companies House User
		"""
		# self.user = user
		self.title = user['title']
		self.address = user['address_snippet']

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
		# print 'DOING LOGIC'
		for appointment in user['appointments']['items']:
			####################################################################################
			# print '\n\t' + '-'*96
			# print '\tCompanies House Appointment'
			# print '\t' + '-'*96
			company_status = 'N/A'
			company_name = 'N/A'
			officer_role = 'N/A'

			if appointment['appointed_to'].has_key('company_status'):
				company_status = appointment['appointed_to']['company_status'].title()

			if appointment['appointed_to'].has_key('company_name'):
				company_name = appointment['appointed_to']['company_name'].title()

			if appointment.has_key('officer_role'):
				officer_role = appointment['officer_role'].title()

			# print '\t%s, %s, %s' % (officer_role, company_name, company_status)

			amount = 0
			next_id = len(self.items) + 1
			item_id = '%04d' % next_id
			raw_string = '%s, %s, %s' % (officer_role, company_name, company_status)
			pretty = '%s, %s, %s' % (officer_role, company_name, company_status)
			registered = ''
		
			item = CompaniesItem(item_id, self.category_id, raw_string, pretty, registered, amount)
			item.company_status = company_status
			item.company_name = company_name
			item.officer_role = officer_role

			self.items.append(item)

			# pprint.pprint(item.data)

