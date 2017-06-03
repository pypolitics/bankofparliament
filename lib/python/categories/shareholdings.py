# local libs

from categories import Category
from items import ShareholdingsItem, OtherShareholdingsItem
from utils import regex_for_registered, regex_for_amount, get_companies_house_person

class Shareholdings(Category):
	def __init__(self, companies_house_user, names=[]):
		"""
		Shareholdings

		TODO: regex for percentage share, then lookup companies house
		then use that value for item amount 

		"""

		# Init the class, then set some class specific variables
		Category.__init__(self)

		# category info
		self.category_id = 8
		self.category_type = 'shareholdings'
		self.category_description = 'Shareholdings'
		self.isCurrency = False
		self.names = names
		self.companies_house_user = companies_house_user

	def do_logic(self, raw_string):
		"""
		Method performing the logic of parsing raw data into item class
		"""

		next_id = len(self.items) + 1
		item_id = '%04d' % next_id

		# not much we can really split on
		pretty = raw_string.split(' (Registered')[0]
		registered = regex_for_registered(raw_string)
		amount = 1

		self.items.append(ShareholdingsItem(item_id, self.category_id, raw_string, pretty, registered, amount))

		companies_query = get_companies_house_person(user=self.companies_house_user, names=self.names, address=[])

class OtherShareholdings(Category):
	def __init__(self):
		"""
		Miscellaneous
		"""

		# Init the class, then set some class specific variables
		Category.__init__(self)

		# category info
		self.category_id = 9
		self.category_type = 'shareholdings'
		self.category_description = 'Other Shareholdings'
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
		amount = regex_for_amount(raw_string)
		if amount == 0:
			amount = 70000

		self.items.append(OtherShareholdingsItem(item_id, self.category_id, raw_string, pretty, registered, amount))
