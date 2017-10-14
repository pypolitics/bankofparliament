#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os, sys
import operator
import locale, subprocess
import pprint
from optparse import OptionParser
from textblob import TextBlob

sys.path.append('../lib/python')

import shutil

from generate_thumbnail import write_thumbnail
from generate_register import write_register
from generate_companieshouse import write_companieshouse
from generate_plot import write_scatter_plot

locale.setlocale(locale.LC_ALL, '')

json_dump_location = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..', 'lib', 'data', 'members_dump.json')

lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lib')

images_directory = os.path.join(os.path.dirname(__file__), '..', 'images')
companies_house_user = 'ZCCtuxpY7uvkDyxLUz37dCYFIgke9PKfhMlEGC-Q'

top_html = os.path.join(os.path.dirname(__file__), '../lib/html/top.html')
register_top_html = os.path.join(os.path.dirname(__file__), '../lib/html/register_top.html')
appointments_top_html = os.path.join(os.path.dirname(__file__), '../lib/html/appointments_top.html')

tail_html = os.path.join(os.path.dirname(__file__), '../lib/html/tail.html')
register_tail_html = os.path.join(os.path.dirname(__file__), '../lib/html/register_tail.html')
appointments_tail_html = os.path.join(os.path.dirname(__file__), '../lib/html/appointments_tail.html')

html_file = os.path.join(os.path.dirname(__file__), '../index.html')

def main(mps):
    """
    Main
    """

    print_to_html_file(mps)

def print_to_html_file(mps):
    start_html_file()
    for mp in mps:

        # output paths
        register_file = os.path.join(os.path.dirname(__file__), '../pages/register/%s.html' % mp['member_id'])
        companies_file = os.path.join(os.path.dirname(__file__), '../pages/companieshouse/%s.html' % mp['member_id'])
        
        # start a page for register and appointments
        start_html_file(mp['member_id'], tops_html=register_top_html, html_file=register_file)
        start_html_file(mp['member_id'], tops_html=appointments_top_html, html_file=companies_file)

        print_mp_panel_into_file(mp, register_file, companies_file)

        end_html_file(tails_html=register_tail_html, html_file=register_file)
        end_html_file(tails_html=appointments_tail_html, html_file=companies_file)

    end_html_file()

def start_html_file(member_id='', tops_html=top_html, html_file=html_file):

    shutil.copy2(tops_html, html_file)
    
    if not member_id == '':
        command = "sed -i '' 's/MEMBER_ID/%s/g' %s" % (member_id, html_file)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = process.communicate()

def end_html_file(tails_html=tail_html, html_file=html_file):
    with open(html_file, "a") as fo:
        with open(tails_html, 'r') as fi:
            fo.write(fi.read())

def format_integer(number):

    loc = locale.currency(number, grouping=True).split('.')[0]
    return loc.replace("£", "&#163;")

