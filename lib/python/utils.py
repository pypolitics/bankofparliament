# -*- coding: utf-8 -*-

# system libs
import requests, time, ast, locale, pprint, re, shutil, os, sys, json, copy
reload(sys) 
sys.setdefaultencoding('utf8')

from datetime import datetime, date
import xml.etree.cElementTree as ElementTree
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from datetime import datetime
from wordcloud import WordCloud
import csv
import matplotlib.pyplot as plt
from plotting import plot_data_to_file

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
def make_node(node, name, hovertext, node_type, unique=True):
    """"""
    if unique:
        global node_id
        node_id += 1
        node['id'] = node_id

    node['name'] = name
    node['hovertext'] = hovertext
    node['node_type'] = node_type
    return node

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def write_scatter_plot(mp, network_file):
    """
    Write out scatter plot html
    """
    node_id = 0
    plot_path = '../pages/plots/%s.html' % mp['member_id']

    colors = {'light_blue' : 'rgb(72, 128, 219)',
            'light_orange' : 'rgb(247, 165, 93)',
            'light_green' : 'rgb(138, 216, 110)',
            'light_grey' : 'rgb(184, 186, 184)',
            'light_turq' : 'rrgb(129, 221, 232)',
            'light_yellow' : 'rgb(255, 245, 112)',
            'light_red' : 'rgb(229, 100, 94)',
            'light_purple' : 'rgb(228, 129, 232)',
            'light_pink' : 'rgb(255, 186, 244)',
            'dark_grey' : 'rgb(0, 0, 0)'
    }

    data_nodes = {  'mp'                : {'color' : colors['light_blue'], 'opacity' : 1, 'size' : 120},

                    'income_item'        : {'color' : colors['light_red'], 'opacity' : 0.5, 'size' : 40},
                    'income_cat'        : {'color' : colors['light_red'], 'opacity' : 1, 'size' : 40},
                    'income_main'        : {'color' : colors['light_red'], 'opacity' : 1, 'size' : 60},

                    'freebies_item'        : {'color' : colors['light_orange'], 'opacity' : 0.5, 'size' : 40},
                    'freebies_cat'        : {'color' : colors['light_orange'], 'opacity' : 1, 'size' : 40},
                    'freebies_main'        : {'color' : colors['light_orange'], 'opacity' : 1, 'size' : 60},

                    'wealth_item'        : {'color' : colors['light_pink'], 'opacity' : 0.5, 'size' : 40},
                    'wealth_cat'        : {'color' : colors['light_pink'], 'opacity' : 1, 'size' : 40},
                    'wealth_main'        : {'color' : colors['light_pink'], 'opacity' : 1, 'size' : 60},

                    'misc_item'        : {'color' : colors['light_green'], 'opacity' : 0.5, 'size' : 40},
                    'misc_cat'        : {'color' : colors['light_green'], 'opacity' : 1, 'size' : 40},
                    'misc_main'        : {'color' : colors['light_green'], 'opacity' : 1, 'size' : 60},

                    }

    data_lines = {  'major' : {'color' : colors['dark_grey'], 'opacity' : 1, 'size' : 8, 'name' : None},
                    'minor' : {'color' : colors['light_grey'], 'opacity' : 0.2, 'size' : 2, 'name' : None},
                    }

    # data
    data = {'nodes' : [], 'links' : []}

    # get main node
    splits = mp['name'].split(' ')
    first = splits[0]
    last = ' '.join(splits[1:])
    label = '<b>%s<br>%s' % (first, last)
    node_main = make_node(data_nodes['mp'], name=label, hovertext='%s' % mp['name'], node_type='mp')
    data['nodes'].append(node_main)

    categories = {  'property_income'       : {'node_type' : 'income'},
                    'salary'                : {'node_type' : 'income'},
                    'employment'            : {'node_type' : 'income'},

                    'gifts'                 : {'node_type' : 'freebies'},
                    'gifts_outside_uk'      : {'node_type' : 'freebies'},
                    'indirect_donations'    : {'node_type' : 'freebies'},
                    'direct_donations'      : {'node_type' : 'freebies'},
                    'visits_outside_uk'     : {'node_type' : 'freebies'},

                    'property_wealth'       : {'node_type' : 'wealth'},
                    'shareholdings'         : {'node_type' : 'wealth'},

                    'miscellaneous'         : {'node_type' : 'misc'},
                    'family'                : {'node_type' : 'misc'},
                    'family_lobbyists'      : {'node_type' : 'misc'},
    }


    n = []

    for each in mp['categories']:

        category_type = each['category_type']

        for i in each['items']:

            if 'property' in each['category_type']:
                if i['isWealth']:
                    category = '%s_wealth' % category_type
                else:
                    category = '%s_income' % category_type
            else:
                category = category_type

            # MAIN CATERGORY NODE
            label = '<b>%s' % categories[category]['node_type'].title() + ' Categories'
            label = '%s' % categories[category]['node_type'].title() + ' Categories'
            hovertext = label
            type_node = make_node(data_nodes[categories[category]['node_type'] + '_main'], name=label, hovertext=hovertext, node_type=categories[category]['node_type'] + '_main')
            type_copy = copy.copy(type_node)

            # find an existing node
            found = None
            for x in data['nodes']:
                for a in x.itervalues():
                    if label in str(a):
                        found = x
                        break

            if not found:
                # print '\nAdding main category : %s' % label
                type_copy['amount'] = 0
                data['nodes'].append(type_copy)
                link = make_link(data_lines['major'], nodes = data['nodes'], source=node_main, target=type_copy)
                l = copy.copy(link)
                data['links'].append(l)

                type_copy['items'] = []
                n.append(type_copy)
            else:
                type_copy = found

            # CATERGORY NODE
            label = '%s' % category.title()
            hovertext = '%s' % category.title()
            category_node = make_node(data_nodes[categories[category]['node_type'] + '_cat'], name=label, hovertext=hovertext, node_type=categories[category]['node_type'] + '_cat')
            cat_copy = copy.copy(category_node)

            # find an existing node
            found = None
            for x in data['nodes']:
                for a in x.itervalues():
                    if label in str(a):
                        # if not 'Basic Salary' in str(a):

                        found_cat_node_type = data['nodes'][data['nodes'].index(x)]['node_type']
                        looking_for = categories[category]['node_type'] + '_cat'
                        if found_cat_node_type == looking_for:
                            found = x
                            break

            if not found:
                # print '\tAdding category : %s' % label
                cat_copy['amount'] = 0
                data['nodes'].append(cat_copy)
                link = make_link(data_lines['major'], nodes = data['nodes'], source=type_copy, target=cat_copy)
                l = copy.copy(link)
                data['links'].append(l)

                cat_copy['items'] = []
                n[n.index(type_copy)]['items'].append(cat_copy)

            else:
                cat_copy = found

            # ITEM NODE
            if each['isCurrency']:
                item_label = u'\u00a3' + '%s' % "{:,}".format(i['amount'])
            else:
                if 'shareholding' in category:
                    item_label = '%s' % i['amount'] + r'%'
                else:
                    item_label = ''

            item_hovertext = '%s' % i['pretty']
            item_node = make_node(data_nodes[categories[category]['node_type'] + '_item'], name=item_label, hovertext=item_hovertext, node_type=categories[category]['node_type'] + '_item', unique=True)
            item_copy = copy.copy(item_node)

            # print 'Adding item: %s' % item_label
            item_copy['amount'] = i['amount']
            data['nodes'].append(item_copy)
            link = make_link(data_lines['major'], nodes = data['nodes'], source=cat_copy, target=item_copy)
            l = copy.copy(link)
            data['links'].append(l)

            t_idx = n.index(type_copy)
            c_idx = n[t_idx]['items'].index(cat_copy)
            n[t_idx]['items'][c_idx]['items'].append(item_copy)

    # find the ranges of the items, so we can adjust size of nodes, relative to all other nodes
    main_range = []
    for main_category in n:

        main_amount = 0
        category_range = []

        for cat in n[n.index(main_category)]['items']:

            cat_amount = 0

            t_idx = n.index(main_category)
            c_idx = n[t_idx]['items'].index(cat)

            item_range = []
            for item in n[t_idx]['items'][c_idx]['items']:
                if not 'wealth' in item['node_type']:
                    if item['amount']:
                        item_amount = item['amount']
                    else:
                        item_amount = 0
                    item_range.append(item_amount)
                    category_range.append(item_amount)
                    main_range.append(item_amount)
                    cat_amount += item_amount

            cat['category_amount'] = int(cat_amount)
            category_range.append(cat_amount)
            main_range.append(cat_amount)
            main_amount += cat_amount

        main_category['main_amount'] = int(main_amount)
        main_range.append(main_amount)

    # now we have ranges, make the size adjustments
    current_min = min(main_range)
    current_max = max(main_range)
    new_min = 10
    new_max = 250

    for main_category in n:

        for cat in n[n.index(main_category)]['items']:

            t_idx = n.index(main_category)
            c_idx = n[t_idx]['items'].index(cat)

            for item in n[t_idx]['items'][c_idx]['items']:
                if not 'wealth' in item['node_type']:
                    v = item['amount']
                    if not current_min == current_max:
                        if v:
                            size_value = int(translate(v, current_min, current_max, new_min, new_max))
                            # print '%s > %s' % (v, size_value)
                            item['size'] += size_value

    title = '%s, %s, %s' % (mp['name'], mp['party'], mp['constituency'])
    plot_data_to_file(data, network_file, mp['name'], div=True)
    # print 'Writing : %s' % network_file
