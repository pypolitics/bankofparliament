# -*- coding: utf-8 -*-

# system libs
import requests, time, ast, locale, pprint, re, shutil, os, sys, json
reload(sys) 
sys.setdefaultencoding('utf8')

from datetime import datetime
import xml.etree.cElementTree as ElementTree
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from datetime import datetime
from wordcloud import WordCloud

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

def regex_for_percent(raw_string):
    """
    Return integer amount
    """
    amount_regex = re.compile(r"\d+%")

    if amount_regex.search(raw_string):

        return int(amount_regex.search(raw_string).group().split('%')[0])
    else:
        return 15

def regex_for_ownership(raw_string):
    """
    Return integer amount
    """
    amount_regex = re.compile(r"\d+-to-\d+")

    if amount_regex.search(raw_string):
        return amount_regex.search(raw_string).group().split('-to-')
    else:
        return None

def get_regex_pair_search(pair, raw_string):
    """
    Return a regex search class
    """
    return re.search(r'%s(.*?)%s' % (pair[0], pair[1]), raw_string)

def getlink(data, link):

    if data.has_key('links'):
        if data['links'].has_key(link):

            link_url = data['links'][link]
            url = 'https://api.companieshouse.gov.uk%s' % link_url
            link_request = get_request(url=url, user=companies_house_user, headers={})

            try:
                l = link_request.json()
                if not l.has_key('items'):
                    l['items'] = []
                return l
            except:
                return {'items' : []}
    return {'items' : []}


def get_controlling_persons(user):
    """
    Query the other officers connected to the company
    """
    for appointment in user['appointments']['items']:

        appointment['company']['controlling_persons'] = []

        if appointment['company'].has_key('company_number'):
            company_number = appointment['company']['company_number']
            company_name = appointment['company']['company_name']

            url = 'https://api.companieshouse.gov.uk/company/%s/persons-with-significant-control' % company_number
            controlling_persons = get_request(url=url, user=companies_house_user, headers={})

            try:
                controlling_persons = controlling_persons.json()

                if controlling_persons.has_key('items'):

                    appointment['company']['controlling_persons'] = controlling_persons['items']
                    read_controlling_persons(appointment, user)

            except:
                pass


def read_controlling_persons(appointment, user):

    # were looking for ownership, we need to see if the appointee is also the
    # person with ownership rights

    # otherwise they are just on the board or havent a controlling shareholding of the company

    dob = user['date_of_birth']
    appointment['significant_ownership'] = ''
    appointment['ceased_significant_ownership'] = ''

    for person in appointment['company']['controlling_persons']:

        name =  person['name']
        kind = person['kind']
        control = person['natures_of_control']

        ownership = None

        for i in control:

            # for now all we care for is ownership, not voting rights etc
            if 'ownership' in i:
                ownership = i

                if kind == 'individual-person-with-significant-control':
                    # the entity of the controlling shareholder is a person, lets check to see
                    # if that person is the mp

                    self = person['links']['self']
                    url = 'https://api.companieshouse.gov.uk%s' % self

                    # get the controller object
                    controller = get_request(url=url, user=companies_house_user, headers={})
                    try:
                        controller = controller.json()

                        if controller['date_of_birth'] == dob:

                            if ownership:

                                if not controller.has_key('ceased_on'):
                                    appointment['significant_ownership'] = ownership
                                else:
                                    appointment['ceased_significant_ownership'] = ownership
                    except:
                        pass

                elif kind == 'corporate-entity-person-with-significant-control':
                    # so, we should find these companies and check to see if our user has controlling shares in
                    # that company
                    pass

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
                    appointment['company']['other_officers'] = other_officers

                    # these are officers of an mps company
                    for other in appointment['company']['other_officers']['items']:
                        link = other['links']['officer']['appointments']

                        apps = get_other_appointments(link)
                        other['other_appointments'] = apps
                
                except:
                    pass

def get_other_appointments(link):
    """
    Query the appointments of the user
    """

    url = 'https://api.companieshouse.gov.uk%s' % link

    appointments = get_request(url=url, user=companies_house_user, headers={})

    try:
        a = appointments.json()

    except:
        a = {}
        a['items'] = []

    return a['items']

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
                    appointment['company']['filing_history'] = filing_history
                
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
    # print url
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

    search_for = ['parliament', 'politician', 'commons', 'SW1A' '0AA', 'civil', 'minister', 'westminister']

    for search in search_for:
        for v in vals:
            if search.lower() in v.lower():
                # print 'MP FOUND : %s' % vals
                return True
    return False

