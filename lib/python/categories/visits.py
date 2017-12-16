# local libs
import re

from categories import Category
from items import VisitsOutsideUKItem
from utils import regex_for_registered, regex_for_amount, get_regex_pair_search

class VisitsOutsideUK(Category):
	def __init__(self):
		"""
		Visits outside the UK
		"""

		# Init the class, then set some class specific variables
		Category.__init__(self)

		# category info
		self.category_id = 5
		self.category_type = 'visits_outside_uk'
		self.category_description = 'Visits Outside UK'
		self.isCurrency = True

	def do_logic(self, raw_string, raw_data):
		"""
		Method performing the logic of parsing raw data into dictionary
		"""

		amount = 0
		next_id = len(self.items) + 1
		item_id = '%04d' % next_id

		# not much we can really split on
		pretty = raw_string.split(' (Registered')[0]
		registered = regex_for_registered(raw_string)
		amount = regex_for_amount(raw_string)

		donor = raw_data['raw_string']
		address = ''
		destination = ''
		purpose = ''
		status = 'visit'

		indiv = re.search('\([0-9]+\)', donor)

		for key in raw_data:

			if 'purpose' in key.lower():
				purpose = raw_data[key]
			elif 'destination' in key.lower():
				destination = raw_data[key]

		for key in raw_data:

			if 'name of donor' in key.lower():
				# name of donor might be: (1) Policy Network (2) Les Gracques
				# split to list
				# TODO
				donor = raw_data[key]
				pretty = donor

			elif 'address' in key.lower():
				address = raw_data[key]

		item = VisitsOutsideUKItem(item_id, self.category_id, raw_string, pretty, registered, amount)
		item.donor = donor
		item.address = address
		item.destination = destination
		item.purpose = purpose
		item.status = status
		item.lookup()
		self.items.append(item)
