#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os, sys
import operator
import locale
import pprint
from optparse import OptionParser

sys.path.append('../lib/python')

from utils import get_companies_house_person, get_request, filter_by_first_last_name, filter_by_appointment_counts, get_appointments
import shutil

locale.setlocale(locale.LC_ALL, '')

json_dump_location = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..', 'lib', 'data', 'members_dump.json')

lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lib')

images_directory = os.path.join(os.path.dirname(__file__), '..', 'images')
companies_house_user = 'ZCCtuxpY7uvkDyxLUz37dCYFIgke9PKfhMlEGC-Q'

tops_html = os.path.join(os.path.dirname(__file__), '../lib/html/tops.html')
mp_top_html = os.path.join(os.path.dirname(__file__), '../lib/html/mp_top.html')

html_file = os.path.join(os.path.dirname(__file__), '../index.html')
tails_html = os.path.join(os.path.dirname(__file__), '../lib/html/tails.html')
mp_tails_html = os.path.join(os.path.dirname(__file__), '../lib/html/mp_tails.html')


def main(mps, options):
    """
    Main
    """
    mps = sort_by_options(mps, options)

    print_to_html_file(mps)


def print_to_html_file(mps):
    start_html_file()
    for mp in mps:
        mp_html_file = os.path.join(os.path.dirname(__file__), '../pages/%s.html' % mp['member_id'])
        
        start_html_file(tops_html=mp_top_html, html_file=mp_html_file)

        print_mp_panel_into_file(mp, mp_html_file)

        end_html_file(tails_html=mp_tails_html, html_file=mp_html_file)

    end_html_file()

    for i in parties:
        print i

parties = []

def start_html_file(tops_html=tops_html, html_file=html_file):
    shutil.copy2(tops_html, html_file)


def end_html_file(tails_html=tails_html, html_file=html_file):
    with open(html_file, "a") as fo:
        with open(tails_html, 'r') as fi:
            fo.write(fi.read())

def format_integer(number):

    loc = locale.currency(number, grouping=True).split('.')[0]
    return loc.replace("£", "&#163;")

