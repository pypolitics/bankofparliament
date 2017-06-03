# local libs

from categories import Category
from items import PropertyItem
from utils import regex_for_registered

class Property(Category):
	def __init__(self):
		"""
		Property
		"""

		# Init the class, then set some class specific variables
		Category.__init__(self)
		
		# category info
		self.category_id = 7
		self.category_type = 'property'
		self.category_description = 'Property'
		self.isCurrency = True

	def do_logic(self, raw_string):
		"""
		Method performing the logic of parsing raw data into item class
		"""

		next_id = len(self.items) + 1
		item_id = '%04d' % next_id

		# not much we can really split on
		pretty = raw_string.split(' (Registered')[0]
		registered = regex_for_registered(raw_string)
	
		wealth = False
		income = False
		if '(i)' in raw_string:
			amount = 100000
			item = PropertyItem(item_id, self.category_id, raw_string, pretty, registered, amount)
			item.isWealth = True
			wealth = True
			self.items.append(item)

		if '(ii)' in raw_string:
			amount = 10000

			if wealth:
				# as simgle raw item can be both income and wealth, if it is, make two
				# items, which of course requires different ids
				nn = next_id + 1
				item_id = '%04d' % nn

			item = PropertyItem(item_id, self.category_id, raw_string, pretty, registered, amount)
			item.isIncome = True
			self.items.append(item)
