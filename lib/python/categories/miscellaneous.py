# local libs

from categories import Category
from items import MiscellaneousItem
from utils import regex_for_registered, regex_for_amount

class Miscellaneous(Category):
	def __init__(self):
		"""
		Miscellaneous
		"""

		# Init the class, then set some class specific variables
		Category.__init__(self)
		
		# category info
		self.category_id = 10
		self.category_type = 'miscellaneous'
		self.category_description = 'Miscellaneous'
		self.isCurrency = False

	def do_logic(self, raw_string):
		"""
		Method performing the logic of parsing raw data into item class
		"""

		next_id = len(self.items) + 1
		item_id = '%04d' % next_id

		# not much we can really split on
		pretty = raw_string.split(' (Registered')[0]
		registered = regex_for_registered(raw_string)
		amount = regex_for_amount(raw_string)

		self.items.append(MiscellaneousItem(item_id, self.category_id, raw_string, pretty, registered, amount))