def print_mp_panel_into_file(member, mp_html_file):

    cat_types = [each['category_type'] for each in member['categories']]
    # print cat_types

    [u'employment', u'indirect_donations', u'direct_donations', u'gifts', u'visits_outside_uk', u'gifts_outside_uk', u'property', u'shareholdings', u'shareholdings', u'miscellaneous', u'family', u'family_lobbyists', u'salary']
    import pprint
    # pprint.pprint(member)

    # incomes
    private_income = 0
    rental_income = 0
    salary = 0

    # freebies
    gifts = 0
    gifts_outside_uk = 0
    visits_outside_uk = 0
    direct_donations = 0
    indirect_donations = 0

    # expenses
    expenses = 0

    family = False
    family_pretty = ''

    # wealth
    property_wealth = 0
    shareholdings = 0
    shareholdings_percent = 0

    shareholdings_percent_items = []
    shareholdings_items = []
    salary_items = []
    private_items = []
    rental_items = []
    gifts_items = []
    gifts_outside_uk_items = []
    direct_donations_items = []
    indirect_donations_items = []
    visits_outside_uk_items = []
    property_items = []

    # find category info
    for category in member['categories']:

        # private_income
        if category['category_type'] == 'employment':
            private_income = category['category_income']
            private_items = category['items']

        # indirect_donations
        if category['category_type'] == 'indirect_donations':
            for item in category['items']:
                indirect_donations += int(item['amount'])
            indirect_donations_items = category['items']

        # direct_donations
        if category['category_type'] == 'direct_donations':
            for item in category['items']:
                direct_donations += int(item['amount'])
            direct_donations_items = category['items']

        # gifts
        if category['category_type'] == 'gifts':
            for item in category['items']:
                gifts += int(item['amount'])
            gifts_items = category['items']

        # gifts_outside_uk
        if category['category_type'] == 'gifts_outside_uk':
            for item in category['items']:
                gifts_outside_uk += int(item['amount'])
            gifts_outside_uk_items = category['items']

        # visits
        if category['category_type'] == 'visits_outside_uk':
            for item in category['items']:
                visits_outside_uk += int(item['amount'])
            visits_outside_uk_items = category['items']

        # property income and wealth
        if category['category_type'] == 'property':

            rental_items = []
            property_items = []

            for item in category['items']:
                if item['isWealth']:
                    property_wealth += int(item['amount'])
                    property_items.append(item)
                else:
                    rental_income += int(item['amount'])
                    rental_items.append(item)

        if category['category_type'] == 'shareholdings':

            for item in category['items']:

                if item['amount'] > 1:
                    # this is a minimum of 70k, total amount will be in multiples of 70k.
                    # until we find a better way of finding accurate value
                    shareholdings += int(item['amount'])
                    shareholdings_items.append(item)

                else:
                    # simply represents a shareholding of 15% or more. we need to query companies house
                    # to find actual minimum value. for now we just count the number of percentage shareholdings
                    shareholdings_percent += int(item['amount'])
                    item['amount'] = '15%'
                    shareholdings_percent_items.append(item)

        # public salary
        if category['category_type'] == 'salary':
            salary =  category['category_income']

            salary_items = category['items']

        # family
        if category['category_type'] == 'family':
            if len(category['items']) > 0:
                family = True
                for f in category['items']:
                    # print f['pretty']
                    family_pretty += '%s\n' % f['pretty']

        # family lobbyists
        if category['category_type'] == 'family_lobbyists':
            if len(category['items']) > 0:
                family = True
                for f in category['items']:
                    # print f['pretty']
                    family_pretty += '%s\n' % f['pretty']

    total_income = private_income + rental_income + salary
    total_wealth = shareholdings + property_wealth
    total_freebies = gifts + direct_donations + indirect_donations + gifts_outside_uk + visits_outside_uk


    total_income_f = format_integer(total_income)
    total_wealth_f = format_integer(total_wealth)
    total_freebies_f = format_integer(total_freebies)


    private_income_f = format_integer(private_income)
    rental_income_f = format_integer(rental_income)
    salary_f = format_integer(salary)

    gifts_f = format_integer(gifts)
    gifts_outside_uk_f = format_integer(gifts_outside_uk)
    visits_outside_uk_f = format_integer(visits_outside_uk)

    direct_donations_f = format_integer(direct_donations)
    indirect_donations_f = format_integer(indirect_donations)

    shareholding_wealth_f = format_integer(shareholdings)
    property_wealth_f = format_integer(property_wealth)

    name = member['name']
    income = locale.currency(member['mp_income'], grouping=True).split('.')[0]
    wealth = locale.currency(member['mp_wealth'], grouping=True).split('.')[0]
    # gifts = locale.currency(member['mp_gifts'], grouping=True).split('.')[0]
    # donations = locale.currency(member['mp_donations'], grouping=True).split('.')[0]
    annual = locale.currency(member['mp_annual'], grouping=True).split('.')[0]

    member_id = member['member_id']
    party = member['party']
    constituency = member['constituency']

    # if party not in parties:
    #     parties.append(party)

    party_dict = {

                'conservative' : 'conservative',
                'liberal democrat' : 'liberal',
                'labour' : 'labour',
                'speaker' : 'speaker',
                'scottish national party' : 'scottish',
                'independent' : 'independent',
                'social democratic and labour party' : 'sdlp', # irish
                'labour/co-operative' : 'labour-co-op',
                'dup' : 'dup', # irish
                'ukip' : 'ukip',
                'uup' : 'uup', # irish
                'green' : 'greenparty',
                'plaid cymru' : 'plaid',
                u'sinn féin' : 'sinn' # irish

    }

    # BUILD THE HTML
    html = u"\n"

    html += '\t\t<div class="photo col panel %s %s %s %s %s" data-salary=%s data-privateinc=%s data-rental=%s data-income=%s data-gifts=%s data-gifts_outside_uk=%s data-direct_donations=%s data-indirect_donations=%s data-visits_outside_uk=%s data-freebies=%s data-shareholdings=%s data-shareholdings_percent=%s data-property=%s data-wealth=%s data-member=%s>\n' % (name.lower(), party.lower(), party_dict[party.lower()], constituency.lower(), str(member_id), int(salary), int(private_income), int(rental_income), int(total_income), int(gifts), int(gifts_outside_uk), int(direct_donations), int(indirect_donations), int(visits_outside_uk), int(total_freebies), int(shareholdings), int(shareholdings_percent), int(property_wealth), int(total_wealth), str(member_id))
    html += '\t\t\t<div class="panelHeader">\n'

    if family:
        html += '\t\t\t\t<img class="family" src="lib/images/family.png" title="%s" height="32" width="32" align="right"></img></br>\n' % family_pretty
    else:
        html += '\t\t\t\t<img class="nofamily" src="lib/images/placeholder.png" height="32" width="32" align="right"></img></br>\n'
    html += '\t\t\t\t<p></p>\n'
    
    if os.path.exists(os.path.join(lib_path, 'images', '%s.jpg' % str(member_id))):

        html += '<a href="pages/%s.html">' % member_id
        # html += '\t\t\t\t<img class="picture" src="lib/images/%s.png" height="128" width="128" onclick="expandWidget()" align="right=middle"></img>\n' % (str(member_id))
        html += '\t\t\t\t<img class="picture" src="lib/images/%s.jpg" height="128" width="128" align="right=middle"></img>\n' % (str(member_id))
        html += '</a>'

    else:
        # html += '\t\t\t\t<img src="lib/images/photo.png" height="128" width="128" onclick="expandWidget()" align="right=middle"></img>\n'
        html += '\t\t\t\t<img src="lib/images/photo.png" height="128" width="128" align="right=middle"></img>\n'

    # html += '\t\t\t\t<p></p><br/>\n'
    html += '\t\t\t\t<p class="name">%s</p>\n' % (name)
    html += '\t\t\t\t<p class="party">%s</p>\n' % (party)
    html += '\t\t\t\t<p class="constituency">%s</p>\n' % (constituency)
    html += '\t\t\t</div>\n'
    html += '\t\t\t<div class="panelBody">\n'

    html += '\t\t\t\t<table class="myTable2" style="width: 92%;">\n'

    html += '\t\t\t\t\t<tr class="toggle" style="display: none">\n'
    html += '\t\t\t\t\t\t<td class="toggle" style="display: none">Public Salary</td>\n'
    html += '\t\t\t\t\t\t<td class="toggle" align="right" style="display: none">%s</td>\n' % (salary_f)
    html += '\t\t\t\t\t</tr class="toggle" style="display: none">\n'

    html += '\t\t\t\t\t<tr class="toggle" style="display: none">\n'
    html += '\t\t\t\t\t\t<td class="toggle" style="display: none">Private Income</td>\n'
    html += '\t\t\t\t\t\t<td class="toggle" align="right" style="display: none">%s</td>\n' % (private_income_f)
    html += '\t\t\t\t\t</tr>\n'

    html += '\t\t\t\t\t<tr class="toggle" style="display: none">\n'
    html += '\t\t\t\t\t\t<td class="toggle" style="display: none">Rental Income (Min)</td>\n'
    html += '\t\t\t\t\t\t<td class="toggle" align="right" style="display: none">%s</td>\n' % (rental_income_f)
    html += '\t\t\t\t\t</tr>\n'

    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td><b>Total Income (Min)</b></td>\n'
    html += '\t\t\t\t\t\t<td align="right"><b>%s</b></td>\n' % (total_income_f)
    html += '\t\t\t\t\t</tr>\n'

    html += '\t\t\t\t\t<td class="toggle" style="display: none"><br/></td>\n'

    html += '\t\t\t\t\t<tr class="toggle" style="display: none">\n'
    html += '\t\t\t\t\t\t<td class="toggle" style="display: none">Gifts</td>\n'
    html += '\t\t\t\t\t\t<td class="toggle" align="right" style="display: none">%s</td>\n' % (gifts_f)
    html += '\t\t\t\t\t</tr>\n'

    html += '\t\t\t\t\t<tr class="toggle" style="display: none">\n'
    html += '\t\t\t\t\t\t<td class="toggle" style="display: none">Gifts Outside UK</td>\n'
    html += '\t\t\t\t\t\t<td class="toggle" align="right" style="display: none">%s</td>\n' % (gifts_outside_uk_f)
    html += '\t\t\t\t\t</tr>\n'

    html += '\t\t\t\t\t<tr class="toggle" style="display: none">\n'
    html += '\t\t\t\t\t\t<td class="toggle" style="display: none">Direct Donations</td>\n'
    html += '\t\t\t\t\t\t<td class="toggle" align="right" style="display: none">%s</td>\n' % (direct_donations_f)
    html += '\t\t\t\t\t</tr>\n'

    html += '\t\t\t\t\t<tr class="toggle" style="display: none">\n'
    html += '\t\t\t\t\t\t<td class="toggle" style="display: none">Indirect Donations</td>\n'
    html += '\t\t\t\t\t\t<td class="toggle" align="right" style="display: none">%s</td>\n' % (indirect_donations_f)
    html += '\t\t\t\t\t</tr>\n'

    html += '\t\t\t\t\t<tr class="toggle" style="display: none">\n'
    html += '\t\t\t\t\t\t<td class="toggle" style="display: none">Overseas Visits</td>\n'
    html += '\t\t\t\t\t\t<td class="toggle" align="right" style="display: none">%s</td>\n' % (visits_outside_uk_f)
    html += '\t\t\t\t\t</tr>\n'

    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td><b>Total Freebies</b></td>\n'
    html += '\t\t\t\t\t\t<td align="right"><b>%s</b></td>\n' % (total_freebies_f)
    html += '\t\t\t\t\t</tr>\n'

    html += '\t\t\t\t\t<td class="toggle" style="display: none"><br/></td>\n'

    html += '\t\t\t\t\t<tr class="toggle" style="display: none">\n'
    html += '\t\t\t\t\t\t<td class="toggle" style="display: none">Shareholdings 15% +</td>\n'
    html += '\t\t\t\t\t\t<td class="toggle" align="right" style="display: none">%s</td>\n' % (shareholdings_percent)
    html += '\t\t\t\t\t</tr>\n'

    html += '\t\t\t\t\t<tr class="toggle" style="display: none">\n'
    html += '\t\t\t\t\t\t<td class="toggle" style="display: none">Shareholdings &#163;70,000 + (Min)</td>\n'
    html += '\t\t\t\t\t\t<td class="toggle" align="right" style="display: none">%s</td>\n' % (shareholding_wealth_f)
    html += '\t\t\t\t\t</tr>\n'

    html += '\t\t\t\t\t<tr class="toggle" style="display: none">\n'
    html += '\t\t\t\t\t\t<td class="toggle" style="display: none">Property (Min)</td>\n'
    html += '\t\t\t\t\t\t<td class="toggle" align="right" style="display: none">%s</td>\n' % (property_wealth_f)
    html += '\t\t\t\t\t</tr>\n'

    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td><b>Total Wealth (Min)</b></td>\n'
    html += '\t\t\t\t\t\t<td align="right"><b>%s</b></td>\n' % (total_wealth_f)
    html += '\t\t\t\t\t</tr>\n'


    html += '\t\t\t\t</table>\n'

    html += '\t\t\t</div>\n'
    html += '\t\t</div>\n'

    # write_mp_page(member)

    # write it out
    with open(html_file, "a") as myfile:
        myfile.write(html.encode("utf8"))

    # -------------------------------------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------------------------------

    # mp_html_file = os.path.join(os.path.dirname(__file__), '../pages/%s.html' % member_id)
    html = u"\n"


    # html += '\t\t\t\t\t<td class="toggle2 income"><br/></td>\n'

    ###########################################################################################################
    # EXPANDED

    # BUILD THE HTML
    html += '\t\t<div class="photo col2 bigWidget panel2 %s %s %s %s %s" data-salary=%s data-privateinc=%s data-rental=%s data-income=%s data-gifts=%s data-gifts_outside_uk=%s data-direct_donations=%s data-indirect_donations=%s data-visits_outside_uk=%s data-freebies=%s data-shareholdings=%s data-shareholdings_percent=%s data-property=%s data-wealth=%s data-member=%s>\n' % (name.lower(), party.lower(), party_dict[party.lower()], constituency.lower(), str(member_id), int(salary), int(private_income), int(rental_income), int(total_income), int(gifts), int(gifts_outside_uk), int(direct_donations), int(indirect_donations), int(visits_outside_uk), int(total_freebies), int(shareholdings), int(shareholdings_percent), int(property_wealth), int(total_wealth), str(member_id))
    html += '\t\t\t<div class="panelHeader photo data-member=%s">\n' % (str(member_id))

    # if family:
    #     html += '\t\t\t\t<img class="family" src="../lib/images/family.png" title="%s" height="32" width="32" align="right"></img></br>\n' % family_pretty
    # else:
    #     html += '\t\t\t\t<img class="nofamily" src="../lib/images/placeholder.png" height="32" width="32" align="right"></img></br>\n'
    # html += '\t\t\t\t<p></p>\n'
    
    if os.path.exists(os.path.join(lib_path, 'images', '%s.jpg' % str(member_id))):
        # html += '\t\t\t\t<img class="picture" src="lib/images/%s.png" height="128" width="128" onclick="expandWidget()" align="right=middle"></img>\n' % (str(member_id))
        html += '\t\t\t\t<img class="picture" src="../lib/images/%s.jpg" height="128" width="128" align="right=middle"></img>\n' % (str(member_id))

    else:
        # html += '\t\t\t\t<img src="lib/images/photo.png" height="128" width="128" onclick="expandWidget()" align="right=middle"></img>\n'
        html += '\t\t\t\t<img src="../lib/images/photo.png" height="128" width="128" align="right=middle"></img>\n'


    html += '\t\t\t\t%s, %s, %s\n' % (name, party, constituency)


    # html += '\t\t\t\t<p></p><br/>\n'
    # html += '\t\t\t\t<p class="name">%s\n' % (name)
    # html += '\t\t\t\t<p class="party">%s\n' % (party)
    # html += '\t\t\t\t<p class="constituency">%s\n' % (constituency)
    html += '\t\t\t</div>\n'
    html += '\t\t\t<div class="panelBody">\n'

    html += '\t\t\t\t<table class="myTable3 " style="width: 92%;">\n'

    ############################################################################################################
    # PUBLIC SALARY

    # html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'
    # html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'

    html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    html += '\t\t\t\t\t\t<td class="toggle2 income bigger"><b>Public Salary</b></td>\n'
    html += '\t\t\t\t\t\t<td class="toggle2 income" align="right"><b>%s</b></td>\n' % (salary_f)
    html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    for item in salary_items:

        html += '\t\t\t\t\t<tr class="toggle2 income">\n'
        html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:140]
        html += '\t\t\t\t\t\t<td class="toggle2 income" align="right">%s</td>\n' % format_integer(item['amount'])
        html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    ############################################################################################################
    # PRIVATE INCOME

    html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'
    html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'

    html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    html += '\t\t\t\t\t\t<td class="toggle2 income bigger"><b>Private Income</b></td>\n'
    html += '\t\t\t\t\t\t<td class="toggle2 income" align="right"><b>%s</b></td>\n' % (private_income_f)
    html += '\t\t\t\t\t</tr>\n'

    for item in private_items:

        html += '\t\t\t\t\t<tr class="toggle2 income">\n'
        html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:140]
        html += '\t\t\t\t\t\t<td class="toggle2 income" align="right">%s</td>\n' % format_integer(item['amount'])
        html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    ############################################################################################################
    # RENTAL INCOME

    html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'
    html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'
    
    html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    html += '\t\t\t\t\t\t<td class="toggle2 income bigger"><b>Rental Income</b></td>\n'
    html += '\t\t\t\t\t\t<td class="toggle2 income" align="right"><b>%s</b></td>\n' % (rental_income_f)
    html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    for item in rental_items:

        html += '\t\t\t\t\t<tr class="toggle2 income">\n'
        html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:140]
        html += '\t\t\t\t\t\t<td class="toggle2 income" align="right">%s</td>\n' % format_integer(item['amount'])
        html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    ############################################################################################################
    # TOTAL INCOME

    html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'
    html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'

    html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    html += '\t\t\t\t\t\t<td class="toggle2total toggle2 income bigger"><b>Total Income (Min)</br></td>\n'
    html += '\t\t\t\t\t\t<td class="toggle2total toggle2 income" align="right"><b>%s</b></td>\n' % (total_income_f)
    html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    ############################################################################################################
    # GIFTS

    html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'
    html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'

    html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    html += '\t\t\t\t\t\t<td class="toggle2 income bigger"><b>Gifts</b></td>\n'
    html += '\t\t\t\t\t\t<td class="toggle2 income" align="right"><b>%s</b></td>\n' % (gifts_f)
    html += '\t\t\t\t\t</tr>\n'

    for item in gifts_items:

        html += '\t\t\t\t\t<tr class="toggle2 income">\n'
        html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:140]
        html += '\t\t\t\t\t\t<td class="toggle2 income" align="right">%s</td>\n' % format_integer(item['amount'])
        html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    ############################################################################################################
    # GIFTS OUTSIDE UK

    html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'
    html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'

    html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    html += '\t\t\t\t\t\t<td class="toggle2 income bigger"><b>Gifts Outside UK</b></td>\n'
    html += '\t\t\t\t\t\t<td class="toggle2 income" align="right"><b>%s</b></td>\n' % (gifts_outside_uk_f)    
    html += '\t\t\t\t\t</tr>\n'

    for item in gifts_outside_uk_items:

        html += '\t\t\t\t\t<tr class="toggle2 income">\n'
        html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:140]
        html += '\t\t\t\t\t\t<td class="toggle2 income" align="right">%s</td>\n' % format_integer(item['amount'])
        html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    ############################################################################################################
    # DIRECT DONATIONS

    html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'
    html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'

    html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    html += '\t\t\t\t\t\t<td class="toggle2 income bigger"><b>Direct Donations</b></td>\n'
    html += '\t\t\t\t\t\t<td class="toggle2 income" align="right"><b>%s</b></td>\n' % (direct_donations_f)    
    html += '\t\t\t\t\t</tr>\n'

    for item in direct_donations_items:

        html += '\t\t\t\t\t<tr class="toggle2 income">\n'
        html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:140]
        html += '\t\t\t\t\t\t<td class="toggle2 income" align="right">%s</td>\n' % format_integer(item['amount'])
        html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    ############################################################################################################
    # DIRECT DONATIONS

    html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'
    html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'

    html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    html += '\t\t\t\t\t\t<td class="toggle2 income bigger"><b>Indirect Donations</b></td>\n'
    html += '\t\t\t\t\t\t<td class="toggle2 income" align="right"><b>%s</b></td>\n' % (indirect_donations_f)    
    html += '\t\t\t\t\t</tr>\n'

    for item in indirect_donations_items:

        html += '\t\t\t\t\t<tr class="toggle2 income">\n'
        html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:140]
        html += '\t\t\t\t\t\t<td class="toggle2 income" align="right">%s</td>\n' % format_integer(item['amount'])
        html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    ############################################################################################################
    # VISITS OUTSIDE UK

    html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'
    html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'

    html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    html += '\t\t\t\t\t\t<td class="toggle2 income bigger"><b>Overseas Visits</b></td>\n'
    html += '\t\t\t\t\t\t<td class="toggle2 income" align="right"><b>%s</b></td>\n' % (visits_outside_uk_f)    
    html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    for item in visits_outside_uk_items:

        html += '\t\t\t\t\t<tr class="toggle2 income">\n'
        html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:140]
        html += '\t\t\t\t\t\t<td class="toggle2 income" align="right">%s</td>\n' % format_integer(item['amount'])
        html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    ############################################################################################################
    # TOTAL FREEBIES

    html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'
    html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'

    html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    html += '\t\t\t\t\t\t<td class="toggle2total income bigger"><b>Total Freebies</br></td>\n'
    html += '\t\t\t\t\t\t<td class="toggle2total income" align="right"><b>%s</b></td>\n' % (total_freebies_f)
    html += '\t\t\t\t\t</tr>\n'

    ############################################################################################################
    # SHAREHOLDINGS PERCENT

    html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'
    html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'

    html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    html += '\t\t\t\t\t\t<td class="toggle2 income bigger"><b>Shareholdings 15% +</b></td>\n'
    html += '\t\t\t\t\t\t<td class="toggle2 income" align="right"><b>%s</b></td>\n' % (shareholdings_percent)
    html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    for item in shareholdings_percent_items:

        html += '\t\t\t\t\t<tr class="toggle2 income">\n'
        html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['raw_string'][:140]
        html += '\t\t\t\t\t\t<td class="toggle2 income" align="right">%s</td>\n' % str(item['amount'])
        html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    ############################################################################################################
    # SHAREHOLDINGS

    html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'
    html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'

    html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    html += '\t\t\t\t\t\t<td class="toggle2 income bigger"><b>Shareholdings &#163;70,000 + (Min)</b></td>\n'
    html += '\t\t\t\t\t\t<td class="toggle2 income" align="right"><b>%s</b></td>\n' % (shareholding_wealth_f)
    html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    for item in shareholdings_items:

        html += '\t\t\t\t\t<tr class="toggle2 income">\n'
        html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['raw_string'][:140]
        html += '\t\t\t\t\t\t<td class="toggle2 income" align="right">%s</td>\n' % format_integer(item['amount'])
        html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    ############################################################################################################
    # PROPERTY

    html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'
    html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'

    html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    html += '\t\t\t\t\t\t<td class="toggle2 income bigger"><b>Property (Min)</b></td>\n'
    html += '\t\t\t\t\t\t<td class="toggle2 income" align="right"><b>%s</b></td>\n' % (property_wealth_f)
    html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    for item in property_items:

        html += '\t\t\t\t\t<tr class="toggle2 income">\n'
        html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:140]
        html += '\t\t\t\t\t\t<td class="toggle2 income" align="right">%s</td>\n' % format_integer(item['amount'])
        html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    ############################################################################################################
    # TOTAL WEALTH

    html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'
    html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'

    html += '\t\t\t\t\t<tr class="toggle2">\n'
    html += '\t\t\t\t\t\t<td class="toggle2total income bigger"><b>Total Wealth (Min)</br></td>\n'
    html += '\t\t\t\t\t\t<td class="toggle2total income" align="right"><b>%s</b></td>\n' % (total_wealth_f)
    html += '\t\t\t\t\t</tr>\n'


    # END TABLE
    html += '\t\t\t\t</table>\n'
    html += '\t\t\t</div>\n'
    html += '\t\t</div>'

    # html = '<html>\n'
    # html += '<p>%s</p>\n' % member_id

    # if os.path.exists(os.path.join(lib_path, 'images', '%s.jpg' % str(member_id))):
    #     html += '\t\t\t\t<img class="picture" src="../lib/images/%s.jpg" height="128" width="128" align="right=middle"></img>\n' % (str(member_id))
    # else:
    #     html += '\t\t\t\t<img src="../lib/images/photo.png" height="128" width="128" align="right=middle"></img>\n'

    # html += '</html>'

    # write it out
    with open(mp_html_file, "a") as myfile2:
        myfile2.write(html.encode("utf8"))

