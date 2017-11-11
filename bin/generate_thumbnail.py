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
    html += '\t\t<!-- %s -->\n' % (100*'*')
    html += '\t\t<!-- thumbnail widget -->\n'
    html += '\t\t<div class="thumbnail_widget _%s %s %s %s" data-salary=%s data-privateinc=%s data-rental=%s data-income=%s data-gifts=%s data-gifts_outside_uk=%s data-direct_donations=%s data-indirect_donations=%s data-visits_outside_uk=%s data-freebies=%s data-shareholdings=%s data-shareholdings_percent=%s data-active_appointments=%s data-previous_appointments=%s data-property=%s data-wealth=%s data-member=%s data-miscellaneous=%s data-family=%s data-lobbyists=%s>\n' % (name.lower(), party_string.lower(), constituency.lower(), str(member_id), int(salary), int(private_income), int(rental_income), int(total_income), int(gifts), int(gifts_outside_uk), int(direct_donations), int(indirect_donations), int(visits_outside_uk), int(total_freebies), int(shareholdings), int(shareholdings_percent), int(len(active_appointments)), int(len(previous_appointments)), int(property_wealth), int(total_wealth), str(member_id), int(miscellaneous), int(len(family_items)), int(len(family_lobbyists_items)))    
    html += '\n'
    html += '\t\t\t<!-- photo and rollover and label -->\n'
    html += '\t\t\t<a>\n'
    html += '\t\t\t\t<h2 class="thumbnail_detail %s" data-memberid=%s><b>Income</b></br>%s</br><b>Freebies</b></br>%s</br><b>Wealth</b></br>%s</h2>\n' % (party.lower(), member_id, total_income_f, total_freebies_f, total_wealth_f)
    html += '\t\t\t\t<img class="thumbnail_picture %s" data-memberid=%s src="lib/data/images/%s" border="0"></a>\n' % (party.lower(), member_id, photo)
    html += '\t\t\t</a>\n'
    html += '\t\t\t<p class="thumbnail_label">%s</p>\n' % name.title()
    html += '\t\t</div>\n'
    html += '\n'
    html += '\t\t<!-- plotly div -->\n'
    html += '\t\t<div id=%s style="height: 619px; width: 1100px;" class="plotly-graph-div" data-memberid=%s><a class="close" data-memberid=%s>Close<a></div>\n' % (member_id, member_id, member_id)
    html += '\t\t<div id="fade" class="black_overlay"></div>\n'

    # write it out
    with open(html_file, "a") as myfile:
        myfile.write(html.encode("utf8"))
