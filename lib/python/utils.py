# -*- coding: utf-8 -*-

# system libs
import requests, time, ast, locale, pprint, re, shutil, os, sys
reload(sys) 
sys.setdefaultencoding('utf8')

from datetime import datetime
import xml.etree.cElementTree as ElementTree
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

companies_house_user = 'ZCCtuxpY7uvkDyxLUz37dCYFIgke9PKfhMlEGC-Q'

# Classes
class PrettyPrintUnicode(pprint.PrettyPrinter):
    """
    Subclassed Pretty Printer which handles unicode characters correctly
    """
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return (object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)

class XmlListConfig(list):
    """
    Subclassed list class for xml parsing
    """
    def __init__(self, aList):
        for element in aList:
            # print element
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)

class XmlDictConfig(dict):
    """
    Subclassed dictionary class for xml parsing
    """
    def __init__(self, parent_element):
        childrenNames = []
        for child in parent_element.getchildren():
            childrenNames.append(child.tag)

        if parent_element.items(): #attributes
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                #print len(element), element[0].tag, element[1].tag
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself
                    aDict = {element[0].tag: XmlListConfig(element)}
                # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))

                if childrenNames.count(element.tag) > 1:
                    try:
                        currentValue = self[element.tag]
                        currentValue.append(aDict)
                        self.update({element.tag: currentValue})
                    except: #the first of its kind, an empty list must be created
                        self.update({element.tag: [aDict]}) #aDict is written in [], i.e. it will be a list

                else:
                     self.update({element.tag: aDict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})

def get_request(url, user=None, headers={}, request_wait_time=300.00):
    # print url
    if user:
        request = requests.get(url, auth=(user, ''), headers=headers)
    else:
        request = requests.get(url, headers=headers)
    
    if request.status_code == 200:
        return request

    # too many requests
    if request.status_code == 429:
        print '*'*100
        print "Too Many Requests, wait for %s seconds" % str(request_wait_time)
        print '*'*100
        time.sleep(request_wait_time)
        return get_request(url, user, headers)
    else:
        return request

def get_all_mps(theyworkyou_apikey):
	"""
    Function to return a full list of current MPs
    """
	url = 'https://www.theyworkforyou.com/api/getMPs?key=%s&output=js' % (theyworkyou_apikey)
	request = get_request(url=url, user=None, headers={})
	# literal eval the json request into actual json
	literal = ast.literal_eval(request.content)

	return literal

def get_companies_house_person(user, names=[], addresses=[]):
    """
    Function to return companies house records, searching with 
    a given list of names
    """

    search_string = ''
    for name in names:
        search_string += '%s+' % name

    # split the last '+' off
    search_string = search_string[:-1]

    url = 'https://api.companieshouse.gov.uk/search/officers?q=%s&items_per_page=100' % (search_string)
    request = get_request(url=url, user=user)

    literal = ast.literal_eval(request.content)
    j = request.json()

    return j

def get_house_of_commons_member(constituency):

    search_criteria = 'House=Commons|IsEligible=true|constituency=%s' % (constituency)
    outputs = 'BasicDetails|Addresses|PreferredNames'
    url = 'http://data.parliament.uk/membersdataplatform/services/mnis/members/query/%s/%s' % (search_criteria, outputs)

    headers = {'Accept': 'application/json'}
    request = get_request(url=url, user=None, headers=headers)

    # replace null with None
    content = request.content.replace("null", "None")
    a = ast.literal_eval(content)

    members = a['Members']['Member']
    return members

def filter_by_first_last_name(data, first_name, last_name, name):
    """
    Function to filter companies house records, attempting to match
    only the record with the exact same name as the member of parliament
    doesnt necessairly mean the filtered record IS the mp, just that they
    share a name.

    If we have more info about the mp, like date of borth or address, we would
    have a better chance of matching them.

    Additional names and addresses are available from data.parliament, but not until
    a government is formed.
    """

    matched_people = []

    for i in data['items']:

      if first_name in i['title'].lower():

          if last_name in i['title'].lower():

              matched_people.append(i)

    return matched_people

