#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, locale, re
locale.setlocale(locale.LC_ALL, '')

def write_thumbnail(html_file, family_pretty, member_id, name, party, party_string, constituency, salary_f, private_income_f, rental_income_f, total_income_f, gifts_f, gifts_outside_uk_f, direct_donations_f, indirect_donations_f, visits_outside_uk_f, total_freebies_f, shareholdings_percent, shareholdings_percent_items, shareholding_wealth_f, active_appointments, property_wealth_f, total_wealth_f,salary, private_income, rental_income, total_income, gifts, gifts_outside_uk, property_wealth, total_wealth, direct_donations, indirect_donations, visits_outside_uk, total_freebies, shareholdings, previous_appointments, family, miscellaneous, miscellaneous_f, miscellaneous_items, family_items, family_lobbyists_items, twitter, gender, scatter_div):

    s = os.path.join(os.path.dirname(__file__), '..', 'lib', 'data', 'images', '%s.jpg' % (str(member_id)))
    if not os.path.exists(s):
        if gender == 'M':
            photo = 'male.png'
        else:
            photo = 'female.png'
    else:
        photo = '%s.jpg' % member_id

    # html block
    html = '\n'
    html += '\t\t<div class="thumbnail_widget _%s %s %s" data-income=%s data-freebies=%s data-wealth=%s data-member=%s>\n' % (name.lower(), party_string.lower(), constituency.lower(), int(total_income), int(total_freebies), int(total_wealth), member_id)
    html += '\n'
    html += '\t\t\t<a>\n'
    html += '\t\t\t\t<h2 class="thumbnail_detail %s" data-memberid=%s><b>Income</b></br>%s</br><b>Freebies</b></br>%s</br><b>Wealth</b></br>%s</h2>\n' % (party.lower(), member_id, total_income_f, total_freebies_f, total_wealth_f)
    html += '\t\t\t\t<img class="thumbnail_picture %s" data-memberid=%s src="lib/data/images/%s" border="0"></a>\n' % (party.lower(), member_id, photo)
    html += '\t\t\t</a>\n'
    html += '\t\t\t<p class="thumbnail_label">%s</p>\n' % name.title()
    html += '\n'
    html += '\t\t\t<p id=%s style="height: 619px; width: 1100px;" class="plotly-graph-div" data-memberid=%s><a class="close" data-memberid=%s>Close</a></p>\n' % (member_id, member_id, member_id)
    html += '\t\t</div>\n'

    # write it out
    with open(html_file, "a") as myfile:
        myfile.write(html.encode("utf8"))
