#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import operator
import locale
import pprint
from optparse import OptionParser
from utils import get_companies_house_person, get_request, filter_by_first_last_name, filter_by_appointment_counts, get_appointments
import shutil

locale.setlocale(locale.LC_ALL, '')

json_dump_location = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..', 'json', 'members_dump.json')
images_directory = os.path.join(os.path.dirname(__file__), '..', 'images')
companies_house_user = 'ZCCtuxpY7uvkDyxLUz37dCYFIgke9PKfhMlEGC-Q'

tops_html = os.path.join(os.path.dirname(__file__), 'html_templates/tops.html')
html_file = os.path.join(os.path.dirname(__file__), 'generated.html')
tails_html = os.path.join(os.path.dirname(
    __file__), 'html_templates/tails.html')


def main(mps, options):
    """
    Main
    """
    mps = sort_by_options(mps, options)

    print_to_html_file(mps)


def print_to_html_file(mps):
    start_html_file()
    for mp in mps:
        print_mp_panel_into_file(mp)
    end_html_file()


def start_html_file():
    shutil.copy2(tops_html, html_file)

def format_integer(number):

    loc = locale.currency(number, grouping=True).split('.')[0]
    return loc.replace("£", "&#163;")

def print_mp_panel_into_file(member):

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
    donations = 0
    visits = 0

    # expenses
    expenses = 0

    # wealth
    property_wealth = 0
    shareholding_wealth = 0

    # find category info
    for category in member['categories']:

        # private_income
        if category['category_type'] == 'employment':
            private_income = category['category_income']

        # indirect_donations
        if category['category_type'] == 'indirect_donations':
            for item in category['items']:
                donations += int(item['amount'])

        # direct_donations
        if category['category_type'] == 'direct_donations':
            for item in category['items']:
                donations += int(item['amount'])

        # gifts
        if category['category_type'] == 'gifts':
            for item in category['items']:
                gifts += int(item['amount'])

        # visits
        if category['category_type'] == 'visits':
            for item in category['items']:
                visits += int(item['amount'])

        # property income and wealth
        if category['category_type'] == 'property':

            for item in category['items']:
                if item['isWealth']:
                    property_wealth += int(item['amount'])
                else:
                    rental_income += int(item['amount'])

        # shareholdings
        if category['category_type'] == 'shareholdings':

            for item in category['items']:
                if item['isWealth']:
                    # this number in inaccurate, we know the value of the holding is at least
                    # 15% - we need to look at company accounts on companies house to determine
                    # the value of the is percentage
                    shareholding_wealth += int(item['amount'])

        # public salary
        if category['category_type'] == 'salary':
            salary =  category['category_income']


    total_income = format_integer(private_income + rental_income + salary)
    total_wealth = format_integer(shareholding_wealth + property_wealth)
    total_freebies = format_integer(gifts + donations + visits)


    private_income = format_integer(private_income)
    rental_income = format_integer(rental_income)
    salary = format_integer(salary)

    gifts = format_integer(gifts)
    donations = format_integer(donations)
    visits = format_integer(visits)

    expenses = format_integer(expenses)

    shareholding_wealth = format_integer(shareholding_wealth)
    property_wealth = format_integer(property_wealth)


    html = u"\n"

    name = member['name']
    income = locale.currency(member['mp_income'], grouping=True).split('.')[0]
    wealth = locale.currency(member['mp_wealth'], grouping=True).split('.')[0]
    # gifts = locale.currency(member['mp_gifts'], grouping=True).split('.')[0]
    # donations = locale.currency(member['mp_donations'], grouping=True).split('.')[0]
    annual = locale.currency(member['mp_annual'], grouping=True).split('.')[0]

    member_id = member['member_id']
    party = member['party']
    constituency = member['constituency']

    # because the party, constituency and name are all class names of the
    # col class, we rename Green to greenparty, so that we dont match 
    if party == 'Green':
        party = 'greenparty'

    html += '\t\t<div class="col %s %s %s">\n' % (name.lower(), party.lower(), constituency.lower())
    html += '\t\t\t<div id=%s class="myHeader">\n' % member_id

    html += '\t\t\t\t<br><img src="images/photo.png"></img></br>\n'
    html += '\t\t\t\t<br>%s\n' % (name)
    html += '\t\t\t\t<br><font size="2">%s</font>\n' % (constituency)
    html += '\t\t\t</div>\n'
    html += '\t\t\t<div class="body">\n'

    html += '\t\t\t\t<table class="myTable2" style="width: 92%;">\n'

    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td>Public Salary</td>\n'
    html += '\t\t\t\t\t\t<td align="right">%s</td>\n' % (salary)
    html += '\t\t\t\t\t</tr>\n'

    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td>Private Income</td>\n'
    html += '\t\t\t\t\t\t<td align="right">%s</td>\n' % (private_income)
    html += '\t\t\t\t\t</tr>\n'

    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td>Rental Income (Min)</td>\n'
    html += '\t\t\t\t\t\t<td align="right">%s</td>\n' % (rental_income)
    html += '\t\t\t\t\t</tr>\n'

    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td><b>Total Income (Min)</b></td>\n'
    html += '\t\t\t\t\t\t<td align="right"><b>%s</b></td>\n' % (total_income)
    html += '\t\t\t\t\t</tr>\n'

    html += '\t\t\t\t\t<td><br/></td>\n'

    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td>Gifts</td>\n'
    html += '\t\t\t\t\t\t<td align="right">%s</td>\n' % (gifts)
    html += '\t\t\t\t\t</tr>\n'

    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td>Donations</td>\n'
    html += '\t\t\t\t\t\t<td align="right">%s</td>\n' % (donations)
    html += '\t\t\t\t\t</tr>\n'

    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td>Overseas Visits</td>\n'
    html += '\t\t\t\t\t\t<td align="right">%s</td>\n' % (visits)
    html += '\t\t\t\t\t</tr>\n'

    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td><b>Total Freebies</b></td>\n'
    html += '\t\t\t\t\t\t<td align="right"><b>%s</b></td>\n' % (total_freebies)
    html += '\t\t\t\t\t</tr>\n'

    html += '\t\t\t\t\t<td><br/></td>\n'

    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td><b>Total Expenses</b></td>\n'
    html += '\t\t\t\t\t\t<td align="right"><b>%s</b></td>\n' % (expenses)
    html += '\t\t\t\t\t</tr>\n'


    html += '\t\t\t\t\t<td><br/></td>\n'

    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td>Shareholdings (Min)</td>\n'
    html += '\t\t\t\t\t\t<td align="right">%s</td>\n' % (shareholding_wealth)
    html += '\t\t\t\t\t</tr>\n'

    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td>Property (Min)</td>\n'
    html += '\t\t\t\t\t\t<td align="right">%s</td>\n' % (property_wealth)
    html += '\t\t\t\t\t</tr>\n'

    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td><b>Total Wealth (Min)</b></td>\n'
    html += '\t\t\t\t\t\t<td align="right"><b>%s</b></td>\n' % (total_wealth)
    html += '\t\t\t\t\t</tr>\n'


    html += '\t\t\t\t</table>\n'

    html += '\t\t\t</div>\n'
    html += '\t\t</div>'

    # write it out
    with open(html_file, "a") as myfile:
        myfile.write(html.encode("utf8"))

def end_html_file():
    with open(html_file, "a") as fo:
        with open(tails_html, 'r') as fi:
            fo.write(fi.read())


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