def filter_by_appointment_counts(data, count=0):
    """
    Function to filter companies house records, removing those that do not have appointments
    """

    matched_people = []

    for i in data:

        if i['appointment_count'] > count:
            matched_people.append(i)

    return matched_people

def get_mp_image(name, first_name, last_name, memid, output_path):
    """
    Function to return an image

    Due to parliament being dissolved at 12:01 on 03/05/2017, the members query returns nothing,
    simply because there are no members of parliament right now.

    For now, use an offline xml version.

    """

    # find the mp id from data.parliament
    url = 'http://data.parliament.uk/membersdataplatform/services/mnis/members/query/name*%s/' % (name)
    request = get_request(url=url, user=None, headers={'content-type' : 'application/json'})
    filepath = '%s/%s.jpg' % (output_path, memid)
    # print filepath

    if os.path.isfile(filepath):
        print 'Image Exists'
        return

    try:
        js = request.json()
        member_id = js['Members']['Member']['@Member_Id']

        # find the member photo
        url = 'http://data.parliament.uk/membersdataplatform/services/images/MemberPhoto/%s/Web Photobooks' % member_id

        response = requests.get(url, stream=True)

        with open(filepath, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
            print 'Downloaded : %s' % filepath
        del response
    except:
        pass

def get_xml_dict(xml_file):
    """
    Returns an xml_file as a dictionary
    """
    tree = ElementTree.parse(xml_file)
    root = tree.getroot()
    xmldict = XmlDictConfig(root)
    return xmldict['regmem']

def string_to_datetime(date_string):
    """
    Returns a datetime class from a given string
    """
    return datetime.strptime(date_string, '%d %B %Y')

def padded_string(string, padding=100):
    """
    Return a padded string
    """
    return string.ljust(padding)

def regex_for_registered(raw_string):
    """
    Returns a date class formatted string
    """
    registered_regex = re.compile(r'\((.*?\))')
    registered_regex = re.compile(r"\bRegistered\b \d+ [A-Z][a-z]+ \d+")

    if registered_regex.findall(raw_string.encode('utf-8'), re.UNICODE):
        match = registered_regex.findall(raw_string)
        date = str(match[-1].split('Registered ')[-1])
        return string_to_datetime(date).strftime("%d/%m/%Y")
    else:
        return None

def regex_for_amount(raw_string):
    """
    Return integer amount
    """
    amount_regex = re.compile(r"£\d+")

    if amount_regex.search(raw_string.replace(',','').encode('utf-8')):
        return int(amount_regex.search(raw_string.replace(',', '').encode('utf-8')).group().split('£')[-1])
    else:
        return 0

def get_regex_pair_search(pair, raw_string):
    """
    Return a regex search class
    """
    return re.search(r'%s(.*?)%s' % (pair[0], pair[1]), raw_string)

def get_other_officers(user):
    """
    Query the other officers connected to the company
    """
    for appointment in user['appointments']['items']:
        if appointment['company'].has_key('links'):

            links = appointment['company']['links']
            if links.has_key('officers'):

                other_officers_link = links['officers']

                url = 'https://api.companieshouse.gov.uk%s' % other_officers_link
                other_officers = get_request(url=url, user=companies_house_user, headers={})

                try:
                    other_officers = other_officers.json()
                    appointment['other_officers'] = other_officers
                
                except:
                    pass

def get_filling_history(user):
    """
    Query the filing history of the company
    """
    for appointment in user['appointments']['items']:
        if appointment['company'].has_key('links'):

            links = appointment['company']['links']

            if links.has_key('filing_history'):

                filing_history_link = links['filing_history']

                url = 'https://api.companieshouse.gov.uk%s' % filing_history_link
                filing_history = get_request(url=url, user=companies_house_user, headers={})

                try:
                    filing_history = filing_history.json()
                    appointment['filing_history'] = filing_history
                
                except:
                    pass

def get_companies(user):
    """
    Query the company of the appointment
    """
    for appointment in user['appointments']['items']:
        appointment['company'] = {}
        appointment['company']['items'] = []

        company_number = appointment['appointed_to']['company_number']
        url = 'https://api.companieshouse.gov.uk/company/%s' % company_number

        companies = get_request(url=url, user=companies_house_user, headers={})
        
        try:
            companies = companies.json()
            appointment['company'] = companies
        
        except:
            pass

def get_appointments(user):
    """
    Query the appointments of the user
    """

    self_link = user['links']['self']
    url = 'https://api.companieshouse.gov.uk%s' % self_link

    appointments = get_request(url=url, user=companies_house_user, headers={})

    try:
        appointments = appointments.json()
        user['appointments'] = appointments

    except:
        user['appointments'] = {}
        user['appointments']['items'] = []

def contains_mp(vals):
    """
    Check if a list of values contain our keywords
    """

    search_for = ['parliament', 'politician', 'commons', 'member', 'SW1A' '0AA']

    for search in search_for:
        for v in vals:
            if search.lower() in v.lower():
                return True
    return False

def value_recurse(data, vals=[]):
    """
    Return a list of values from given data, dict, nested dict etc etc
    """

    # make data a list
    if isinstance(data, dict):
        data = [data]
    elif isinstance(data, list):
        data = data
    else:
        data = [data]

    # list of dicts
    for d in data:

        # ok, data is a list, but what of its contents
        if isinstance(d, dict):
            for k, v in d.iteritems():

                if isinstance(v, dict):
                    value_recurse([v], vals)
                elif isinstance(v, list):
                    value_recurse(v, vals)
                else:
                    vals.append(str(v))

        elif isinstance(d, list):
            value_recurse(d, vals)
        
        else:
            vals.append(str(d))

    return vals


def decoded(data):
    """
    Decode data items
    """
    for i in data['items']:
        i['title'].encode('utf-8')

    return data

def fuzzy_filter(data, first_name, middle_name, last_name, addresses=[]):
    """
    Perform fuzzy logic on name matching
    """

    # set the fuzzy ratio threshold value
    ratio_threshold = 50

    top_ratio = []
    for i in data:

        title = i['title'].lower()
        name = '%s %s' % (first_name, last_name)
        if middle_name != '':
            name = '%s %s %s' % (first_name, middle_name, last_name)

        ratio = fuzz.token_sort_ratio(name, title)

        if int(ratio) >= ratio_threshold:
            i['fuzzy_ratio'] = ratio
            top_ratio.append(i)
    
    return top_ratio

def get_companies_house_users(member):
    """Get data from companies house"""

    # id
    member_id = member['@Member_Id']

    # names
    first_name = member['BasicDetails']['GivenForename'].lower()
    last_name = member['BasicDetails']['GivenSurname'].lower()

    middle_name = ''
    if member['BasicDetails']['GivenMiddleNames']:
        middle_name = member['BasicDetails']['GivenMiddleNames'].lower()
 
    #############################################################################################################################
    # basic search
    if middle_name != '':
        url = 'https://api.companieshouse.gov.uk/search/officers?q=%s+%s+%s&items_per_page=100' % (first_name, middle_name, last_name)
    else:
        url = 'https://api.companieshouse.gov.uk/search/officers?q=%s+%s&items_per_page=100' % (first_name, last_name)

    url = url.replace(' ', '+')

    r = get_request(url=url, user=companies_house_user, headers={})
    data = r.json()
    data = decoded(data)

    # filter the data
    data = filter_by_first_last_name(data, first_name, middle_name, last_name)
    data = filter_by_appointment_counts(data)
    data = fuzzy_filter(data, first_name, middle_name, last_name)

    # these are the matched companieshouse users - queried by name only, filtered a little bit
    return data
