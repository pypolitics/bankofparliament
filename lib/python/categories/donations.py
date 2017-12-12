# local libs
from categories import Category
from items import DirectDonationsItem, IndirectDonationsItem
from utils import regex_for_registered, regex_for_amount, get_regex_pair_search, string_to_datetime
from pprint import pprint

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

	def do_logic(self, raw_string, raw_data):
		"""
		Method performing the logic of parsing raw data into dictionary
		"""

		amount = 0
		next_id = len(self.items) + 1
		item_id = '%04d' % next_id

		# not much we can really split on
		pretty = raw_string
		registered = regex_for_registered(raw_string)

		amount = regex_for_amount(raw_string)

		donor = raw_data['raw_string']
		address = ''
		status = ''

		for key in raw_data:
			if 'name of donor' in key.lower():
				donor = raw_data[key]
				pretty = donor

			elif 'address' in key.lower():
				address = raw_data[key]

			elif 'status' in key.lower():
				status = raw_data[key]
		
		item = IndirectDonationsItem(item_id, self.category_id, raw_string, pretty, registered, amount)
		item.donor = donor
		item.address = address
		item.status = status
		item.lookup()
		self.items.append(item)
		# pprint(raw_data)

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

	def do_logic(self, raw_string, raw_data):
		"""
		Method performing the logic of parsing raw data into dictionary
		"""

		amount = 0
		next_id = len(self.items) + 1
		item_id = '%04d' % next_id

		# not much we can really split on
		pretty = raw_string
		registered = regex_for_registered(raw_string)

		amount = regex_for_amount(raw_string)

		donor = raw_data['raw_string']
		address = ''
		status = ''

		for key in raw_data:
			if 'name of donor' in key.lower():
				donor = raw_data[key]
				pretty = donor

			elif 'address' in key.lower():
				address = raw_data[key]

			elif 'status' in key.lower():
				status = raw_data[key]

		item = DirectDonationsItem(item_id, self.category_id, raw_string, pretty, registered, amount)
		item.donor = donor
		item.address = address
		item.status = status
		item.lookup()
		self.items.append(item)
