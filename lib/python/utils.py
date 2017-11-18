# -*- coding: utf-8 -*-

# system libs
import requests, time, ast, locale, pprint, re, shutil, os, sys, json, copy
reload(sys) 
sys.setdefaultencoding('utf8')

from datetime import datetime, date
import xml.etree.cElementTree as ElementTree
# from fuzzywuzzy import fuzz
# from fuzzywuzzy import process
from datetime import datetime
import textwrap
# from wordcloud import WordCloud
import csv
# import matplotlib.pyplot as plt
from plotting import plot_data_to_file
from constants import party_colours

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

def get_request(url, user=None, headers={}, request_wait_time=300.00):
    # print url
    if user:
        request = requests.get(url, auth=(user, ''), headers=headers)
    else:
        request = requests.get(url, headers=headers)
    # print request
    if request.status_code == 200:
        return request

    # too many requests
    if request.status_code == 429:
        print '*'*100
        print "Too Many Requests, wait for %s seconds" % str(request_wait_time)
        print '*'*100
        time.sleep(request_wait_time)
        return get_request(url, user, headers)
    
    # temporarily unavailable
    elif request.status_code == 503:
        print '*'*100
        print "Temporarily Unavailable, wait for %s seconds" % str(request_wait_time)
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

def get_house_of_commons_member(constituency, outputs=None):

    search_criteria = 'House=Commons|IsEligible=true|constituency=%s' % (constituency)
    if not outputs:
        outputs = 'BasicDetails|Addresses|PreferredNames'
    url = 'http://data.parliament.uk/membersdataplatform/services/mnis/members/query/%s/%s' % (search_criteria, outputs)

    headers = {'Accept': 'application/json'}
    request = get_request(url=url, user=None, headers=headers)

    # replace null with None
    content = request.content.replace("null", "None")
    a = ast.literal_eval(content)

    members = a['Members']['Member']
    return members

def get_house_of_commons_member2(constituency):

    search_criteria = 'House=Commons|IsEligible=true|constituency=%s' % (constituency)
    outputs = 'GovernmentPosts|BiographyEntries|Committees'

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

def contains_keywords(vals, keywords):
    """
    Check if a list of values contain our keywords
    """

    for search in keywords:
        for v in vals:
            if search.lower() in v.lower():
                # print 'MP FOUND : %s' % vals
                return True
    return False

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

def read_sic_codes(sic):

    path = '../lib/data/sic_codes.csv'
    if os.path.isfile(path):
        pass
    else:
        path = '../data/sic_codes.csv'

    in_file = open(path, "rb")
    reader = csv.reader(in_file)
    next(reader, None)

    for row in reader:
        if sic == row[0]:
            return row[-1]
    return ''

def cleanup_raw_string(raw):
    """Cleanup a raw string from the register of intrests, ready for querying with"""

    raw = raw.lower()
    raw_list = re.sub('[^0-9a-zA-Z]+', ' ', raw).split(' ')

    exclude = ['shareholder', 'director', 'of', 'services', 'service', 'recruitment', 'international', 'specialist','and', '(', ')', '%', 'registered', '', 'from', 'an', 'a', 'company', 'shareholding', 'shareholdings', 'business']

    months = [date(2000, m, 1).strftime('%b').lower() for m in range(1, 13)]
    months_short = [date(2000, m, 1).strftime('%B').lower() for m in range(1, 13)]
    for i in months:
        exclude.append(i)
    for i in months_short:
        exclude.append(i)

    found = []
    for r in raw_list:
        if r not in exclude:
            try:
                r = int(r)
            except:
                found.append(r)

    return ' '.join(found)

def read_json_file():
    """
    Read file from json_dump_location
    """
    json_dump_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'members')
    data = []
    for mp in os.listdir(json_dump_location):
        f = os.path.join(json_dump_location, mp)
        with open(f) as json_data:
            data.append(json.load(json_data))

    return data

