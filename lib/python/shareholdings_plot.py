# -*- coding: utf-8 -*-
import copy, re
import textwrap
from fuzzywuzzy import fuzz

from constants import PARTY_COLOURS
from plotting import plot_data_to_file
from plot_utils import make_node, make_link, translate, clean_name

def write_shareholder_plot(mp, plot_file):
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

    data_nodes = {  'mp'                : {'color' : 'black', 'opacity' : 1, 'size' : 60},

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

                    'person_item'        : {'color' : yellow_darker, 'opacity' : 0.5, 'size' : 25},
                    'officer_item'        : {'color' : 'white', 'opacity' : 0.5, 'size' : 15},

                    'declared_company'              : {'color' : green_darker, 'opacity' : 1, 'size' : 30},
                    'undeclared_company'            : {'color' : orange_darker, 'opacity' : 1, 'size' : 30},
                    'undeclared_active_company'     : {'color' : 'red', 'opacity' : 1, 'size' : 30},
                    'undeclared_inactive_company'   : {'color' : grey_darker, 'opacity' : 0.5, 'size' : 30},

                    'active_person'           : {'color' : yellow_darker, 'opacity' : 0.5, 'size' : 20},
                    'inactive_person'           : {'color' : grey_darker, 'opacity' : 0.5, 'size' : 20},
                    'active_officer'           : {'color' : 'white', 'opacity' : 0.5, 'size' : 10},
                    'inactive_officer'           : {'color' : grey_darker, 'opacity' : 0.5, 'size' : 10},


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
    label = ''

    node_main = make_node(data_nodes['mp'], name=label, hovertext='%s' % mp['name'], node_type='mp')
    # node_main['color'] = PARTY_COLOURS[mp['party'].lower()]
    data['nodes'].append(node_main)

    for category in mp['categories']:

        if 'shareholding' in category['category_type'] or 'companies' in category['category_type']:

            for item in category['items']:
                url = item['link']

                # textwrap the hovertext
                pretty = item['pretty']
                wrapped = textwrap.wrap(pretty, 50)

                hovertext = ''
                hovertext += '</br>'
                if item['company'].has_key('company_name'):
                    hovertext += '</br><b>Company Name:</b> %s' % item['company']['company_name'].title()
                if item['company'].has_key('company_number'):
                    hovertext += '</br><b>Company Number:</b> %s' % item['company']['company_number']
                if item['company'].has_key('company_status'):
                    hovertext += '</br><b>Company Status:</b> %s' % item['company']['company_status'].title()

                # hovertext += '</br></br><b>Register of Interests Raw Entry:</b>'
                # hovertext += '</br>' + '</br>'.join(wrapped)
                # hovertext += '</br>'

                # if url:
                #     hovertext += '</br>Click node to visit Companies House record.'

                if not 'companies' in category['category_type']:
                    # this is given by the register of interests
                    n = 'declared_company'
                else:

                    if item['company']['company_status'] == 'active':
                        n = 'undeclared_active_company'
                    else:
                        n = 'undeclared_inactive_company'

                item_node = make_node(data_nodes[n], name='', hovertext=hovertext, node_type=category, hyperlink=url)
                item_copy = copy.copy(item_node)
                item_copy['amount'] = item['amount']

                # hyperlinked node - add a border
                if url != 'https://beta.companieshouse.gov.uk':
                    item_copy['border_style'] = {'color' : 'gray', 'size' : 2}

                found = False
                for each in data['nodes']:
                    if hovertext == each['hovertext']:
                        item_copy = each
                        found = True

                if not found:
                    data['nodes'].append(item_copy)

                link = make_link(data_lines['income_line'], nodes = data['nodes'], source=node_main, target=item_copy)
                l = copy.copy(link)
                data['links'].append(l)

                ################################################################################################################
                # COMPANIES HOUSE STUFF ONLY
                # significant persons
                if item.has_key('persons'):

                    for person in item['persons']:

                        name = clean_name(person['name'])
                        hovertext = '%s' % name.title()
                        label = name.title()

                        if url:
                            url = item['link'] + '/persons-with-significant-control/'

                        if person.has_key('ceased_on'):
                            n = 'inactive_person'
                        else:
                            n = 'active_person'

                        person_node = make_node(data_nodes[n], name=label, hovertext=hovertext, node_type=category, hyperlink=url)
                        person_copy = copy.copy(person_node)

                        # fuzzy logic a cleaned name for match with mp
                        # set our threshold at 90%
                        ratio = fuzz.token_set_ratio(name, mp['name'])

                        if ratio < 90:
                            # only if the person is not our mp

                            # lets check they dont already exist
                            found = person_copy
                            for each in data['nodes']:
                                if fuzz.token_set_ratio(label, each['name']) >= 90:
                                    found = each

                            if found == person_copy:
                                data['nodes'].append(found)
                            
                            link = make_link(data_lines['wealth_line'], nodes = data['nodes'], source=item_copy, target=found)
                            l = copy.copy(link)
                            data['links'].append(l)

                if item.has_key('officers'):

                    for person in item['officers']:

                        if person.has_key('resigned_on'):
                            n = 'inactive_officer'
                        else:
                            n = 'active_officer'

                        name = clean_name(person['name'])
                        hovertext = '%s' % name.title()
                        label = ''

                        if url:
                            url = item['link'] + '/persons-with-significant-control/'

                        person_node = make_node(data_nodes[n], name=label, hovertext=hovertext, node_type=category, hyperlink=url)
                        person_copy = copy.copy(person_node)

                        # fuzzy logic a cleaned name for match with mp
                        # set our threshold at 90%
                        ratio = fuzz.token_set_ratio(name, mp['name'])

                        if ratio < 90:
                            # only if the person is not our mp

                            # lets check they dont already exist
                            found = person_copy
                            for each in data['nodes']:
                                if each['node_type'] != 'mp':
                                    if fuzz.token_set_ratio(hovertext, each['hovertext']) >= 90:
                                        found = each

                            if found == person_copy:
                                data['nodes'].append(found)
                            
                            link = make_link(data_lines['wealth_line'], nodes = data['nodes'], source=item_copy, target=found)
                            l = copy.copy(link)
                            data['links'].append(l)

    return plot_data_to_file(data, plot_file, mp['member_id'], mp['dods_id'], mp['name'], mp['constituency'], mp['party'], hyperlink)
    # print 'Writing : %s' % plot_file
