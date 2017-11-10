#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, locale, re
locale.setlocale(locale.LC_ALL, '')

def write_thumbnail(html_file, family_pretty, member_id, name, party, party_string, constituency, salary_f, private_income_f, rental_income_f, total_income_f, gifts_f, gifts_outside_uk_f, direct_donations_f, indirect_donations_f, visits_outside_uk_f, total_freebies_f, shareholdings_percent, shareholdings_percent_items, shareholding_wealth_f, active_appointments, property_wealth_f, total_wealth_f,salary, private_income, rental_income, total_income, gifts, gifts_outside_uk, property_wealth, total_wealth, direct_donations, indirect_donations, visits_outside_uk, total_freebies, shareholdings, previous_appointments, family, miscellaneous, miscellaneous_f, miscellaneous_items, family_items, family_lobbyists_items, twitter, gender, scatter_div):
    s = os.path.join(os.path.dirname(__file__), '..', 'lib', 'data', 'images', '%s.jpg' % str(member_id))
    if gender == 'M':
        gender = 'male'
    else:
        gender = 'female'

    html = u"\n"
    html += '\t\t<div class="thumbnail_widget _%s %s %s %s" data-salary=%s data-privateinc=%s data-rental=%s data-income=%s data-gifts=%s data-gifts_outside_uk=%s data-direct_donations=%s data-indirect_donations=%s data-visits_outside_uk=%s data-freebies=%s data-shareholdings=%s data-shareholdings_percent=%s data-active_appointments=%s data-previous_appointments=%s data-property=%s data-wealth=%s data-member=%s data-miscellaneous=%s data-family=%s data-lobbyists=%s>\n' % (name.lower(), party_string.lower(), constituency.lower(), str(member_id), int(salary), int(private_income), int(rental_income), int(total_income), int(gifts), int(gifts_outside_uk), int(direct_donations), int(indirect_donations), int(visits_outside_uk), int(total_freebies), int(shareholdings), int(shareholdings_percent), int(len(active_appointments)), int(len(previous_appointments)), int(property_wealth), int(total_wealth), str(member_id), int(miscellaneous), int(len(family_items)), int(len(family_lobbyists_items)))    

    if os.path.exists(s):
        html += '\t\t\t<a title="%s" href="javascript:void(0)"><img class="thumbnail_picture %s" data-memberid=%s src="lib/data/images/%s.jpg" border="0"></a>\n' % (name.title(), party_string.lower(), member_id, member_id)
    else:
        html += '\t\t\t<a title="%s" href="javascript:void(0)"><img class="thumbnail_picture %s" data-memberid=%s src="lib/data/images/%s.png" border="0"></a>\n' % (name.title(), party_string.lower(), member_id, gender)

    html += '\t\t\t<p class="thumbnail_label">%s</p>\n' % name.title()
    html += '\t\t\t<div class="thumbnail_tooltip" style="display:none">%s, %s\n' % (party.title(), constituency.title())
    html += '\t\t\t</div>\n'
    html += '\t\t</div>\n'

    html += '\t\t<div id="%s" style="height: 619px; width: 1100px;" class="plotly-graph-div" href="javascript:void(0)" onclick="document.getElementById(\'%s\').style.display=\'none\';document.getElementById(\'fade\').style.display=\'none\'">\n' % (member_id, member_id)
    html += '\t\t</div>\n'
    html += '\t\t<div id="fade" class="black_overlay"></div>\n'

    # write it out
    with open(html_file, "a") as myfile:
        myfile.write(html.encode("utf8"))
