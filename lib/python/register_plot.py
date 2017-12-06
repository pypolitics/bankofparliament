# -*- coding: utf-8 -*-
import copy, re
import textwrap
from fuzzywuzzy import fuzz

from constants import PARTY_COLOURS
from plotting import plot_data_to_file
from plot_utils import make_node, make_link, translate, clean_name

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
    grey_lighter_white = '#e5e6e5'

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

    data_nodes = {  'mp'                : {'color' : grey_lighter, 'opacity' : 1, 'size' : 120},

                    'income_item'        : {'color' : orange_lighter, 'opacity' : 0.8, 'size' : 30},
                    'income_sub'        : {'color' : orange_darker, 'opacity' : 1, 'size' : 40},
                    'income_cat'        : {'color' : orange_darker, 'opacity' : 1, 'size' : 60},

                    'freebies_item'        : {'color' : yellow_lighter, 'opacity' : 0.8, 'size' : 30},
                    'freebies_sub'        : {'color' : yellow_darker, 'opacity' : 1, 'size' : 40},
                    'freebies_cat'        : {'color' : yellow_darker, 'opacity' : 1, 'size' : 60},

                    'wealth_item'        : {'color' : grey_lighter, 'opacity' : 0.8, 'size' : 30},
                    'wealth_sub'        : {'color' : grey_darker, 'opacity' : 1, 'size' : 40},
                    'wealth_cat'        : {'color' : grey_darker, 'opacity' : 1, 'size' : 60},

                    'miscellaneous_item'        : {'color' : pink_lighter, 'opacity' : 0.8, 'size' : 30},
                    'miscellaneous_sub'        : {'color' : pink_darker, 'opacity' : 1, 'size' : 40},
                    'miscellaneous_cat'        : {'color' : pink_darker, 'opacity' : 1, 'size' : 60},

                    'expenses_item'        : {'color' : green_lighter, 'opacity' : 0.8, 'size' : 30},
                    'expenses_sub'        : {'color' : green_darker, 'opacity' : 1, 'size' : 40},
                    'expenses_cat'        : {'color' : green_darker, 'opacity' : 1, 'size' : 60},

                    'person_item'        : {'color' : grey_lighter_white, 'opacity' : 0.5, 'size' : 15},
                    'officer_item'        : {'color' : 'white', 'opacity' : 0.5, 'size' : 10},

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

    # url = '%s' % mp['member_id']
    url = None
    node_main = make_node(data_nodes['mp'], name=label, hovertext='%s' % mp['name'], node_type='mp', hyperlink=url)
    node_main['color'] = PARTY_COLOURS[mp['party'].lower()]
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

            if not s['category_description'] == 'Shareholdings':
                for i in s['items']:
                    if i['amount']:
                        amount += i['amount']

        amount = "{:,}".format(amount)

        hovertext = '<b>%s</b></br></br>£%s' % (category.title(), str(amount))
        if category in ['wealth', 'income']:
            hovertext = '<b>%s</b></br></br>£%s (Min)' % (category.title(), str(amount))
        else:
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
                if sub['category_description'] in ['Other Shareholdings', 'Property', 'Rental Income']:
                    hovertext = '<b>%s</b>£%s (Min)' % (s, amount)

                elif sub['category_description'] == 'Shareholdings':
                    hovertext = '<b>Shareholdings</b>'
                else:
                    hovertext = '<b>%s</b>£%s' % (s, amount)
            else:
                hovertext = '<b>%s</br></br></b>£%s' % (sub['category_description'], amount)

            url = None
            if 'shareholdings' in sub['category_description'].lower():
                url = '%s' % mp['member_id']
                label = '<a href="%s">%s</a>' % (str(mp['member_id']), sub['category_description'])
            else:
                label = '%s' % sub['category_description']

            sub_node = make_node(data_nodes['%s_sub' % category], name=label, hovertext=hovertext, node_type=category, hyperlink=url)
            sub_copy = copy.copy(sub_node)
            sub_copy['amount'] = 0
            data['nodes'].append(sub_copy)

            link = make_link(data_lines['%s_line' % category], nodes = data['nodes'], source=cat_copy, target=sub_copy)
            l = copy.copy(link)
            data['links'].append(l)

            for item in sub['items']:

                if 'shareholding' in sub['category_description'].lower():
                    if item['link'] != '':
                        url = item['link']
                    else:
                        url = None
                else:
                    url = None

                if sub['isCurrency']:

                    # the item is a currency, see if it requires a '(Min)' suffix too
                    label = "£" + "{:,}".format(item['amount'])
                    if sub['category_description'] in ['Property', 'Rental Income']:
                        label += '+'
                    elif sub['category_description'] in ['Other Shareholdings']:
                        if url == None:
                            label = '%sk+' % str(item['amount'])[:2]
                        else:
                            label = '<a href="%s">%sk+</a>' % (url, str(item['amount'])[:2])


                # its not currency
                elif sub['category_description'] == 'Shareholdings':
                    label = '%s' % item['amount'] + r'%'
                    if url == None:
                        label += '+'
                    else:
                        label = '<a href="%s">%s+</a>' % (url, label)
                else:
                    label = ''

                # textwrap the hovertext
                pretty = item['pretty']
                wrapped = textwrap.wrap(pretty, 50)
                hovertext = '</br>' + '</br>'.join(wrapped)

                if 'shareholding' in sub['category_description'].lower():
                    hovertext = ''

                    hovertext += '</br>'
                    if item['company'].has_key('company_name'):
                        hovertext += '</br><b>Company Name:</b> %s' % item['company']['company_name'].title()
                    if item['company'].has_key('company_number'):
                        hovertext += '</br><b>Company Number:</b> %s' % item['company']['company_number']
                    if item['company'].has_key('company_status'):
                        hovertext += '</br><b>Company Status:</b> %s' % item['company']['company_status'].title()

                    hovertext += '</br></br><b>Register of Interests Raw Entry:</b>'
                    hovertext += '</br>' + '</br>'.join(wrapped)
                    hovertext += '</br>'

                    if url:
                        hovertext += '</br>Click node to visit Companies House record.'

                item_node = make_node(data_nodes['%s_item' % category], name=label, hovertext=hovertext, node_type=category, hyperlink=url)
                item_copy = copy.copy(item_node)
                item_copy['amount'] = item['amount']

                # scale the marker
                if not sub['category_description'] in ['Shareholdings']:

                    if len(sub['items']) > 0:
                        if not current_min == current_max:
                            if item['amount']:
                                size_value = int(translate(int(item['amount']), current_min, current_max, new_min, new_max))
                                # if 'expenses' in category:
                                #     size_value = size_value / 2
                                item_copy['size'] += size_value

                data['nodes'].append(item_copy)

                link = make_link(data_lines['%s_line' % category], nodes = data['nodes'], source=sub_copy, target=item_copy)
                l = copy.copy(link)
                data['links'].append(l)

                ################################################################################################################
                # COMPANIES HOUSE STUFF ONLY
                # significant persons
                if item.has_key('persons'):

                    for person in item['persons']:
                        label = ''

                        name = clean_name(person['name'])
                        hovertext = '%s' % name.title()
                        if url:
                            url = item['link'] + '/persons-with-significant-control/'

                        person_node = make_node(data_nodes['person_item'], name=label, hovertext=hovertext, node_type=category, hyperlink=url)
                        person_copy = copy.copy(person_node)

                        # fuzzy logic a cleaned name for match with mp
                        # set our threshold at 90%
                        ratio = fuzz.token_set_ratio(name, mp['name'])

                        if ratio >= 90:

                            person_copy['color'] = PARTY_COLOURS[mp['party'].lower()]

                            # update the upstrem node with new percentage if higher than current value
                            for control in person['natures_of_control']:
                                if 'ownership' in control:
                                    # find the first digits, always the minimum
                                    minimum = re.search('[\d]+', control).group()

                                    # if the minimum is bigger than the current percentage value, update it
                                    if int(minimum) > item['amount']:

                                        min_label = '%s' % str(minimum) + r'%'
                                        if url == None:
                                            min_label += '+'
                                        else:
                                            min_label = '<a href="%s">%s+</a>' % (url, min_label)

                                        data['nodes'][data['nodes'].index(item_copy)]['name'] = min_label

    title = '%s, %s, %s' % (mp['name'], mp['party'], mp['constituency'])
    return plot_data_to_file(data, plot_file, mp['member_id'], mp['dods_id'], mp['name'], mp['constituency'], mp['party'], hyperlink)
    # print 'Writing : %s' % plot_file