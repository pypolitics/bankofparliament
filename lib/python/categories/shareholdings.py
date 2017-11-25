# local libs
from categories import Category
from items import ShareholdingsItem, OtherShareholdingsItem
from utils import regex_for_registered, regex_for_amount, regex_for_percent, getlink, get_request
from companies_house_query import CompaniesHouseCompanySearch
from pprint import pprint
import re
from datetime import datetime, date
from companies_house_patches import urls

class Shareholdings(Category):
	def __init__(self, extended, keywords, month, year, first, middle, last, display):
		"""
		Shareholdings

		TODO: regex for percentage share, then lookup companies house
		then use that value for item amount 

		"""
		self.month = month
		self.year = year
		self.first = first
		self.middle = middle
		self.last = last
		self.display = display

		# Init the class, then set some class specific variables
		Category.__init__(self)

		# category info
		self.category_id = 8
		self.category_type = 'shareholdings'
		self.category_description = 'Shareholdings'
		self.isCurrency = False

	def do_logic(self, raw_string):
		"""
		Method performing the logic of parsing raw data into item class.

		Here im just look for the company link. I need to verify that the mp has significant control or
		is an officer to double check.
		"""
		matched_company = {}

		next_id = len(self.items) + 1
		item_id = '%04d' % next_id

		# not much we can really split on
		pretty = raw_string.split(' (Registered')[0]
		registered = regex_for_registered(raw_string)

		if self.category_description == 'Shareholdings':
			amount = 1
			amount = regex_for_percent(raw_string)
		elif self.category_description == 'Other Shareholdings':
			amount = regex_for_amount(raw_string)
			if amount == 0:
				amount = 70000

		# were looking for:
		company = None
		url = ''

		print '\tRaw String : %s' % raw_string

		# check if we have pre-defined this
		if raw_string in urls.keys():
			print '\tPatched : %s' % urls[raw_string]
			company = patched_company(urls[raw_string])
			# test the patch url, may have been set to ''
			if company.has_key('company_name'):
				company['title'] = company['company_name']
			else:
				company = {}
				company_search_string = ''

		if not company and company != {}:
			# no patches have been applied
			company_search_string = make_search_string(raw_string)
			print '\tSearch String : %s' % company_search_string

			# do the query
			limit = '50'
			if len(company_search_string.split(' ')) > 5:
				limit = '100'
			companies = CompaniesHouseCompanySearch(queries=[company_search_string], limit=limit)

			for i in companies.data:
				# check for matches, when one if found, break the loop
				if check_match(i, company_search_string, self.month, self.year, self.first, self.middle, self.last, self.display):
					company = i
					break

		if company:
			print '\tMatched Company : %s\n' % company['title']
			link = company['links']['self']
			url = 'https://beta.companieshouse.gov.uk%s' % link
		else:
			print '\t\tUnatched Company : %s\n' % (company_search_string)
			company = {}

		self.items.append(ShareholdingsItem(item_id, self.category_id, raw_string, pretty, registered, amount, company, url))

	@property
	def data(self):
		"""
		Returns the class variables as a key/pair dict
		"""
		return vars(self)

class OtherShareholdings(Shareholdings):
	def __init__(self, extended, keywords, month, year, first, middle, last, display):
		"""
		Miscellaneous
		"""
		self.month = month
		self.year = year
		self.first = first
		self.middle = middle
		self.last = last
		self.display = display

		# Init the class, then set some class specific variables
		Category.__init__(self)

		# category info
		self.category_id = 9
		self.category_type = 'shareholdings'
		self.category_description = 'Other Shareholdings'
		self.isCurrency = True