def value_recurse(data):

    vals = []

    if data.has_key('address_snippet'):
        vals.append(data['address_snippet'])

    if data.has_key('title'):
        vals.append(data['title'])

    for app in data['appointments']['items']:

        if app.has_key('officer_role'):
            vals.append(app['officer_role'])

        if app.has_key('occupation'):
            vals.append(app['occupation'])

        if app.has_key('address'):

            for k, v in app['address'].iteritems():
                vals.append(v)

    clean = []
    for v in vals:
        if ' ' in v:
            spl = v.split(' ')
            for i in spl:
                clean.append(i.lower())

        else:
            clean.append(v.lower())

    return clean

def value_recurse_old(data=[], vals=[]):
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
                    value_recurse(v, vals)
                elif isinstance(v, list):
                    value_recurse(v, vals)
                else:
                    vals.append(str(v))

        elif isinstance(d, list):
            value_recurse(d, vals)
        
        else:
            vals.append(str(d))

    return vals

def value_recurse_keys(data, vals=[], keys=[]):
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
                    value_recurse_keys([v], vals, keys)
                elif isinstance(v, list):
                    value_recurse_keys(v, vals, keys)
                else:
                    vals.append(str(v))

        elif isinstance(d, list):
            value_recurse_keys(d, vals, keys)

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
    ratio_threshold = 75

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

def filter_by_dob(data, dob):
    """
    If the user has a 'date_of_birth' key, that matches the member dob, add to list to return.

    If no users were matched to dob, return the users that didnt have the 'date_of_birth' key. The ones that
    did have the key, we know they cant be the mp, unless the data is wrong. which i cant assume.

    """

    matched_people = []
    unmatched_people = []
    if dob != None:
        i = data

        if i.has_key('date_of_birth'):

            month = i['date_of_birth']['month']
            year = i['date_of_birth']['year']

            if month == dob.month:
                if year == dob.year:
                    matched_people.append(i)

        # we cant be sure they arent the mp, so add them
        else:
            unmatched_people.append(i)

        if len(matched_people) < 1:
            # if we havent found any, return the users that have no dob key
            # return unmatched_people
            return []
        else:
            return matched_people
    else:
        return []


def filter_by_name_string(data, display_as_name):
    """
    """
    # print display_as_name
    exclude_titles = ['mr', 'mrs', 'ms', 'miss', 'dr', 'sir', '']
    display_names = []
    for i in display_as_name.split(' '):
        if i not in exclude_titles:
            display_names.append(i)

    matched_people = []

    user = data
    # for user in data:
    if not user.has_key('title'):
        if user.has_key('name'):
            user['title'] = user['name']

    # get the title, split it
    title = user['title'].lower()
    title_splits = []
    for t in title.split(' '):
        title_splits.append(t.replace(',',''))

    # check if display names are in the title
    disp_match = True
    for disp in display_names:
        if disp.lower() in title_splits:
            pass
        else:
            disp_match = False

    if disp_match:
        # if the full display name is in the title, thats good enough
        matched_people.append(user)

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

def remove_duplicates(data):
    set_of_jsons = {json.dumps(d, sort_keys=True) for d in data}
    data = [json.loads(t) for t in set_of_jsons]

    b = []
    for i in data:
        self = i['links']['self']
        f = False
        for x in b:
            b_self = x['links']['self']
            if b_self == self:
                f = True
        if not f:
            b.append(i)

    return b

def remove_duplicates_companies(data):
    set_of_jsons = {json.dumps(d, sort_keys=True) for d in data}
    data = [json.loads(t) for t in set_of_jsons]

    b = []
    for i in data:
        # print '*'*100
        # pprint.pprint(i)
        # print ''
        self = i['links']['self']
        # print self
        # print i['title']
        f = False
        for x in b:
            b_self = x['links']['self']
            if b_self == self:
                f = True
        if not f:
            b.append(i)

    return b

