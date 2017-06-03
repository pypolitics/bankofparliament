
# system libs
import os
from textblob import TextBlob

# local libs
from utils import PrettyPrintUnicode

class Item():
	def __init__(self, item_id, category_id, raw_string, pretty, registered, amount):
		"""
		Basic Item Class
		"""
		self.item_id = item_id
		self.category_id = category_id
		self.raw_string = raw_string
		self.pretty = pretty
		self.registered = registered
		self.amount = amount
		self.nouns = []

		self.isIncome = False
		self.isWealth = False
		self.isGift = False
		self.isDonation = False

		# pluck out nouns, maybe we make a word cloud out of it
		# or
		# use it them to query companies house, land registry
		self.get_nouns()

	def get_nouns(self):
		"""
		Use nlp to find nouns
		"""
		blob = TextBlob(self.raw_string)

		for word, tag in blob.tags:
			if tag in ['NNP', 'NN']:
				self.nouns.append(word.lemmatize())

	def pprint(self):
		"""
		Petty prints using custom pprint class, formatting unicode characters
		"""
		PrettyPrintUnicode().pprint(self.data)

	@property
	def data(self):
		"""
		Returns the class variables as a key/pair dict
		"""
		return vars(self)

class SalaryItem(Item):
	def __init__(self, item_id, category_id, raw_string, pretty, registered, amount):
		"""
		SalaryItem
		"""

		Item.__init__(self, item_id, category_id, raw_string, pretty, registered, amount)

		self.isIncome = True

class AdditionalSalaryItem(Item):
	def __init__(self, item_id, category_id, raw_string, pretty, registered, amount):
		"""
		AdditionalSalaryItem
		"""

		Item.__init__(self, item_id, category_id, raw_string, pretty, registered, amount)

		self.isIncome = True

class DirectDonationsItem(Item):
	def __init__(self, item_id, category_id, raw_string, pretty, registered, amount):
		"""
		DirectDonationsItem
		"""

		Item.__init__(self, item_id, category_id, raw_string, pretty, registered, amount)

		self.isDonation = True

class IndirectDonationsItem(Item):
	def __init__(self, item_id, category_id, raw_string, pretty, registered, amount):
		"""
		IndirectDonationsItem
		"""

		Item.__init__(self, item_id, category_id, raw_string, pretty, registered, amount)

		self.isDonation = True

class FamilyItem(Item):
	def __init__(self, item_id, category_id, raw_string, pretty, registered, amount):
		"""
		FamilyItem
		"""

		Item.__init__(self, item_id, category_id, raw_string, pretty, registered, amount)

class FamilyLobbyistsItem(Item):
	def __init__(self, item_id, category_id, raw_string, pretty, registered, amount):
		"""
		FamilyLobbyistsItem
		"""

		Item.__init__(self, item_id, category_id, raw_string, pretty, registered, amount)

class MiscellaneousItem(Item):
	def __init__(self, item_id, category_id, raw_string, pretty, registered, amount):
		"""
		MiscellaneousItem
		"""

		Item.__init__(self, item_id, category_id, raw_string, pretty, registered, amount)

class ShareholdingsItem(Item):
	def __init__(self, item_id, category_id, raw_string, pretty, registered, amount):
		"""
		ShareholdingsItem
		"""

		Item.__init__(self, item_id, category_id, raw_string, pretty, registered, amount)

		self.isWealth = True

class OtherShareholdingsItem(Item):
	def __init__(self, item_id, category_id, raw_string, pretty, registered, amount):
		"""
		OtherShareholdingsItem
		"""

		Item.__init__(self, item_id, category_id, raw_string, pretty, registered, amount)

		self.isWealth = True

class GiftsItem(Item):
	def __init__(self, item_id, category_id, raw_string, pretty, registered, amount):
		"""
		GiftsItem
		"""

		Item.__init__(self, item_id, category_id, raw_string, pretty, registered, amount)

		self.isGift = True

class GiftsOutsideUKItem(Item):
	def __init__(self, item_id, category_id, raw_string, pretty, registered, amount):
		"""
		GiftsOutsideUKItem
		"""

		Item.__init__(self, item_id, category_id, raw_string, pretty, registered, amount)

		self.isGift = True

class VisitsOutsideUKItem(Item):
	def __init__(self, item_id, category_id, raw_string, pretty, registered, amount):
		"""
		VisitsOutsideUKItem
		"""

		Item.__init__(self, item_id, category_id, raw_string, pretty, registered, amount)

		self.isGift = True

class EmploymentItem(Item):
	def __init__(self, item_id, category_id, raw_string, pretty, registered, amount):
		"""
		EmploymentItem
		"""

		Item.__init__(self, item_id, category_id, raw_string, pretty, registered, amount)

		self.isIncome = True

class PropertyItem(Item):
	def __init__(self, item_id, category_id, raw_string, pretty, registered, amount):
		"""
		PropertyItem
		"""

		Item.__init__(self, item_id, category_id, raw_string, pretty, registered, amount)

		# could be either wealth or income or both