def cleanup_raw_string(raw, keep_numbers=False):
    """Cleanup a raw string from the register of intrests, ready for querying with"""

    raw = raw.lower()
    raw_list = raw.split(' ')

    exclude = ['shareholder', 'director', 'of', 'services', 'service', 'recruitment', 'international', 'specialist', '(', ')', '%', 'registered', '', 'from', 'an', 'a', 'company', 'shareholding', 'shareholdings', 'business']
    # exclude = ['shareholder', 'director', 'of', 'specialist', '(', ')', '%', 'registered', '', 'from', 'an', 'a', 'company', 'shareholding', 'shareholdings']

    # remove any days or months in the raw string
    months = [date(2000, m, 1).strftime('%b').lower() for m in range(1, 13)]
    months_short = [date(2000, m, 1).strftime('%B').lower() for m in range(1, 13)]
    for i in months:
        exclude.append(i)
    for i in months_short:
        exclude.append(i)

    found = []
    for r in raw_list:
        if r not in exclude:

            if not keep_numbers:
                try:
                    r = int(r)
                    pass
                except:
                    found.append(r)
            else:
                found.append(r)

    cleanup = ' '.join(found)
    if cleanup.startswith('and '):
    	cleanup = cleanup[3:]
    return cleanup

def make_search_string(raw_string):
	"""
	build a useful search string, from a given raw string
	"""
	company_search_string = raw_string.split(' (Registered')[0].lower()

	from_regex = re.compile('(?:from|until) [0-9]+ [a-zA-Z0-9]+ [a-zA-Z0-9]+,')
	if from_regex.search(company_search_string):
		f = from_regex.search(company_search_string).group()
		company_search_string = company_search_string.replace(f, '')

	from_regex = re.compile('since [a-zA-Z0-9]+ [a-zA-Z0-9]+,')
	if from_regex.search(company_search_string):
		f = from_regex.search(company_search_string).group()
		company_search_string = company_search_string.replace(f, '')

	# spit on semi colon first, take the first index
	split_on_semi = False
	if '; ' in company_search_string:
		company_search_string = company_search_string.split('; ')[0]
		split_on_semi = True

	if not split_on_semi:
		# split on comma, take the first index
		if ', ' in company_search_string:
			company_search_string = company_search_string.split(', ')[0]

	if '. ' in company_search_string:
		company_search_string = company_search_string.split('. ')[0]

	if 'non-trading' in company_search_string:
		company_search_string = company_search_string.replace('non-trading', '').strip()

	if 'non trading' in company_search_string:
		company_search_string = company_search_string.replace('non trading', '').strip()

	if 'trading as ' in company_search_string:
		company_search_string = company_search_string.split('trading as ')[0]

	if ' ltd' in company_search_string:
		company_search_string = company_search_string.split(' ltd')[0]

	if ' plc' in company_search_string:
		# if there are words (space after plc), replace it, rather than split as theres likely
		# to be words after it
		company_search_string = company_search_string.replace(' plc ', ' ')

	if ' limited' in company_search_string:
		company_search_string = company_search_string.split(' limited')[0]

	if 'share options held in ' in company_search_string:
		company_search_string = company_search_string.split('share options held in ')[-1]

	if 'i am the sole owner ' in company_search_string:
		company_search_string = company_search_string.split('i am the sole owner ')[-1]

	if 'partner in ' in company_search_string:
		company_search_string = company_search_string.split('partner in ')[-1]

	if 'interest in ' in company_search_string:
		company_search_string = company_search_string.split('interest in ')[-1]

	if 'corp ' in company_search_string:
		company_search_string = company_search_string.replace('corp ', 'corporation ')

	company_search_string = cleanup_raw_string(company_search_string, True)
	return company_search_string