def get_companies_house_companies(member):
    """Get data from companies house"""

    # this is the dob from the data.parliament query
    dob = None
    if member.has_key('DateOfBirth'):
        if type(member['DateOfBirth']) == str:
            dob = datetime.strptime(member['DateOfBirth'], '%Y-%m-%dT%H:%M:%S')

    # id
    member_id = member['@Member_Id']

    # names
    first_name = member['BasicDetails']['GivenForename'].lower()
    last_name = member['BasicDetails']['GivenSurname'].lower()
    display_as_name = member['DisplayAs'].lower()

    middle_name = ''
    if member['BasicDetails']['GivenMiddleNames']:
        middle_name = member['BasicDetails']['GivenMiddleNames'].lower()

    #############################################################################################################################
    # BASIC SEARCH
    limit_results = '100'
    url = 'https://api.companieshouse.gov.uk/search/companies?q=%s+%s&items_per_page=%s' % (first_name, last_name, limit_results)

    url = url.replace(' ', '+')
    r = get_request(url=url, user=companies_house_user, headers={})

    data_first_last = r.json()
    data_first_last = decoded(data_first_last)
    data_first_last = data_first_last['items']

    if middle_name != '':
        url = 'https://api.companieshouse.gov.uk/search/companies?q=%s+%s+%s&items_per_page=%s' % (first_name, middle_name, last_name, limit_results)

        url = url.replace(' ', '+')
        r = get_request(url=url, user=companies_house_user, headers={})

        data_middle = r.json()
        data_middle = decoded(data_middle)
        data_middle = data_middle['items']

        data_first_last += data_middle

    if display_as_name != '%s %s' % (first_name, last_name):

        url = 'https://api.companieshouse.gov.uk/search/companies?q=%s&items_per_page=%s' % (display_as_name, limit_results)

        url = url.replace(' ', '+')
        r = get_request(url=url, user=companies_house_user, headers={})

        data_display = r.json()
        data_display = decoded(data_display)
        data_display = data_display['items']

        data_first_last += data_display

    data = data_first_last
    #############################################################################################################################
    # WE HAVE COMPANIES FROM THE QUERIES, FILTER BY NAME AND KEYWORD
    # WE NEED TO MATCH EITHER - A FAIRLY LOOSE SEARCH

    matched_companies = []
    for record in data:

        record['match_results'] = {}
        record['match_results']['dob'] = None
        record['match_results']['names'] = {}
        record['match_results']['names']['display_name'] = None
        record['match_results']['names']['first_middle_last_name'] = None
        record['match_results']['names']['first_last_name'] = None
        record['match_results']['address'] = None
        record['match_results']['keyword'] = None

        # look for display name first
        if filter_by_name_string(record, display_as_name) != []:
            record['match_results']['names']['display_name'] = True
        else:
            record['match_results']['names']['display_name'] = False

        # look for first last name
        if filter_by_name_string(record, '%s %s' % (first_name, last_name)) != []:
            record['match_results']['names']['first_last_name'] = True
        else:
            record['match_results']['names']['first_last_name'] = False

        # look for first middle last name
        if filter_by_name_string(record, '%s %s %s' % (first_name, middle_name, last_name)) != []:
            record['match_results']['names']['first_middle_last_name'] = True
        else:
            record['match_results']['names']['first_middle_last_name'] = False

        # look for keyword
        to_search = []
        if record.has_key('title'):
            to_search.append(record['title'])

        if record.has_key('address'):
            if type(record['address']) == list:
                for each in record['address'].values():
                    to_search.append(each)

        if contains_mp(to_search):
            record['match_results']['keyword'] = True

        # now count up the match types
        count = 0

        # names
        if True in record['match_results']['names'].values():
            count += 1

        # keyword
        if record['match_results']['keyword'] == True:
            count += 1

        count_threshold = 1
        record['match_results']['count'] = count

        if count >= count_threshold:
            matched_companies.append(record)

    # clean up the records and filter out records with no appointments
    matched_companies = remove_duplicates_companies(matched_companies)

    #############################################################################################################################
    # NOW GET COMPANY, OFFICERS AND PERSONS
    matched_officers = []

    # now we have matched records that have passed the initial check (name and keywords). now we must get
    # the officers and persons and check to see if any of those are our MP. if th
    for record in matched_companies:

        record['company'] = getlink(record, 'self')
        record['company']['officers'] = getlink(record['company'], 'officers')['items']
        # record['company']['persons_with_significant_control'] = getlink(record['company'], 'persons_with_significant_control')['items']

        for officer in record['company']['officers']:

            officer['links']['appointments'] = officer['links']['officer']['appointments']

            if not officer.has_key('date_of_birth'):
                officer['date_of_birth'] = {'month' : None, 'year' : None}

            officer['match_results'] = {}
            officer['appointments'] = getlink(officer, 'appointments')['items']
            officer['match_results']['dob'] = None
            officer['match_results']['names'] = {}
            officer['match_results']['names']['display_name'] = False
            officer['match_results']['names']['first_middle_last_name'] = False
            officer['match_results']['names']['first_last_name'] = False
            officer['match_results']['address'] = False
            officer['match_results']['keyword'] = False

            # look for display name first
            if filter_by_name_string(officer, display_as_name) != []:
                officer['match_results']['names']['display_name'] = True

            # look for first last name
            if filter_by_name_string(officer, '%s %s' % (first_name, last_name)) != []:
                officer['match_results']['names']['first_last_name'] = True

            # look for first middle last name
            if filter_by_name_string(officer, '%s %s %s' % (first_name, middle_name, last_name)) != []:
                officer['match_results']['names']['first_middle_last_name'] = True

            # look for dob
            if dob != None:
                # if there is no dob in the companies house record, then None,
                # if there is dob but doesnt match, then False
                # if there is dob and matches, then True
                if filter_by_dob(officer, dob) != []:
                    officer['match_results']['dob'] = True
                else:
                    officer['match_results']['dob'] = False

            # look for keyword
            for app in officer['appointments']:
                to_search = []
                if app.has_key('occupation'):
                    to_search.append(app['occupation'])

                if app.has_key('address'):
                    for each in app['address'].values():
                        to_search.append(each)

                if contains_mp(to_search):
                    officer['match_results']['keyword'] = True

            # now count up the match types
            count = 0

            # names
            if True in officer['match_results']['names'].values():
                count += 1

            # dob
            if officer['match_results']['dob'] == True:
                count += 1
            elif officer['match_results']['dob'] == False:
                count -= 1

            # keyword
            if officer['match_results']['keyword'] == True:
                count += 1

            count_threshold = 2
            if display_as_name in ['michael gove']:
                # the prick has given an incorrect date of birth, which makes him harder to locate
                count_threshold = 1

            officer['match_results']['count'] = count

            if count >= count_threshold:
                for app in officer['appointments']:

                    app['company'] = getlink(app, 'company')
                    app['company']['persons_with_significant_control'] = check_controlling_persons(officer['date_of_birth'], getlink(app['company'], 'persons_with_significant_control')['items'])
                    # app['company']['officers'] = getlink(app['company'], 'officers')['items']
                    # app['company']['filing_history'] = getlink(app['company'], 'filing_history')['items']

                if officer not in matched_officers:
                    matched_officers.append(officer)

    return matched_officers