def write_word_cloud(words, member_id, filepath, width=1600, height=1000, background_color='#cccccc', max_words=300):
    """
    Write out word cloud
    """
    # words to generate a clod from
    string = ''
    for w in words:
        spl = w.split(' ')
        for i in spl:
            if i != '':
                i = i.replace('-', ' ').replace('/', ' ')
                string += '%s ' % i.lower()

    stopwords = ['other', 'member', 'trading', 'companies', 'uk', 'and', 'none', 'from', 'of', 'for', 'in', 'on', 'true', 'false', 'england', 'scotland', 'wales', 'northern', 'ireland', 'officers', 'active', 'company', 'street', 'director', 'london', 'limited', 'corporate', 'secretary', 'dissolved', 'officer', 'united', 'kingdom', 'british', 'appointments', 'appointment', 'mr', 'mrs', 'ms', 'miss', 'the', 'ltd', 'limited', 'plc', 'llp']

    wordcloud = WordCloud(background_color=background_color, mode="RGBA", width=width, height=height, max_words=max_words, stopwords=stopwords, colormap="Set1").generate(string)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    print 'Writing : %s' % filepath
    plt.savefig(filepath, transparent=True, bbox_inches='tight', pad_inches=0, dpi=300)

def make_link(link, nodes, source, target):
    """"""

    link['source'] = nodes.index(source)
    link['target'] = nodes.index(target)
    return link