def feeback(mps):
    """"""

    # now print by options specified on commandline
    for member in mps:
        name = member['name']
        income = locale.currency(member['mp_income'], grouping=True)
        wealth = locale.currency(member['mp_wealth'], grouping=True)
        gifts = locale.currency(member['mp_gifts'], grouping=True)
        donations = locale.currency(member['mp_donations'], grouping=True)
        annual = locale.currency(member['mp_annual'], grouping=True)
        forname = member['forname']
        surname = member['surname']
        member_id = member['member_id']

        names = [forname, surname, name]

        print '*' * 150
        print name, '(' + member['party'] + ')', member['constituency']
        print 'Income :', income, ' |  Wealth :', wealth, ' |  Gifts :', gifts, ' |  Donations :', donations, ' |  Annual :', annual
        print os.path.abspath(os.path.join(images_directory, '%s_%s_%s.png' % (forname, surname, member_id)))
        print '*' * 150
        print ''

        # refresh_html_file(member)
        # print_register_of_intrests(member)

        # data = get_companies_house_person(user=companies_house_user, names=names, addresses=[])
        # data = filter_by_first_last_name(data, forname, surname, name)
        # data = filter_by_appointment_counts(data)
        # data = get_appointments(user=companies_house_user, data=data, status=['active'])

        # print_companies_house_info(data)

        # now we have an idea of the active appointments of people with the exact same
        # name as the member of parliament

        # we should check with the shareholding data in the member dictionary
        # it's a start at least


