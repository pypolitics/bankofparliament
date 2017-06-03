# local libs

from categories import Category
from items import SalaryItem, AdditionalSalaryItem
from utils import regex_for_registered, regex_for_amount
from mps_salaries import salaries

class Salary(Category):
	def __init__(self, offices, forname, surname, party):
		"""
		Salary
		"""
		self.offices = offices
		self.forname = forname
		self.surname = surname
		self.party = party

		# lists of raw entries and parsed entries (dictionaries)
		self.raw_entries = []
		self.entries = []
		self.items = []

		# category info
		self.category_type = 'salary'
		self.category_id = 13
		self.category_description = 'Public Employment'
		self.isCurrency = True

		# basic salary of on MP, as of April 1st 2016
		self.basic_salary = 74962
		self.panel_of_chairs_salary = 15025
		self.chair_salary = 15025

		self.add_basic_salary()
		self.do_logic(None)

		self.category_income = self.income
		self.category_wealth = self.wealth
		self.category_gifts = self.gifts
		self.category_donations = self.donations
		self.category_amount = self.amount

	def add_basic_salary(self):
		"""
		Add basic mp salary
		"""

		next_id = len(self.items) + 1
		item_id = '%04d' % next_id

		# not much we can really split on
		raw_string = 'Basic Salary'
		pretty = 'Basic Salary'
		registered = regex_for_registered(raw_string)
		amount = self.basic_salary

		self.items.append(SalaryItem(item_id, self.category_id, raw_string, pretty, registered, amount))

	def do_logic(self, raw):
		"""
		Method performing the logic of parsing raw data into dictionary
		"""

		if self.offices:
			for office in self.offices:
				dept = office['dept']
				position = office['position']
				pretty = ''
				registered = None
				amount = 0

				if dept == 'Panel of Chairs':
					amount = self.panel_of_chairs_salary
					pretty = dept

				if 'Committee' in dept and position == 'Chair':
					amount = self.chair_salary
					pretty = dept

				for pos in salaries.keys():
					if pos in position:
						if not 'shadow' in position.lower():
							amount = salaries[pos]
							pretty = position			

				next_id = len(self.entries) + 1
				item_id = '%04d' % next_id
				raw_string = pretty

				if amount > 0:
					self.items.append(AdditionalSalaryItem(item_id, self.category_id, raw_string, pretty, registered, amount))

