#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, locale
locale.setlocale(locale.LC_ALL, '')

def write_thumbnail(html_file, family_pretty, member_id, name, party, party_string, constituency, salary_f, private_income_f, rental_income_f, total_income_f, gifts_f, gifts_outside_uk_f, direct_donations_f, indirect_donations_f, visits_outside_uk_f, total_freebies_f, shareholdings_percent, shareholdings_percent_items, shareholding_wealth_f, active_appointments, property_wealth_f, total_wealth_f,salary, private_income, rental_income, total_income, gifts, gifts_outside_uk, property_wealth, total_wealth, direct_donations, indirect_donations, visits_outside_uk, total_freebies, shareholdings, previous_appointments, family, miscellaneous, miscellaneous_f, miscellaneous_items, family_items, family_lobbyists_items):
    ##############################################################################################################################
    # BUILD THE HTML - THUMBNAIL
    ##############################################################################################################################

    # so the class names on the main thumbnail widget dictate how it can be searched for.
    # lets go for name, party, constituency only

    # we also have to add data attributes for sorting functions

    html = u"\n"
    html += '\t\t<div class="photo col panel %s %s %s %s" data-salary=%s data-privateinc=%s data-rental=%s data-income=%s data-gifts=%s data-gifts_outside_uk=%s data-direct_donations=%s data-indirect_donations=%s data-visits_outside_uk=%s data-freebies=%s data-shareholdings=%s data-shareholdings_percent=%s data-active_appointments=%s data-previous_appointments=%s data-property=%s data-wealth=%s data-member=%s data-miscellaneous=%s data-family=%s data-lobbyists=%s>\n' % (name.lower(), party_string.lower(), constituency.lower(), str(member_id), int(salary), int(private_income), int(rental_income), int(total_income), int(gifts), int(gifts_outside_uk), int(direct_donations), int(indirect_donations), int(visits_outside_uk), int(total_freebies), int(shareholdings), int(shareholdings_percent), int(len(active_appointments)), int(len(previous_appointments)), int(property_wealth), int(total_wealth), str(member_id), int(miscellaneous), int(len(family_items)), int(len(family_lobbyists_items)))
    html += '\t\t\t<div class="panelHeader">\n'

    if family:
        html += '\t\t\t\t<img class="family" src="lib/images/family.png" title="%s" height="32" width="32" align="right"></img></br>\n' % family_pretty
    else:
        html += '\t\t\t\t<img class="nofamily" src="lib/images/placeholder.png" height="32" width="32" align="right"></img></br>\n'
    html += '\t\t\t\t<p></p>\n'

    # add the clickable thumbnail
    html += '<a href="pages/register/%s.html">' % member_id

    s = os.path.join(os.path.dirname(__file__), '..', 'lib', 'images', '%s.jpg' % str(member_id))

    if os.path.exists(s):
        html += '\t\t\t\t<img class="picture" src="lib/images/%s.jpg" height="128" width="128" align="right=middle"></img>\n' % (str(member_id))
    else:
        html += '\t\t\t\t<img src="lib/images/photo.png" height="128" width="128" align="right=middle"></img>\n'
 
    html += '</a>'

    # add the mp text
    html += '\t\t\t\t<p class="name">%s</p>\n' % (name)
    html += '\t\t\t\t<p class="party">%s</p>\n' % (party.title())
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
    html += '\t\t\t\t\t\t<td class="toggle" align="right" style="display: none">%s</td>\n' % (str(len(shareholdings_percent_items)))
    html += '\t\t\t\t\t</tr>\n'

    html += '\t\t\t\t\t<tr class="toggle" style="display: none">\n'
    html += '\t\t\t\t\t\t<td class="toggle" style="display: none">Shareholdings &#163;70,000 + (Min)</td>\n'
    html += '\t\t\t\t\t\t<td class="toggle" align="right" style="display: none">%s</td>\n' % (shareholding_wealth_f)
    html += '\t\t\t\t\t</tr>\n'

    html += '\t\t\t\t\t<tr class="toggle" style="display: none">\n'
    html += '\t\t\t\t\t\t<td class="toggle" style="display: none">Companies House Appointments</td>\n'
    html += '\t\t\t\t\t\t<td class="toggle" align="right" style="display: none">%s</td>\n' % (len(active_appointments))
    html += '\t\t\t\t\t</tr>\n'

    html += '\t\t\t\t\t<tr class="toggle" style="display: none">\n'
    html += '\t\t\t\t\t\t<td class="toggle" style="display: none">Property (Min)</td>\n'
    html += '\t\t\t\t\t\t<td class="toggle" align="right" style="display: none">%s</td>\n' % (property_wealth_f)
    html += '\t\t\t\t\t</tr>\n'

    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td><b>Total Wealth (Min)</b></td>\n'
    html += '\t\t\t\t\t\t<td align="right"><b>%s</b></td>\n' % (total_wealth_f)
    html += '\t\t\t\t\t</tr>\n'

    html += '\t\t\t\t\t<td class="toggle" style="display: none"><br/></td>\n'

    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td class="toggle" style="display: none">Miscellaneous</td>\n'
    html += '\t\t\t\t\t\t<td class="toggle" align="right" style="display: none">%s</td>\n' % (miscellaneous_f)
    html += '\t\t\t\t\t</tr>\n'

    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td class="toggle" style="display: none">Family</td>\n'
    html += '\t\t\t\t\t\t<td class="toggle" align="right" style="display: none">%s</td>\n' % (str(len(family_items)))
    html += '\t\t\t\t\t</tr>\n'

    html += '\t\t\t\t\t<tr>\n'
    html += '\t\t\t\t\t\t<td class="toggle" style="display: none">Family Lobbyists</td>\n'
    html += '\t\t\t\t\t\t<td class="toggle" align="right" style="display: none">%s</td>\n' % (str(len(family_lobbyists_items)))
    html += '\t\t\t\t\t</tr>\n'

    html += '\t\t\t\t</table>\n'

    html += '\t\t\t</div>\n'
    html += '\t\t</div>\n'

    # write it out
    with open(html_file, "a") as myfile:
        myfile.write(html.encode("utf8"))