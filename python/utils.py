# -*- coding: utf-8 -*-

# system libs
import requests, time, ast, locale, pprint, re, shutil
from datetime import datetime
import xml.etree.cElementTree as ElementTree

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

# Functions
def get_request(url, user=None, headers={}, request_wait_time=3600.00):
	"""
    Function to return a http get request
    """

	if user:
		request = requests.get(url, auth=(user, ''), headers=headers)
	else:
		request = requests.get(url, headers=headers)

	if request.status_code == 201:
		print '*'*100
		print request.status_code
		print ''
		print "Ok, I'll wait for 5 mins"
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

def get_appointments(user, data, status=['active']):
    """
    Function to return appointmentsm, referenced in the officer dictionary

    Valid status:
        active
        liquidated
        dissolved

    """
    for user in data:

        appointment_dict = {}
        user['appointments'] = {}

        # get the officer id, and query that for appointments
        link = user['links']['self']
        officer_id = link.split('/')[2]

        url = 'https://api.companieshouse.gov.uk/officers/%s/appointments' % officer_id
        request = get_request(url=url, user=user, headers={})

        try:

            appointments = request.json()

            # sort the appointments into status keys, then we can look at active, dissolved, liquidated
            # companies of the member
            for app in appointments['items']:
                company_status = app['appointed_to']['company_status']
                print company_status, status
                if company_status in status:

                    if not appointment_dict.has_key(company_status):
                        appointment_dict[company_status] = []
                    
                    appointment_dict[company_status].append(app)

            # add the appointment_dict into the original user dict 
            user['appointments'] = appointment_dict

        except:
            pass

    return data

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

    # see if both first_name and last_name are in the title
    for i in data['items']:
        if first_name.lower() in i['title'].lower():
            if last_name.lower() in i['title'].lower():
                matched_people.append(i)

    # see if both names appear sequentially in the title
    for match in matched_people:
        if not name.lower() in match['title'].lower():
            matched_people.remove(match)

    # see if title startswith name
    for match in matched_people:
        if not match['title'].lower().startswith(name.lower()):
            matched_people.remove(match)

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
    filepath = '%s/%s_%s_%s.png' % (output_path, first_name, last_name, memid)

    try:
        js = request.json()
        member_id = js['Members']['Member']['@Member_Id']

        # find the member photo
        url = 'http://data.parliament.uk/membersdataplatform/services/images/MemberPhoto/%s/Web Photobooks' % member_id

        response = requests.get(url, stream=True)

        filepath = '%s/%s_%s_%s.png' % (output_path, first_name, last_name, memid)

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