def get_companies_house_users(member):
    """Get data from companies house"""

    # this is the dob from the data.parliament query
    dob = None
    if member.has_key('DateOfBirth'):
        if type(member['DateOfBirth']) == str:
            dob = datetime.strptime(member['DateOfBirth'], '%Y-%m-%dT%H:%M:%S')

    # id
    member_id = member['@Member_Id']

    # names
    first_name = member['BasicDetails']['GivenForename'].lower()
    last_name = member['BasicDetails']['GivenSurname'].lower()
    display_as_name = member['DisplayAs'].lower()

    middle_name = ''
    if member['BasicDetails']['GivenMiddleNames']:
        middle_name = member['BasicDetails']['GivenMiddleNames'].lower()
 
    #############################################################################################################################
    # BASIC SEARCH
    limit_results = '10'
    url = 'https://api.companieshouse.gov.uk/search/officers?q=%s+%s&items_per_page=%s' % (first_name, last_name, limit_results)

    url = url.replace(' ', '+')
    r = get_request(url=url, user=companies_house_user, headers={})

    data_first_last = r.json()
    data_first_last = decoded(data_first_last)
    data_first_last = data_first_last['items']

    if middle_name != '':
        url = 'https://api.companieshouse.gov.uk/search/officers?q=%s+%s+%s&items_per_page=%s' % (first_name, middle_name, last_name, limit_results)

        url = url.replace(' ', '+')
        r = get_request(url=url, user=companies_house_user, headers={})

        data_middle = r.json()
        data_middle = decoded(data_middle)
        data_middle = data_middle['items']

        data_first_last += data_middle

    if display_as_name != '%s %s' % (first_name, last_name):

        url = 'https://api.companieshouse.gov.uk/search/officers?q=%s&items_per_page=%s' % (display_as_name, limit_results)

        url = url.replace(' ', '+')
        r = get_request(url=url, user=companies_house_user, headers={})

        data_display = r.json()
        data_display = decoded(data_display)
        data_display = data_display['items']

        data_first_last += data_display

    data = data_first_last

    #############################################################################################################################
    # NOW MATCH THE RECORDS TO THE MP

    matched = []
    for record in data:

        # get the appointments for the user
        appointments = getlink(record, 'self')['items']

        # setup the matches dictionary
        record['appointments'] = appointments
        record['match_results'] = {}
        record['match_results']['dob'] = None
        record['match_results']['names'] = {}
        record['match_results']['names']['display_name'] = False
        record['match_results']['names']['first_middle_last_name'] = False
        record['match_results']['names']['first_last_name'] = False
        record['match_results']['address'] = False
        record['match_results']['keyword'] = False

        # look for display name first
        if filter_by_name_string(record, display_as_name) != []:
            record['match_results']['names']['display_name'] = True

        # look for first last name
        if filter_by_name_string(record, '%s %s' % (first_name, last_name)) != []:
            record['match_results']['names']['first_last_name'] = True

        # look for first middle last name
        if filter_by_name_string(record, '%s %s %s' % (first_name, middle_name, last_name)) != []:
            record['match_results']['names']['first_middle_last_name'] = True

        # look for dob
        if dob != None:
            # if there is no dob in the companies house record, then None,
            # if there is dob but doesnt match, then False
            # if there is dob and matches, then True
            if filter_by_dob(record, dob) != []:
                record['match_results']['dob'] = True
            else:
                record['match_results']['dob'] = False

        # look for keyword
        for app in appointments:

            to_search = []
            if app.has_key('occupation'):
                to_search.append(app['occupation'])

            if app.has_key('address'):
                for each in app['address'].values():
                    to_search.append(each)

            if contains_mp(to_search):
                record['match_results']['keyword'] = True

        # now count up the match types
        count = 0

        # names
        if True in record['match_results']['names'].values():
            count += 1

        # dob
        if record['match_results']['dob'] == True:
            count += 1
        elif record['match_results']['dob'] == False:
            count -= 1

        # keyword
        if record['match_results']['keyword'] == True:
            count += 1

        count_threshold = 2
        record['match_results']['count'] = count

        if count >= count_threshold:
            matched.append(record)

    # clean up the records and filter out records with no appointments
    matched = remove_duplicates(matched)
    matched = filter_by_appointment_counts(matched)

    #############################################################################################################################
    # NOW GET PERSONS, OFFICERS, FILING HISTORY

    # now we have matched records that im confident of being the MP
    for record in matched:

        # iterate the appointments, find the officers, persons with significat control and filing history
        for app in record['appointments']:

            app['company'] = getlink(app, 'company')
            app['company']['persons_with_significant_control'] = check_controlling_persons(record['date_of_birth'], getlink(app['company'], 'persons_with_significant_control')['items'])
            # app['company']['officers'] = getlink(app['company'], 'officers')['items']
            # app['company']['filing_history'] = getlink(app['company'], 'filing_history')['items']

    return matched

