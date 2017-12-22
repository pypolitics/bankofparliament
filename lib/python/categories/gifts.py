# local libs

from categories import Category
from items import GiftsItem
from utils import regex_for_registered, regex_for_amount, get_regex_pair_search, string_to_datetime
import pprint

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

	def do_logic(self, raw_string, raw_data):
		"""
		Method performing the logic of parsing raw data into dictionary
		"""

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

		item = GiftsItem(item_id, self.category_id, raw_string, pretty, registered, amount)
		item.donor = donor
		item.address = address
		item.status = status
		item.raw_data = raw_data
		item.lookup()
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

	def do_logic(self, raw_string, raw_data):
		"""
		Method performing the logic of parsing raw data into dictionary
		"""
		next_id = len(self.items) + 1
		item_id = '%04d' % next_id

		# not much we can really split on
		pretty = raw_string.split(' (Registered')[0]
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

		item = GiftsItem(item_id, self.category_id, raw_string, pretty, registered, amount)
		item.donor = donor
		item.address = address
		item.status = status
		item.raw_data = raw_data
		item.lookup()
		self.items.append(item)
