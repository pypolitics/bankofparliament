# local libs

from categories import Category
from items import GiftsItem, GiftsOutsideUKItem
from utils import regex_for_registered, regex_for_amount, get_regex_pair_search, string_to_datetime

class Gifts(Category):
	def __init__(self):
		"""
		Gifts
		"""

		# Init the class, then set some class specific variables
		Category.__init__(self)

		# category info
		self.category_id = 4
		self.category_type = 'gifts'
		self.category_description = 'Gifts'
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
				elif 'address of donor' in pair[0].lower():
					address = value
				elif 'received' in pair[0].lower():
					received = value
				elif 'accepted' in pair[0].lower():
					accepted = value
				elif 'donor status' in pair[0].lower():
					status = value
				elif 'amount' in pair[0].lower():
					pretty = value

		item = GiftsItem(item_id, self.category_id, raw_string, pretty, registered, amount)
		item.donor = donor
		item.address = address
		item.received = received
		item.accepted = accepted
		item.status = status

		self.items.append(item)

class GiftsOutsideUK(Category):
	def __init__(self):
		"""
		Gifts from outside the UK
		"""

		# Init the class, then set some class specific variables
		Category.__init__(self)

		# category info
		self.category_id = 6
		self.category_type = 'gifts_outside_uk'
		self.category_description = 'Gifts Outside UK'
		self.isCurrency = True

	def do_logic(self, raw_string):
		"""
		Method performing the logic of parsing raw data into dictionary
		"""

		amount = 0
		next_id = len(self.items) + 1
		item_id = '%04d' % next_id

		# not much we can really split on
		pretty = raw_string.split(' (Registered')[0]
		registered = regex_for_registered(raw_string)

		# hold a list of lists with search pair, to then regex out the value between them
		regex_pairs = []
		regex_pairs.append(['Name of donor: ', 'Address of donor: '])
		regex_pairs.append(['Address of donor: ', 'Amount of donation or nature and value if donation in kind: '])
		regex_pairs.append(['Amount of donation or nature and value if donation in kind:', 'Date received: '])
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
				elif 'address of donor' in pair[0].lower():
					address = value
				elif 'received' in pair[0].lower():
					received = value
				elif 'accepted' in pair[0].lower():
					accepted = value
				elif 'donor status' in pair[0].lower():
					status = value
				elif 'amount' in pair[0].lower():
					pretty = value

		item = GiftsItem(item_id, self.category_id, raw_string, pretty, registered, amount)
		item.donor = donor
		item.address = address
		item.received = received
		item.accepted = accepted
		item.status = status

		self.items.append(item)