def check_controlling_persons(dob, persons):

    controllers = []

    for person in persons:

        name =  person['name']
        kind = person['kind']
        control = person['natures_of_control']

        ownership = None

        for i in control:

            # for now all we care for is ownership, not voting rights etc
            if 'ownership' in i:
                ownership = i

                if kind == 'individual-person-with-significant-control':
                    # the entity of the controlling shareholder is a person, lets check to see
                    # if that person is the mp

                    controller = getlink(person, 'self')

                    if controller.has_key('date_of_birth'):
                        if controller['date_of_birth'] == dob:
                            controllers.append(person)

                elif kind == 'corporate-entity-person-with-significant-control':
                    # so, we should find these companies and check to see if our user has controlling shares in
                    # that company
                    pass

    return controllers

def write_wordcloud(member_id, name, words):
    """
    Write out word cloud
    """
    image_path = '../lib/data/wordclouds/%s.png' % member_id

    # words to generate a clod from
    string = ''
    for w in words:
        spl = w.split(' ')
        for i in spl:
            if i != '':
                i = i.replace('-', ' ').replace('/', ' ')
                string += '%s ' % i.lower()

    stopwords = ['an', 'it', 'to', 'as', 'incorporated', 'co', 'is', 'my', 'member', 'trading', 'companies', 'uk', 'and', 'none', 'from', 'of', 'for', 'in', 'on', 'true', 'false', 'england', 'scotland', 'wales', 'northern', 'ireland', 'officers', 'active', 'company', 'street', 'director', 'london', 'limited', 'corporate', 'secretary', 'dissolved', 'officer', 'united', 'kingdom', 'british', 'appointments', 'appointment', 'mr', 'mrs', 'ms', 'miss', 'the', 'ltd', 'limited', 'plc', 'llp']

    wordcloud = WordCloud(background_color=None, mode="RGBA", width=1000, height=160, max_words=50, stopwords=stopwords, colormap="binary_r").generate(string)
    import matplotlib.pyplot as plt
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    print 'Writing : %s' % name
    plt.savefig(image_path, transparent=True, bbox_inches='tight', pad_inches=0, dpi=200)
    plt.close()
