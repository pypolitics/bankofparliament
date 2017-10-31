#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, locale
from utils import camel_case_split

locale.setlocale(locale.LC_ALL, '')

def format_integer(number):

    loc = locale.currency(number, grouping=True).split('.')[0]
    return loc.replace("£", "&#163;")

def write_register(html_file, family_pretty, member_id, name, party, constituency, salary_f, private_income_f, rental_income_f, total_income_f, gifts_f, gifts_outside_uk_f, direct_donations_f, indirect_donations_f, visits_outside_uk_f, total_freebies_f, shareholdings_percent, shareholding_wealth_f, active_appointments, property_wealth_f, total_wealth_f, party_dict, salary, private_income, rental_income, total_income, gifts, gifts_outside_uk, property_wealth, total_wealth, direct_donations, indirect_donations, visits_outside_uk, total_freebies, shareholdings, previous_appointments, family, salary_items, private_items, rental_items, gifts_items, gifts_outside_uk_items, direct_donations_items, indirect_donations_items, visits_outside_uk_items, shareholdings_items, shareholdings_percent_items, property_items, miscellaneous_f, miscellaneous_items, family_items, family_lobbyists_items, dob_str):

    html = u"\n"
    html += '\t\t<div class="detailed_panel %s %s %s %s %s" data-salary=%s data-privateinc=%s data-rental=%s data-income=%s data-gifts=%s data-gifts_outside_uk=%s data-direct_donations=%s data-indirect_donations=%s data-visits_outside_uk=%s data-freebies=%s data-shareholdings=%s data-shareholdings_percent=%s data-property=%s data-wealth=%s data-member=%s data-miscellaneous=%s>\n' % (name.lower(), party.lower(), party_dict[party.lower()], constituency.lower(), str(member_id), int(salary), int(private_income), int(rental_income), int(total_income), int(gifts), int(gifts_outside_uk), int(direct_donations), int(indirect_donations), int(visits_outside_uk), int(total_freebies), int(shareholdings), int(shareholdings_percent), int(property_wealth), int(total_wealth), str(member_id), miscellaneous_f)
    html += '\t\t\t<div class="detailed_panel_header data-member=%s">\n' % (str(member_id))
    
    # add the thumbnail
    s = os.path.join(os.path.dirname(__file__), '..', 'lib', 'data', 'images', '%s.jpg' % str(member_id))
    if os.path.exists(s):
        html += '\t\t\t\t<img class="picture" src="../../lib/data/images/%s.jpg" height="128" width="128" align="right=middle"></img>\n' % (str(member_id))
    else:
        html += '\t\t\t\t<img src="../../lib/data/images/photo.png" height="128" width="128" align="right=middle"></img>\n'

    # add the mp text
    html += '\t\t\t\t\t<a class="name">%s,</a>\n' % (name)
    html += '\t\t\t\t\t<a class="party">%s,</a>\n' % (party.title())
    html += '\t\t\t\t\t<a class="constituency">%s</a>\n' % (constituency)

    html += '\t\t\t</div>\n'
    html += '\t\t\t<div class="detailed_panel_body">\n'
    html += '\t\t\t\t<table class="detailed_table"">\n'

    ############################################################################################################
    # PUBLIC SALARY

    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td class="category"><b>Public Salary</b></td>\n'
    html += '\t\t\t\t\t\t<td class="category" align="right"><b>%s</b></td>\n' % (salary_f)
    html += '\t\t\t\t\t</tr>\n'

    for item in salary_items:

        html += '\t\t\t\t\t<tr>\n'
        html += '\t\t\t\t\t\t<td>&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:200]
        html += '\t\t\t\t\t\t<td align="right">%s</td>\n' % format_integer(item['amount'])
        html += '\t\t\t\t\t</tr>\n'

    ############################################################################################################
    # PRIVATE INCOME

    html += '\t\t\t\t\t<td></br></td>\n'
    html += '\t\t\t\t\t<td></br></td>\n'

    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td class="category"><b>Private Income</b></td>\n'
    html += '\t\t\t\t\t\t<td class="category" align="right"><b>%s</b></td>\n' % (private_income_f)
    html += '\t\t\t\t\t</tr>\n'

    for item in private_items:

        html += '\t\t\t\t\t<tr>\n'
        html += '\t\t\t\t\t\t<td>&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:200]
        html += '\t\t\t\t\t\t<td align="right">%s</td>\n' % format_integer(item['amount'])
        html += '\t\t\t\t\t</tr>\n'

    ############################################################################################################
    # RENTAL INCOME

    html += '\t\t\t\t\t<td></br></td>\n'
    html += '\t\t\t\t\t<td></br></td>\n'
    
    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td class="category"><b>Rental Income</b></td>\n'
    html += '\t\t\t\t\t\t<td class="category" align="right"><b>%s</b></td>\n' % (rental_income_f)
    html += '\t\t\t\t\t</tr>\n'

    for item in rental_items:

        html += '\t\t\t\t\t<tr>\n'
        html += '\t\t\t\t\t\t<td>&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:200]
        html += '\t\t\t\t\t\t<td align="right">%s</td>\n' % format_integer(item['amount'])
        html += '\t\t\t\t\t</tr>\n'

    ############################################################################################################
    # TOTAL INCOME

    html += '\t\t\t\t\t<td></br></td>\n'
    html += '\t\t\t\t\t<td></br></td>\n'

    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td class="category category_total"><b>Total Income (Min)</br></td>\n'
    html += '\t\t\t\t\t\t<td class="category category_total" align="right"><b>%s</b></td>\n' % (total_income_f)
    html += '\t\t\t\t\t</tr>\n'    

    ############################################################################################################
    # GIFTS

    html += '\t\t\t\t\t<td></br></td>\n'
    html += '\t\t\t\t\t<td></br></td>\n'

    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td class="category"><b>Gifts</b></td>\n'
    html += '\t\t\t\t\t\t<td class="category" align="right"><b>%s</b></td>\n' % (gifts_f)
    html += '\t\t\t\t\t</tr>\n'

    for item in gifts_items:

        html += '\t\t\t\t\t<tr>\n'
        html += '\t\t\t\t\t\t<td>&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:200]
        # html += '\t\t\t\t\t\t<td>&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % '</br>'.join(camel_case_split(item['pretty']))
        html += '\t\t\t\t\t\t<td align="right">%s</td>\n' % format_integer(item['amount'])
        html += '\t\t\t\t\t</tr>\n'

    ############################################################################################################
    # GIFTS OUTSIDE UK

    html += '\t\t\t\t\t<td></br></td>\n'
    html += '\t\t\t\t\t<td></br></td>\n'

    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td class="category"><b>Gifts Outside UK</b></td>\n'
    html += '\t\t\t\t\t\t<td class="category" align="right"><b>%s</b></td>\n' % (gifts_outside_uk_f)    
    html += '\t\t\t\t\t</tr>\n'

    for item in gifts_outside_uk_items:

        html += '\t\t\t\t\t<tr>\n'
        html += '\t\t\t\t\t\t<td>&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:200]
        html += '\t\t\t\t\t\t<td align="right">%s</td>\n' % format_integer(item['amount'])
        html += '\t\t\t\t\t</tr>\n'

    ############################################################################################################
    # DIRECT DONATIONS

    html += '\t\t\t\t\t<td></br></td>\n'
    html += '\t\t\t\t\t<td></br></td>\n'

    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td class="category"><b>Direct Donations</b></td>\n'
    html += '\t\t\t\t\t\t<td class="category" align="right"><b>%s</b></td>\n' % (direct_donations_f)    
    html += '\t\t\t\t\t</tr>\n'

    for item in direct_donations_items:

        html += '\t\t\t\t\t<tr>\n'
        html += '\t\t\t\t\t\t<td>&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:200]
        html += '\t\t\t\t\t\t<td align="right">%s</td>\n' % format_integer(item['amount'])
        html += '\t\t\t\t\t</tr>\n'

    ############################################################################################################
    # DIRECT DONATIONS

    html += '\t\t\t\t\t<td></br></td>\n'
    html += '\t\t\t\t\t<td></br></td>\n'

    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td class="category"><b>Indirect Donations</b></td>\n'
    html += '\t\t\t\t\t\t<td class="category" align="right"><b>%s</b></td>\n' % (indirect_donations_f)    
    html += '\t\t\t\t\t</tr>\n'

    for item in indirect_donations_items:

        html += '\t\t\t\t\t<tr>\n'
        html += '\t\t\t\t\t\t<td>&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:200]
        html += '\t\t\t\t\t\t<td align="right">%s</td>\n' % format_integer(item['amount'])
        html += '\t\t\t\t\t</tr>\n'

    ############################################################################################################
    # VISITS OUTSIDE UK

    html += '\t\t\t\t\t<td></br></td>\n'
    html += '\t\t\t\t\t<td></br></td>\n'

    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td class="category"><b>Overseas Visits</b></td>\n'
    html += '\t\t\t\t\t\t<td class="category" align="right"><b>%s</b></td>\n' % (visits_outside_uk_f)    
    html += '\t\t\t\t\t</tr>\n'

    for item in visits_outside_uk_items:

        html += '\t\t\t\t\t<tr>\n'
        html += '\t\t\t\t\t\t<td>&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:200]
        html += '\t\t\t\t\t\t<td align="right">%s</td>\n' % format_integer(item['amount'])
        html += '\t\t\t\t\t</tr>\n'

    ############################################################################################################
    # TOTAL FREEBIES

    html += '\t\t\t\t\t<td></br></td>\n'
    html += '\t\t\t\t\t<td></br></td>\n'

    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td class="category category_total"><b>Total Freebies</br></td>\n'
    html += '\t\t\t\t\t\t<td class="category category_total" align="right"><b>%s</b></td>\n' % (total_freebies_f)
    html += '\t\t\t\t\t</tr>\n'

    ############################################################################################################
    # SHAREHOLDINGS PERCENT

    html += '\t\t\t\t\t<td></br></td>\n'
    html += '\t\t\t\t\t<td></br></td>\n'

    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td class="category"><b>Shareholdings 15% +</b></td>\n'
    html += '\t\t\t\t\t\t<td class="category" align="right"><b>%s</b></td>\n' % (str(len(shareholdings_percent_items)))
    html += '\t\t\t\t\t</tr>\n'

    for item in shareholdings_percent_items:

        link = item['link']
        link_label = 'Link'
        if link == '':
            link_label = 'Missing'

        html += '\t\t\t\t\t<tr>\n'
        html += '\t\t\t\t\t\t<td>&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['raw_string'][:200]
        html += '\t\t\t\t\t\t<td align="right"><a target="_blank" href="%s"><div style="height:100;width:100">%s</div></a></td>\n' % (link, link_label)
        html += '\t\t\t\t\t</tr>\n'

    ############################################################################################################
    # SHAREHOLDINGS

    html += '\t\t\t\t\t<td></br></td>\n'
    html += '\t\t\t\t\t<td></br></td>\n'

    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td class="category"><b>Shareholdings &#163;70,000 + (Min)</b></td>\n'
    html += '\t\t\t\t\t\t<td class="category" align="right"><b>%s</b></td>\n' % (shareholding_wealth_f)
    html += '\t\t\t\t\t</tr>\n'

    for item in shareholdings_items:

        link = item['link']
        link_label = 'Link'
        if link == '':
            link_label = 'Missing'

        html += '\t\t\t\t\t<tr>\n'
        html += '\t\t\t\t\t\t<td>&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['raw_string'][:200]
        html += '\t\t\t\t\t\t<td align="right"><a target="_blank" href="%s"><div style="height:100;width:100">%s</div></a></td>\n' % (link, link_label)
        html += '\t\t\t\t\t</tr>\n'

    ############################################################################################################
    # PROPERTY

    html += '\t\t\t\t\t<td></br></td>\n'
    html += '\t\t\t\t\t<td></br></td>\n'

    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td class="category"><b>Property (Min)</b></td>\n'
    html += '\t\t\t\t\t\t<td class="category" align="right"><b>%s</b></td>\n' % (property_wealth_f)
    html += '\t\t\t\t\t</tr>\n'

    for item in property_items:

        html += '\t\t\t\t\t<tr>\n'
        html += '\t\t\t\t\t\t<td>&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:200]
        html += '\t\t\t\t\t\t<td align="right">%s</td>\n' % format_integer(item['amount'])
        html += '\t\t\t\t\t</tr>\n'

    ############################################################################################################
    # TOTAL WEALTH

    html += '\t\t\t\t\t<td></br></td>\n'
    html += '\t\t\t\t\t<td></br></td>\n'

    html += '\t\t\t\t\t<tr class="toggle2">\n'
    html += '\t\t\t\t\t\t<td class="category category_total"><b>Total Wealth (Min)</br></td>\n'
    html += '\t\t\t\t\t\t<td class="category category_total" align="right"><b>%s</b></td>\n' % (total_wealth_f)
    html += '\t\t\t\t\t</tr>\n'

    ############################################################################################################
    # Family

    html += '\t\t\t\t\t<td></br></td>\n'
    html += '\t\t\t\t\t<td></br></td>\n'

    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td class="category"><b>Family</b></td>\n'
    html += '\t\t\t\t\t</tr>\n'

    for item in family_items:

        html += '\t\t\t\t\t<tr>\n'
        html += '\t\t\t\t\t\t<td>&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:200]
        html += '\t\t\t\t\t</tr>\n'

    ############################################################################################################
    # FAMILY LOBBYISTS

    html += '\t\t\t\t\t<td></br></td>\n'
    html += '\t\t\t\t\t<td></br></td>\n'

    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td class="category"><b>Family Lobbyists</b></td>\n'
    html += '\t\t\t\t\t</tr>\n'

    for item in family_lobbyists_items:

        html += '\t\t\t\t\t<tr>\n'
        html += '\t\t\t\t\t\t<td>&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:200]
        html += '\t\t\t\t\t</tr>\n'

    ############################################################################################################
    # MISCELLANEOUS

    html += '\t\t\t\t\t<td></br></td>\n'
    html += '\t\t\t\t\t<td></br></td>\n'

    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td class="category"><b>Miscellaneous</b></td>\n'
    html += '\t\t\t\t\t\t<td class="category" align="right"><b>%s</b></td>\n' % (miscellaneous_f)
    html += '\t\t\t\t\t</tr>\n'

    for item in miscellaneous_items:

        html += '\t\t\t\t\t<tr>\n'
        html += '\t\t\t\t\t\t<td>&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:200]
        html += '\t\t\t\t\t\t<td align="right">%s</td>\n' % format_integer(item['amount'])
        html += '\t\t\t\t\t</tr>\n'

    # END TABLE
    html += '\t\t\t\t</table>\n'
    html += '\t\t\t</div>\n'
    html += '\t\t</div>'


    # write it out
    with open(html_file, "a") as myfile2:
        myfile2.write(html.encode("utf8"))