def check_match(i, company_search_string, month, year, first, middle, last, display):
	"""
	get the first company that matches (in order):

		- if the search string exactly matches the company name
		- if everyword in search string in the company name
		- if previous company name matches the search string
		- if a person with significant control, matches the display name of mp
			- if the date of birth data is there, we test that too, if the name matches but
			  the dob is incorrect, then it cant be them. (michael gove has entered an incorrect dob though)
		- if an officer (who may also be a shareholder) matches the display name
			- if dob present, test that too
	"""
	title = i['title']

	# remove ltd and limited from search string, companies house dont match against it
	company_search_string_clean = company_search_string.lower().replace('ltd', '').replace('limited', '').strip()

	match_count = False
	if not match_count:
		'''
		this is the hardest to match against as the search string has to match exactly the company house record.
		'''
		if title.lower() == company_search_string:
			# is an exact string match - bingo
			match_count = True


	if not match_count:
		'''
		if the number of words searched for, matches the number of words found, this matches. it's got all the words.
		'''
		if i.has_key('matches'):
			if i['matches'].has_key('title'):
				title_match_list = i['matches']['title']

				title_tuples = [(title_match_list[x],title_match_list[x+1]) for x in range(0,len(title_match_list),2)]
				number_of_search_words = len(company_search_string_clean.split(' '))

				if number_of_search_words == len(title_tuples):
					# all the words in the search string are in the company title - bingo
					match_count = True

				# if there are 5 or more search words, lets account for one missing
				elif number_of_search_words > 5:
					if number_of_search_words -1 == len(title_tuples):
						match_count = True
				else:
					matched_words_company_title = []

					for tup in title_tuples:
						first_bit = tup[0] - 1
						last_bit = tup[-1]
						matched_words_company_title.append(title[first_bit:last_bit])

					# print matched_words_company_title
					# not sure how to proceed from here ?

	if not match_count:
		'''
		ok, so, no name match.
		lets get the company record and check previous_names, maybe the company has changed name
		'''
		company = getlink(i, 'self')
		previous_names = []
		if company.has_key('previous_company_names'):
			for c in company['previous_company_names']:
				previous_names.append(c['name'])

			for previous in previous_names:
				if previous.lower() == company_search_string.lower():
					match_count = True

	if not match_count:
		'''
		ok, no name matches or previous names. time to check the significant persons. these are people / companies
		that took shares at the formation of the company. subsequent investors aren't required to submit shareholder
		details, but many do. if the name of someone with significant control matches the mp, NOT the search string,
		then we can match against that instead. we verify with the date of birth, if present in companies house record.

		the companies house records arent consistent or complete, there are lots of gaps, which makes it hard to verify
		with a second value, such as date of birth or address. this is an ongoing problem.
		'''

		remove = ['mr', 'mrs', 'ms', 'miss', 'sir', 'lady', 'dr', 'rt', 'hon']

		persons = getlink(company, 'persons_with_significant_control')['items']
		for person in persons:
			# print ''
			keys = ['name', 'name_elements', 'date_of_birth', 'natures_of_control', 'country_of_residence']

			# check our display name, with the name key, strip out titles and check for an exact match
			person_name = person['name'].lower()
			person_string = ''
			for w in person_name.split(' '):
				if w not in remove:
					person_string += '%s ' % w
			person_string = person_string.strip()

			if person_string == display:
				match_count = True

	if not match_count:
		'''
		check officers
		'''
		remove = ['mr', 'mrs', 'ms', 'miss', 'sir', 'lady', 'dr', 'rt', 'hon']

		officers = getlink(company, 'officers')['items']
		for officer in officers:
			officer_name = officer['name']

			# sort out the name, it comes in as 'LAST, First'
			last_regex = re.compile('[A-Z]+, ')
			if last_regex.search(officer_name):
				last_match = last_regex.search(officer_name).group()

				first_match = officer_name.split(last_match)[-1]

				name = '%s %s' % (first_match, last_match.split(',')[0].lower())
				officer_name = name.lower()
			else:
				officer_name = officer_name.lower()

			# check our display name, with the name key, strip out titles and check for an exact match
			officer_string = ''
			for w in officer_name.split(' '):
				if w not in remove:
					officer_string += '%s ' % w
			officer_string = officer_string.strip()

			if officer_string == display:
				match_count = True
				break

			officer_splits = officer_string.split(' ')
			display_splits =  display.lower().split(' ')
			counter = 0

			# if all the display names are in the officer name, good, match that
			for sp in display_splits:
				if sp.lower() in officer_splits:
					counter += 1

			if counter == len(display_splits):
				match_count = True
				break

			if middle != '':
				if first in officer_splits and middle in officer_splits and last in officer_splits:
					match_count = True
					break
			if first in officer_splits and last in officer_splits:
				match_count = True
				break

	return match_count

def patched_company(patch):
	"""
	get a patched company
	"""
	companies_house_user = 'ZCCtuxpY7uvkDyxLUz37dCYFIgke9PKfhMlEGC-Q'
	headers = {}

	company_number = patch.split('/')[-1]
	url = 'https://api.companieshouse.gov.uk/company/%s' % (company_number)
	request = get_request(url=url, user=companies_house_user, headers=headers)
	data = request.json()
	return data