def print_mp_panel_into_file(member, register_file, companies_file):

    cat_types = [each['category_type'] for each in member['categories']]

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
    miscellaneous = 0

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
    miscellaneous_items = []
    family_items = []
    family_lobbyists_items = []

    active_appointments = []
    previous_appointments = []

    self_link = ''
    keywords = []
    exclude = ['ltd', ' ', 'plc', 'limited', 'llp', 'the',  '-', 'and', 'united', 'kingdom', 'uk', 'false', 'true', 'none', 'n/a']

    dob_str = member['dob']
    if member.has_key('twitter'):
        twitter = member['twitter']
    else:
        twitter = ''

    for user in member['companies_house']:
        for item in user['items']:

            company_name = item['company_name'].split(' ')

            for n in company_name:
                if not n.lower() in exclude:
                    keywords.append(n.lower())

            if item['resigned_on'] == '' and item['company_status'].lower() == 'active' :
                active_appointments.append(item)

            else:
                previous_appointments.append(item)

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

                if item['amount'] == 70000:
                    # this is a minimum of 70k, total amount will be in multiples of 70k.
                    # until we find a better way of finding accurate value
                    shareholdings += int(item['amount'])
                    shareholdings_items.append(item)

                else:
                    # simply represents a shareholding of 15% or more. we need to query companies house
                    # to find actual minimum value. for now we just count the number of percentage shareholdings
                    shareholdings_percent += int(item['amount'])
                    # item['amount'] = '15%'
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
                    family_items.append(f)
                    keywords.append(f['pretty'])

        # family lobbyists
        if category['category_type'] == 'family_lobbyists':
            if len(category['items']) > 0:
                family = True
                for f in category['items']:
                    # print f['pretty']
                    family_pretty += '%s\n' % f['pretty']
                    family_lobbyists_items.append(f)
                    keywords.append(f['pretty'])

        # misc
        if category['category_type'] == 'miscellaneous':
            for item in category['items']:
                miscellaneous += int(item['amount'])
            miscellaneous_items = category['items']


    total_income = private_income + rental_income + salary
    total_wealth = shareholdings + property_wealth
    total_freebies = gifts + direct_donations + indirect_donations + gifts_outside_uk + visits_outside_uk


    total_income_f = format_integer(total_income)
    total_wealth_f = format_integer(total_wealth)
    total_freebies_f = format_integer(total_freebies)

    miscellaneous_f = format_integer(miscellaneous)

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
    annual = locale.currency(member['mp_annual'], grouping=True).split('.')[0]

    member_id = member['member_id']
    constituency = member['constituency']

    party = member['party'].lower()
    if party.lower().startswith('sinn'):
        party = 'Sinn Fein'.lower()
    
    party_dict = {

                'conservative' : 'conservative tory tories',
                'liberal democrat' : 'liberal democrat lib',
                'labour' : 'labour',
                'speaker' : 'speaker',
                'scottish national party' : 'scottish national snp',
                'independent' : 'independent',
                'social democratic and labour party' : 'sdlp', # irish
                'labour/co-operative' : 'labour co-op',
                'dup' : 'dup irish', # irish
                'ukip' : 'ukip',
                'uup' : 'uup irish', # irish
                'green' : 'greenparty green',
                'plaid cymru' : 'plaid wales welsh cymru',
                'sinn fein' : 'sinn fein irish' # irish
    }

    keywords.append(name)
    keywords.append(constituency)
    keywords.append(party_dict[party])

    nouns = ' '.join(keywords)

    # write the thumbail into the main front page
    write_thumbnail(html_file, family_pretty, member_id, name, party, party_dict[party], constituency, salary_f, private_income_f, rental_income_f, total_income_f, gifts_f, gifts_outside_uk_f, direct_donations_f, indirect_donations_f, visits_outside_uk_f, total_freebies_f, shareholdings_percent, shareholdings_percent_items, shareholding_wealth_f, active_appointments, property_wealth_f, total_wealth_f, salary, private_income, rental_income, total_income, gifts, gifts_outside_uk, property_wealth, total_wealth, direct_donations, indirect_donations, visits_outside_uk, total_freebies, shareholdings, previous_appointments, family, miscellaneous, miscellaneous_f, miscellaneous_items, family_items, family_lobbyists_items, twitter)

    # write the register page
    write_register(register_file, family_pretty, member_id, name, party, constituency, salary_f, private_income_f, rental_income_f, total_income_f, gifts_f, gifts_outside_uk_f, direct_donations_f, indirect_donations_f, visits_outside_uk_f, total_freebies_f, shareholdings_percent, shareholding_wealth_f, active_appointments, property_wealth_f, total_wealth_f, party_dict, salary, private_income, rental_income, total_income, gifts, gifts_outside_uk, property_wealth, total_wealth, direct_donations, indirect_donations, visits_outside_uk, total_freebies, shareholdings, previous_appointments, family, salary_items, private_items, rental_items, gifts_items, gifts_outside_uk_items, direct_donations_items, indirect_donations_items, visits_outside_uk_items, shareholdings_items, shareholdings_percent_items, property_items, miscellaneous_f, miscellaneous_items, family_items, family_lobbyists_items, dob_str)

    # write the companies house page
    write_companieshouse(companies_file, name, party, party_dict, constituency, member_id, active_appointments, previous_appointments, dob_str, member)

    # # write a word cloud image out
    # write_wordcloud(member_id, name, keywords)

    # # write scatter plot
    # write_scatter_plot(member)

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
    json_dump_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lib', 'data', 'members')
    data = []
    for mp in os.listdir(json_dump_location):
        f = os.path.join(json_dump_location, mp)
        with open(f) as json_data:
            data.append(json.load(json_data))

    return data

    # with open(json_dump_location) as json_data:
    #     return json.load(json_data)

def run():
    """"""
    mps = read_json_file()
    main(mps)

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

    mps = sort_by_options(mps, options)
    main(mps)