node_id = 0
def make_node(node, name, hovertext, node_type, hyperlink=None, unique=True):
    """"""
    if unique:
        global node_id
        node_id += 1
        node['id'] = node_id

    node['name'] = name
    node['hovertext'] = hovertext
    node['node_type'] = node_type
    node['hyperlink'] = hyperlink
    node['border_style'] = {'color' : 'rgb(50,50,50)', 'size' : 0.5}
    return node

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def write_scatter_plot(mp, plot_file):
    """"""
    node_id = 0
    plot_path = '../pages/plots/%s.html' % mp['member_id']

    orange_darker = '#f7a55d'
    orange_lighter = '#fac99e'

    yellow_darker = '#fff570'
    yellow_lighter = '#fff899'

    pink_darker = '#ffbaf4'
    pink_lighter = 'rgb(255, 235, 251)'

    grey_darker = '#b8bab8'
    grey_lighter = '#d8dad8'

    green_darker = '#00ff99'
    green_lighter = '#4dffb8'

    data_lines = {  'major' : {'color' : grey_darker, 'opacity' : 1, 'size' : 8, 'name' : None},
                    'minor' : {'color' : grey_darker, 'opacity' : 0.2, 'size' : 2, 'name' : None},

                    'income_line' : {'color' : orange_darker, 'opacity' : 0.4, 'size' : 8, 'name' : None},
                    'wealth_line' : {'color' : grey_darker, 'opacity' : 0.4, 'size' : 8, 'name' : None},
                    'freebies_line' : {'color' : yellow_darker, 'opacity' : 0.4, 'size' : 8, 'name' : None},
                    'miscellaneous_line' : {'color' : pink_darker, 'opacity' : 0.4, 'size' : 8, 'name' : None},
                    'expenses_line' : {'color' : green_darker, 'opacity' : 0.4, 'size' : 8, 'name' : None},

                    }

    data_nodes = {  'mp'                : {'color' : grey_lighter, 'opacity' : 1, 'size' : 128},

                    'income_item'        : {'color' : orange_lighter, 'opacity' : 0.9, 'size' : 30},
                    'income_sub'        : {'color' : orange_darker, 'opacity' : 1, 'size' : 40},
                    'income_cat'        : {'color' : orange_darker, 'opacity' : 1, 'size' : 60},

                    'freebies_item'        : {'color' : yellow_lighter, 'opacity' : 0.9, 'size' : 30},
                    'freebies_sub'        : {'color' : yellow_darker, 'opacity' : 1, 'size' : 40},
                    'freebies_cat'        : {'color' : yellow_darker, 'opacity' : 1, 'size' : 60},

                    'wealth_item'        : {'color' : grey_lighter, 'opacity' : 0.9, 'size' : 30},
                    'wealth_sub'        : {'color' : grey_darker, 'opacity' : 1, 'size' : 40},
                    'wealth_cat'        : {'color' : grey_darker, 'opacity' : 1, 'size' : 60},

                    'miscellaneous_item'        : {'color' : pink_lighter, 'opacity' : 0.9, 'size' : 30},
                    'miscellaneous_sub'        : {'color' : pink_darker, 'opacity' : 1, 'size' : 40},
                    'miscellaneous_cat'        : {'color' : pink_darker, 'opacity' : 1, 'size' : 60},

                    'expenses_item'        : {'color' : green_lighter, 'opacity' : 0.9, 'size' : 30},
                    'expenses_sub'        : {'color' : green_darker, 'opacity' : 1, 'size' : 40},
                    'expenses_cat'        : {'color' : green_darker, 'opacity' : 1, 'size' : 60},

                    }

    # data
    data = {'nodes' : [], 'links' : []}

    person_id = mp['person_id']
    hyperlink = 'https://www.theyworkforyou.com/mp/%s#register' % person_id

    # get main node
    splits = mp['name'].split(' ')
    first = splits[0]
    last = ' '.join(splits[1:])
    label = '<b>%s<br>%s' % (first, last)

    node_main = make_node(data_nodes['mp'], name=label, hovertext='%s' % mp['name'], node_type='mp')
    node_main['color'] = party_colours[mp['party'].lower()]
    data['nodes'].append(node_main)

    categories = {'income' : [], 'freebies' : [], 'wealth' : [], 'miscellaneous' : [], 'expenses' : []}
    for each in mp['categories']:
        category_type = each['category_type']

        if category_type in ['salary', 'employment']:
            categories['income'].append(each)
        elif category_type in ['family', 'family_lobbyists', 'miscellaneous']:
            categories['miscellaneous'].append(each)
        elif category_type in ['shareholdings']:
            categories['wealth'].append(each)
        elif category_type in ['gifts', 'gifts_outside_uk', 'indirect_donations', 'direct_donations', 'visits_outside_uk']:
            categories['freebies'].append(each)

        if category_type == 'property':
            incomes = copy.copy(each)
            wealths = copy.copy(each)
            incomes['items'] = []
            incomes['category_description'] = 'Rental Income'
            wealths['items'] = []
            wealths['category_description'] = 'Property'

            for item in each['items']:

                if item['isIncome']:
                    incomes['items'].append(item)
                else:
                    wealths['items'].append(item)

            categories['income'].append(incomes)
            categories['wealth'].append(wealths)

    # now expenses
    categories['expenses'] = mp['expenses']

    main_range = []
    for c in categories.keys():
        if not c == 'wealth':
            for s in categories[c]:
                for i in s['items']:
                    if i['amount']:
                        main_range.append(int(i['amount']))

    current_min = min(main_range)
    current_max = max(main_range)
    new_min = 0

    for category in categories.keys():

        if category == 'wealth':
            new_max = 40
        else:
            new_max = 100

        # total category amount
        amount = 0
        for s in categories[category]:
            for i in s['items']:
                if i['amount']:
                    amount += i['amount']

        amount = "{:,}".format(amount)
        hovertext = '<b>%s</b></br></br>£%s' % (category.title(), str(amount))
        label = '<b>%s</b>' % category.title()
        cat_node = make_node(data_nodes['%s_cat' % category], name=label, hovertext=hovertext, node_type=category)
        cat_copy = copy.copy(cat_node)
        cat_copy['amount'] = 0
        data['nodes'].append(cat_copy)

        link = make_link(data_lines['%s_line' % category], nodes = data['nodes'], source=node_main, target=cat_copy)
        l = copy.copy(link)
        data['links'].append(l)

        for sub in categories[category]:

            # sub category total amount
            amount = 0
            for i in sub['items']:
                if i['amount']:
                    amount += i['amount']
            amount = "{:,}".format(amount)

            spl = sub['category_description'].split(' ')
            s = ''
            for i in spl:
                s += '%s<br>' % i

            if not category == 'expenses':
                hovertext = '<b>%s</b>£%s' % (s, amount)
            else:
                hovertext = '<b>%s</br></br></b>£%s' % (sub['category_description'], amount)

            label = '%s' % sub['category_description']
            sub_node = make_node(data_nodes['%s_sub' % category], name=label, hovertext=hovertext, node_type=category)
            sub_copy = copy.copy(sub_node)
            sub_copy['amount'] = 0
            data['nodes'].append(sub_copy)

            link = make_link(data_lines['%s_line' % category], nodes = data['nodes'], source=cat_copy, target=sub_copy)
            l = copy.copy(link)
            data['links'].append(l)

            for item in sub['items']:

                if sub['isCurrency']:
                    label = "£" + "{:,}".format(item['amount'])
                else:
                    label = ''

                if 'shareholding' in sub['category_description'].lower():
                    url = item['link']
                else:
                    url = None

                # textwrap the hovertext
                pretty = item['pretty']
                wrapped = textwrap.wrap(pretty, 50)

                hovertext = '</br>' + '</br>'.join(wrapped)
                item_node = make_node(data_nodes['%s_item' % category], name=label, hovertext=hovertext, node_type=category, hyperlink=url)
                item_copy = copy.copy(item_node)
                item_copy['amount'] = item['amount']

                # scale the marker
                if len(sub['items']) > 0:
                    if not current_min == current_max:
                        if item['amount']:
                            size_value = int(translate(int(item['amount']), current_min, current_max, new_min, new_max))
                            item_copy['size'] += size_value

                # hyperlinked node - add a border
                if url:
                    item_copy['border_style'] = {'color' : '#99ff99', 'size' : 2}

                data['nodes'].append(item_copy)

                link = make_link(data_lines['%s_line' % category], nodes = data['nodes'], source=sub_copy, target=item_copy)
                l = copy.copy(link)
                data['links'].append(l)

    title = '%s, %s, %s' % (mp['name'], mp['party'], mp['constituency'])
    return plot_data_to_file(data, plot_file, mp['member_id'], mp['dods_id'], mp['name'], mp['constituency'], mp['party'], hyperlink, div=True)
    # print 'Writing : %s' % plot_file

