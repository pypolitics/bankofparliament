#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, locale
locale.setlocale(locale.LC_ALL, '')

def format_integer(number):

    loc = locale.currency(number, grouping=True).split('.')[0]
    return loc.replace("£", "&#163;")

def write_register(html_file, family_pretty, member_id, name, party, constituency, salary_f, private_income_f, rental_income_f, total_income_f, gifts_f, gifts_outside_uk_f, direct_donations_f, indirect_donations_f, visits_outside_uk_f, total_freebies_f, shareholdings_percent, shareholding_wealth_f, active_appointments, property_wealth_f, total_wealth_f, party_dict, salary, private_income, rental_income, total_income, gifts, gifts_outside_uk, property_wealth, total_wealth, direct_donations, indirect_donations, visits_outside_uk, total_freebies, shareholdings, previous_appointments, family, salary_items, private_items, rental_items, gifts_items, gifts_outside_uk_items, direct_donations_items, indirect_donations_items, visits_outside_uk_items, shareholdings_items, shareholdings_percent_items, property_items):

    html = u"\n"
    html += '\t\t<div class="photo col2 bigWidget panel2 %s %s %s %s %s" data-salary=%s data-privateinc=%s data-rental=%s data-income=%s data-gifts=%s data-gifts_outside_uk=%s data-direct_donations=%s data-indirect_donations=%s data-visits_outside_uk=%s data-freebies=%s data-shareholdings=%s data-shareholdings_percent=%s data-property=%s data-wealth=%s data-member=%s>\n' % (name.lower(), party.lower(), party_dict[party.lower()], constituency.lower(), str(member_id), int(salary), int(private_income), int(rental_income), int(total_income), int(gifts), int(gifts_outside_uk), int(direct_donations), int(indirect_donations), int(visits_outside_uk), int(total_freebies), int(shareholdings), int(shareholdings_percent), int(property_wealth), int(total_wealth), str(member_id))
    html += '\t\t\t<div class="panelHeader photo data-member=%s">\n' % (str(member_id))
    
    # add the thumbnail
    s = os.path.join(os.path.dirname(__file__), '..', 'lib', 'images', '%s.jpg' % str(member_id))
    if os.path.exists(s):
        html += '\t\t\t\t<img class="picture" src="../../lib/images/%s.jpg" height="128" width="128" align="right=middle"></img>\n' % (str(member_id))
    else:
        html += '\t\t\t\t<img src="../../lib/images/photo.png" height="128" width="128" align="right=middle"></img>\n'

    # add the mp text
    html += '\t\t\t\t%s, %s, %s\n' % (name, party, constituency)
    html += '\t\t\t</div>\n'
    html += '\t\t\t<div class="panelBody">\n'
    html += '\t\t\t\t<table class="myTable3 " style="width: 92%;">\n'

    ############################################################################################################
    # PUBLIC SALARY

    html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    html += '\t\t\t\t\t\t<td class="toggle2 income bigger"><b>Public Salary</b></td>\n'
    html += '\t\t\t\t\t\t<td class="toggle2 income" align="right"><b>%s</b></td>\n' % (salary_f)
    html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    for item in salary_items:

        html += '\t\t\t\t\t<tr class="toggle2 income">\n'
        html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:125]
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
        html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:125]
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
        html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:125]
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
        html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:125]
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
        html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:125]
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
        html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:125]
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
        html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:125]
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
        html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:125]
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
    html += '\t\t\t\t\t\t<td class="toggle2 income" align="right"><b>%s</b></td>\n' % (str(len(shareholdings_percent_items)))
    html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    for item in shareholdings_percent_items:

        html += '\t\t\t\t\t<tr class="toggle2 income">\n'
        html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['raw_string'][:125]
        html += '\t\t\t\t\t\t<td class="toggle2 income" align="right">%s</td>\n' % (str(item['amount']) + '%')
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
        html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['raw_string'][:125]
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
        html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:125]
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


    # write it out
    with open(html_file, "a") as myfile2:
        myfile2.write(html.encode("utf8"))