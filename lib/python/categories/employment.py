# local libs

from categories import Category
from items import EmploymentItem
from utils import regex_for_registered, regex_for_amount

class Employment(Category):
	def __init__(self):
		"""
		Employment
		"""

		# Init the class, then set some class specific variables
		Category.__init__(self)

		# category info
		self.category_id = 1
		self.category_type = 'employment'
		self.category_description = 'Private Employment'
		self.isCurrency = True


	def do_logic(self, raw_string):
		"""
		Method performing the logic of parsing raw data into item class
		"""

		# NOTE: usually the register uses 'Hours' to note time taken -  very clunky but works the moment
		# TODO: need to be able to parse hours values into mins, hours, days - basically interpret whatever
		# was filled in on their form.
		# TODO: need to decipher if the amount earned, was donated to party, charity etc
		# TODO: if possible find the employer - could also check companies house to investigate further the links
		# of the employer, other directors, other MPs, relatives etc
		if 'Hours:' in raw_string:

			amount = regex_for_amount(raw_string) 

			if 'monthly salary' in raw_string.lower():
				amount = amount * 12

			elif 'a month' in raw_string.lower():
				amount = amount * 12

			next_id = len(self.items) + 1
			item_id = '%04d' % next_id

			# not much we can really split on
			pretty = raw_string.split(' (Registered')[0]
			registered = regex_for_registered(raw_string)

			self.items.append(EmploymentItem(item_id, self.category_id, raw_string, pretty, registered, amount))
