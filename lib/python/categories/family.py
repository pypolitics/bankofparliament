# local libs

from categories import Category
from items import FamilyItem, FamilyLobbyistsItem
from utils import regex_for_registered

class FamilyLobbyists(Category):
	def __init__(self):
		"""
		Family Lobbyists
		"""

		# Init the class, then set some class specific variables
		Category.__init__(self)

		# category info
		self.category_id = 12
		self.category_type = 'family_lobbyists'
		self.category_description = 'Family Lobbyists'
		self.isCurrency = False

	def do_logic(self, raw_string):
		"""
		Method performing the logic of parsing raw data into item class
		"""

		amount = None
		next_id = len(self.items) + 1
		item_id = '%04d' % next_id

		# not much we can really split on
		pretty = raw_string.split(' (Registered')[0]
		registered = regex_for_registered(raw_string)

		item = FamilyLobbyistsItem(item_id, self.category_id, raw_string, pretty, registered, amount)

		self.items.append(item)

class Family(Category):
	def __init__(self):
		"""
		Family
		"""

		# Init the class, then set some class specific variables
		Category.__init__(self)
		
		# category info
		self.category_id = 11
		self.category_type = 'family'
		self.category_description = 'Family'
		self.isCurrency = False

	def do_logic(self, raw_string):
		"""
		Method performing the logic of parsing raw data into item class
		"""

		amount = None
		next_id = len(self.items) + 1
		item_id = '%04d' % next_id

		# not much we can really split on
		pretty = raw_string.split(' (Registered')[0]
		registered = regex_for_registered(raw_string)

		self.items.append(FamilyLobbyistsItem(item_id, self.category_id, raw_string, pretty, registered, amount))
		