def print_register_of_intrests(member):
    """
    Function to print out the register of intrests
    """
    for category in member['categories']:

        category_amount = category['category_amount']

        # if its currency, format it
        if category['isCurrency']:
            print '\t', category['category_description'], '', locale.currency(category_amount, grouping=True)
        else:
            print '\t', category['category_description']

        for item in category['items']:

            item_amount = item['amount']

            if category['isCurrency']:
                print '\t\t', item['pretty'], locale.currency(item_amount, grouping=True)
            else:
                print '\t\t', item['pretty']


def print_companies_house_info(data):
    """
    Function to print out companies house matches
    """

    print '-' * 100
    print 'Companies House Lookup'
    print '-' * 100
    print ''
    for matched_person in data:
        print matched_person['title']
        print matched_person['appointments']
        for status in matched_person['appointments'].keys():

            active_appointments = matched_person['appointments'][status]

            for app in active_appointments:

                role = app['officer_role']
                company_links = app['links']
                company_name = app['appointed_to']['company_name']
                company_number = app['appointed_to']['company_number']
                company_status = app['appointed_to']['company_status']

                if app.has_key('resigned_on'):
                    resigned_on = app['resigned_on']
                else:
                    resigned_on = None
                if app.has_key('occupation'):
                    occupation = app['occupation']
                else:
                    occupation = None

                address_string = ''
                address = app['address']
                keys = ['address_line_1', 'address_line_2',
                        'locality', 'postal_code']

                for k in keys:
                    if address.has_key(k):
                        address_string += '%s, ' % address[k]

                print '\t%s, %s, %s' % (company_name, company_status, role)
                print '\t\t%s' % address_string


