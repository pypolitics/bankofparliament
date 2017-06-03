# local libs

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
		self.category_description = 'Vists outside UK'
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
		regex_pairs.append(['Address of donor: ', 'Amount of donation '])
		regex_pairs.append(['Address of donor: ', 'Estimate of the probable value'])
		regex_pairs.append(['Destination of visit: ', 'Dates of visit: '])
		regex_pairs.append(['Destination of visit: ', 'Date of visit: '])
		regex_pairs.append(['Dates of visit: ', 'Purpose of visit: '])
		regex_pairs.append(['Date of visit: ', 'Purpose of visit: '])
		regex_pairs.append(['Purpose of visit: ', r'\(Registered '])

		amount = regex_for_amount(raw_string)

		donor = None
		address = None
		destination = None
		dates = None
		purpose = None

		for pair in regex_pairs:
			regex_search = get_regex_pair_search(pair, raw_string)

			if regex_search:
				value = regex_search.group(1)

				if 'name of donor' in pair[0].lower():
					donor = value
				elif 'address of donor' in pair[0].lower():
					address = value
				elif 'destination' in pair[0].lower():
					destination = value
				elif 'date' in pair[0].lower():
					dates = value
				elif 'dates' in pair[0].lower():
					dates = value
				elif 'purpose' in pair[0].lower():
					pretty = value

		item = VisitsOutsideUKItem(item_id, self.category_id, raw_string, pretty, registered, amount)
		item.donor = donor
		item.address = address
		item.destination = destination
		item.dates = dates

		self.items.append(item)
