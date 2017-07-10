#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, locale, pprint
locale.setlocale(locale.LC_ALL, '')
from utils import regex_for_ownership

companies_house_base_url = 'https://beta.companieshouse.gov.uk'

def format_integer(number):

    loc = locale.currency(number, grouping=True).split('.')[0]
    return loc.replace("£", "&#163;")

def write_companieshouse(html_file, name, party, party_dict, constituency, member_id, active_appointments, previous_appointments, dob_str, member):

    html = u"\n"
    html += '\t\t<div class="photo col2 bigWidget panel2 %s %s %s %s %s">\n' % (name.lower(), party.lower(), party_dict[party.lower()], constituency.lower(), str(member_id))
    html += '\t\t\t<div class="panelHeader photo data-member=%s">\n' % (str(member_id))

    # add the thumbnail
    s = os.path.join(os.path.dirname(__file__), '..', 'lib', 'images', '%s.jpg' % str(member_id))
    if os.path.exists(s):
        html += '\t\t\t\t<img class="picture" src="../../lib/images/%s.jpg" height="128" width="128" align="right=middle"></img>\n' % (str(member_id))
    else:
        html += '\t\t\t\t<img src="../../lib/images/photo.png" height="128" width="128" align="right=middle"></img>\n'

    # add the mp text
    html += '\t\t\t\t\t<a class="name_r">%s,</a>\n' % (name)
    html += '\t\t\t\t\t<a class="party_r">%s,</a>\n' % (party.title())
    html += '\t\t\t\t\t<a class="constituency_r">%s,</a>\n' % (constituency)
    html += '\t\t\t\t\t<a class="constituency_r">%s</a>\n' % (dob_str)

    html += '\t\t\t</div>\n'
    html += '\t\t\t<div class="panelBody">\n'
    html += '\t\t\t\t<table class="myTable3 " style="width: 92%;">\n'

    ############################################################################################################
    # ACTIVE

    html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    html += '\t\t\t\t\t\t<td class="toggle2 income bigger"><b>Active Appointments</b></td>\n'
    html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    for item in active_appointments:

        if item['appointment']['company'].has_key('links'):
            self = item['appointment']['company']['links']['self']
        else:
            self = '/'

        if item['appointment'].has_key('significant_ownership'):
            significant = item['appointment']['significant_ownership']
        else:
            significant = ''

        if item['appointment']['company'].has_key('company_name'):
            name = item['appointment']['company']['company_name']
        else:
            name = 'N/A'

        link = '%s%s' % (companies_house_base_url, self)

        html += '\t\t\t\t\t<tr class="toggle2 income">\n'
        if significant != '':
            ownership_range = regex_for_ownership(significant)
            html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - <b>%s</b> - Ownership %s%% - %s%%</td>\n' % (name[:125].title(), ownership_range[0], ownership_range[1])
        else:
            html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - <b>%s</b> </td>\n' % (name[:125].title())

        html += '\t\t\t\t\t\t<td>\n'
        html += '\t\t\t\t\t\t\t<a target="_blank" href="%s">\n' % (link)
        html += '\t\t\t\t\t\t\t\t<div style="height:100%;width:100%">'
        html += '\t\t\t\t\t\t\t\t\tLink\n'
        html += '\t\t\t\t\t\t\t\t</div>'
        html += '\t\t\t\t\t\t\t</a>\n'
        html += '\t\t\t\t\t\t</td>\n'

        html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    ############################################################################################################
    # HISTORIC

    html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'
    html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'

    html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    html += '\t\t\t\t\t\t<td class="toggle2 income bigger"><b>Historic Appointments</b></td>\n'
    html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    for item in previous_appointments:
        significant = ''

        if item['appointment']['company'].has_key('links'):
            self = item['appointment']['company']['links']['self']
        else:
            self = '/'

        if item['appointment'].has_key('significant_ownership'):
            significant = item['appointment']['significant_ownership']
        else:
            significant = ''

        if item['appointment']['company'].has_key('company_name'):
            name = item['appointment']['company']['company_name']
        else:
            name = 'N/A'

        link = '%s%s' % (companies_house_base_url, self)

        html += '\t\t\t\t\t<tr class="toggle2 income">\n'
        if significant != '':
            ownership_range = regex_for_ownership(significant)
            html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - <b>%s</b> - Ownership %s%% - %s%%</td>\n' % (name[:125].title(), ownership_range[0], ownership_range[1])
        else:
            html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - <b>%s</b> </td>\n' % (name[:125].title())
        html += '\t\t\t\t\t\t<td>\n'
        html += '\t\t\t\t\t\t\t<a target="_blank" href="%s">\n' % (link)
        html += '\t\t\t\t\t\t\t\t<div style="height:100%;width:100%">'
        html += '\t\t\t\t\t\t\t\t\tLink\n'
        html += '\t\t\t\t\t\t\t\t</div>'
        html += '\t\t\t\t\t\t\t</a>\n'
        html += '\t\t\t\t\t\t</td>\n'

        html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    # write it out
    with open(html_file, "a") as myfile2:
        myfile2.write(html.encode("utf8"))