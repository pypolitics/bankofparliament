# system  libs
import locale
import inspect

# local libs
from utils import padded_string

class Category():
	'''
	Class holding a category. Is populated with individual items, each of the same category type
	'''
	def __init__(self):

		# lists of raw entries and parsed entries (dictionaries)
		self.raw_items = []
		# self.entries = []
		self.items = []
		
		# category info
		self.category_id = 0
		self.category_type = 'category'
		self.category_description = 'Category Description'

		# class variables, used for sorting, printing
		self.isCurrency = True

	@property
	def isEmpty(self):
		"""
		Boolean
		"""
		if len(self.raw_items) == 0:
			return True
		else:
			return False

	def parse(self):
		"""
		Parse the list of raw data strings into entry dictionaries based on self.template
		"""

		# process the raw
		for raw in self.raw_items:
			self.do_logic(raw)

		# add some variables for the category
		# decorators arent stored as local class variables, but....
		# i automatically store class varibales using vars(self), to build a dict structure
		# ready for writing to json, so need to create class variables manually
		self.category_income = self.income
		self.category_wealth = self.wealth
		self.category_gifts = self.gifts
		self.category_donations = self.donations
		self.category_amount = self.amount

	def do_logic(self, raw):
		"""
		Method performing the logic of parsing raw data into dictionary
		"""

		pass

	@property
	def wealth(self):
		"""
		Sums all the wealth in the list of items
		"""
		value = 0	
		for entry in self.items:
			if entry.isWealth:
				value += entry.amount
		
		return value

	@property
	def income(self):
		"""
		Sums all the income in the list of items
		"""
		value = 0
		for entry in self.items:
			if entry.isIncome:
				value += entry.amount
		
		return value

	@property
	def gifts(self):
		"""
		Sums all the gifts in the list of items
		"""
		value = 0
		for entry in self.items:
			if entry.isGift:
				value += entry.amount
		
		return value

	@property
	def amount(self):
		"""
		Sums all the donations in the list of items
		"""
		value = 0
		for entry in self.items:
			if entry.amount:
				value += entry.amount
		
		return value

	@property
	def donations(self):
		"""
		Sums all the donations in the list of items
		"""
		value = 0
		for entry in self.items:
			if entry.isDonation:
				value += entry.amount
		
		return value

	@property
	def expenses(self):
		"""
		Sums all the expenses in the list of items
		"""
		value = 0
		for entry in self.items:
			if entry.isExpense:
				value += entry.amount
		
		return value

	@property
	def data(self):
		"""
		Returns the class variables as a key/pair dict
		"""
		return vars(self)

	def add_entry(self, raw_data):
		"""
		Adds raw data, in the form of a string to a list of raw entries
		"""
		self.raw_items.append(raw_data)