def camel_case_split(identifier):
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$|(?<=[0-9])(?=[A-Z]))', identifier)
    return [m.group(0) for m in matches]

def read_expenses(expenses_data):
    """
    read expenses csv file, organise into ready made plot categories
    """

    expenses_dictionary = {}
    office = ['Office spend', 'Staffing spend', 'Startup spend', 'Windup spend']
    other = ['Accommodation spend', 'Travel/subs spend', 'Other spend']
    total = []

    keys = office + other + total

    for year in expenses_data.keys():
        expenses_dictionary[year] = []
        with open(expenses_data[year], 'rb') as f:

            # replace null
            reader = csv.reader(x.replace('\0', '').replace('\xef\xbb\xbf', '').replace(' CC', '').replace(' BC', '') for x in f)
            headers = reader.next()

            for row in reader:
                if row != []:
                    data = {'office' : {'items' : []}, 'other' : {'items' : []}}

                    data = {}
                    data['category_amount'] = 0
                    data['category_description'] = '%s' % year.replace('-', ' - ')
                    data['isCurrency'] = True
                    data['items'] = []
                    data['name'] = row[headers.index('MP name')].replace(u'\xa3', '').replace(',','')
                    data['constituency'] = row[headers.index('Constituency')].replace(' CC', '').replace(' BC', '')

                    for head in headers:
                        if head in keys:
                            i = head.decode('utf-8')
                            cell = row[headers.index(head)]
                            cell_amount = cell.replace(u'\xa3', '').replace(',','')
                            try:
                                amount = int(float(cell_amount))
                            except:
                                amount = amount

                            item = {}
                            item['amount'] = amount
                            item['pretty'] = head

                            data['items'].append(item)

                    expenses_dictionary[year].append(data)
            f.close()

    return expenses_dictionary

def match_expenses(mp, year, expenses_dictionary):
    """
    Match a year and an mp to its expenses record
    """
    for ex in expenses_dictionary[year]:
        if mp['name'] == ex['name']:
            return [ex]
        elif mp['constituency'] == ex['constituency']:
            return [ex]

    print 'Unmatched : ', mp['name']
    return {'items' : [], 'category_amount' : 0, 'category_description' : year, 'isCurrency' : True, 'name' : mp['name']}
