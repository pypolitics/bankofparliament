# local libs
from categories import Category
from items import DirectDonationsItem, IndirectDonationsItem
from utils import regex_for_registered, regex_for_amount, get_regex_pair_search, string_to_datetime

class IndirectDonations(Category):
	def __init__(self):
		"""
		Indirect Donations
		"""
		# Init the class, then set some class specific variables
		Category.__init__(self)

		# category info
		self.category_id = 2
		self.category_type = 'indirect_donations'
		self.category_description = 'Indirect Donations'
		self.isCurrency = True

	def do_logic(self, raw_string):
		"""
		Method performing the logic of parsing raw data into dictionary
		"""

		amount = 0
		next_id = len(self.items) + 1
		item_id = '%04d' % next_id

		# not much we can really split on
		pretty = raw_string
		registered = regex_for_registered(raw_string)

		# hold a list of lists with search pair, to then regex out the value between them
		regex_pairs = []
		regex_pairs.append(['Name of donor: ', 'Address of donor: '])
		regex_pairs.append(['Address of donor: ', 'Amount of donation or nature and value if donation in kind: '])
		regex_pairs.append(['Amount of donation or nature and value if donation in kind:', 'Date received: '])
		regex_pairs.append(['Donor status: ', r'\(Registered '])

		amount = regex_for_amount(raw_string)

		donor = None
		address = None
		status = None

		for pair in regex_pairs:
			regex_search = get_regex_pair_search(pair, raw_string)

			if regex_search:
				value = regex_search.group(1)

				if 'name of donor' in pair[0].lower():
					donor = value
					pretty = value
				elif 'address of donor' in pair[0].lower():
					address = value
				elif 'donor status' in pair[0].lower():
					status = value
		
		item = IndirectDonationsItem(item_id, self.category_id, raw_string, pretty, registered, amount)
		item.donor = donor
		item.address = address
		item.status = status

		self.items.append(item)

class DirectDonations(Category):
	def __init__(self):
		"""
		Direct Donations
		"""
		
		# Init the class, then set some class specific variables
		Category.__init__(self)

		# category info
		self.category_id = 3
		self.category_type = 'direct_donations'
		self.category_description = 'Direct Donations'
		self.isCurrency = True

	def do_logic(self, raw_string):
		"""
		Method performing the logic of parsing raw data into dictionary
		"""

		amount = 0
		next_id = len(self.items) + 1
		item_id = '%04d' % next_id

		# not much we can really split on
		pretty = raw_string
		registered = regex_for_registered(raw_string)

		# hold a list of lists with search pair, to then regex out the value between them
		regex_pairs = []
		regex_pairs.append(['Name of donor: ', 'Address of donor: '])
		regex_pairs.append(['Address of donor: ', 'Amount of donation or nature and value if donation in kind: '])
		regex_pairs.append(['Address of donor: ', 'Estimate of the probable value (or amount of any donation): '])
		regex_pairs.append(['Amount of donation or nature and value if donation in kind:', 'Date received: '])
		regex_pairs.append(['Estimate of the probable value (or amount of any donation): ', 'Date received: '])
		regex_pairs.append(['Date received: ', 'Date accepted: '])
		regex_pairs.append(['Date accepted: ', 'Donor status: '])
		regex_pairs.append(['Donor status: ', r'\(Registered '])

		amount = regex_for_amount(raw_string)

		donor = None
		address = None
		received = None
		accepted = None
		status = None

		for pair in regex_pairs:
			regex_search = get_regex_pair_search(pair, raw_string)

			if regex_search:
				value = regex_search.group(1)

				if 'name of donor' in pair[0].lower():
					donor = value
					pretty = value
				elif 'address of donor' in pair[0].lower():
					address = value
				elif 'received' in pair[0].lower():
					received = value
				elif 'accepted' in pair[0].lower():
					accepted = value
				elif 'donor status' in pair[0].lower():
					status = value

		item = DirectDonationsItem(item_id, self.category_id, raw_string, pretty, registered, amount)
		item.donor = donor
		item.address = address
		item.received = received
		item.accepted = accepted
		item.status = status

		self.items.append(item)