def sort_by_options(mps, options):
    """
    Sort by options
    """

    # sort by options specified on commandline
    if options.sortby == 'wealth':
        mps = sorted(mps, key=operator.itemgetter('mp_wealth'), reverse=True)

    elif options.sortby == 'income':
        mps = sorted(mps, key=operator.itemgetter('mp_income'), reverse=True)

    elif options.sortby == 'gifts':
        mps = sorted(mps, key=operator.itemgetter('mp_gifts'), reverse=True)

    elif options.sortby == 'donations':
        mps = sorted(mps, key=operator.itemgetter(
            'mp_donations'), reverse=True)

    elif options.sortby == 'annual':
        mps = sorted(mps, key=operator.itemgetter('mp_annual'), reverse=True)

    else:
        mps = sorted(mps, key=operator.itemgetter(
            '%s' % options.sortby), reverse=True)

    return mps


def read_json_file():
    """
    Read file from json_dump_location
    """
    with open(json_dump_location) as json_data:
        return json.load(json_data)

if __name__ == "__main__":
    """
    Commandline run
    """
    parser = OptionParser()

    # parser.add_option("--summary", help="Summary print", action="store_true", default=True)
    # parser.add_option("--detailed", help="Detailed print", action="store_true", default=False)
    parser.add_option("--sortby", help="Sort By",
                      action="store", default='income')

    # parse the comand line
    (options, args) = parser.parse_args()

    # return a list (of dicts) of mps
    mps = read_json_file()
    # print mps

    searched = []

    # TODO: fix this crude arg porser
    if args:
        for member in args:
            for i in mps:
                if member.lower() in i['name'].lower():
                    searched.append(i)
                if member.lower() in i['party'].lower():
                    searched.append(i)
                if member.lower() in i['constituency'].lower():
                    searched.append(i)

        mps = searched

    main(mps, options)
