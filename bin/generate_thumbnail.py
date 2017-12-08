#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, locale, re
locale.setlocale(locale.LC_ALL, '')

def write_thumbnail(html_file, total_expenses, total_expenses_f, family_pretty, member_id, name, party, party_string, constituency, salary_f, private_income_f, rental_income_f, total_income_f, gifts_f, gifts_outside_uk_f, direct_donations_f, indirect_donations_f, visits_outside_uk_f, total_freebies_f, shareholdings_percent, shareholdings_percent_items, shareholding_wealth_f, active_appointments, property_wealth_f, total_wealth_f,salary, private_income, rental_income, total_income, gifts, gifts_outside_uk, property_wealth, total_wealth, direct_donations, indirect_donations, visits_outside_uk, total_freebies, shareholdings, previous_appointments, family, miscellaneous, miscellaneous_f, miscellaneous_items, family_items, family_lobbyists_items, companies_house, twitter, gender):

    s = os.path.join(os.path.dirname(__file__), '..', 'lib', 'data', 'images', '%s.jpg' % (str(member_id)))
    if not os.path.exists(s):
        if gender == 'M':
            photo = 'male.png'
        else:
            photo = 'female.png'
    else:
        photo = '%s.jpg' % member_id

    party = party.replace('/', '-')

    html = '\n'
    html += '\t\t<div class="element-item thumbnail_widget _%s _%s _%s" data-salary=%s data-privateinc=%s data-rental=%s data-income=%s data-gifts=%s data-gifts_outside=%s data-direct=%s data-indirect=%s data-visits=%s data-freebies=%s data-shareholdings=%s data-shareholdings_percent=%s data-property=%s data-wealth=%s data-misc=%s data-family=%s data-lobbyists=%s data-expenses=%s data-companies_house=%s data-member=%s>\n' % (name.lower(), party_string.lower(), constituency.lower(), int(salary), int(private_income), int(rental_income), int(total_income), int(gifts), int(gifts_outside_uk), int(direct_donations), int(indirect_donations), int(visits_outside_uk), int(total_freebies), int(shareholdings), int(shareholdings_percent), int(property_wealth), int(total_wealth), int(miscellaneous), int(len(family_items)), int(len(family_lobbyists_items)), int(total_expenses), len(companies_house), member_id)
    html += '\t\t\t<a>\n'
    html += '\t\t\t\t<h2 class="thumbnail_detail %s" data-memberid=%s>\n' % (party.lower(), member_id)
    html += '\t\t\t\t<b>Income</b>\n'
    html += '\t\t\t\t</br>%s</br>\n' % total_income_f
    html += '\t\t\t\t<b>Freeblies</b>\n'
    html += '\t\t\t\t</br>%s</br>\n' % total_freebies_f
    html += '\t\t\t\t\t<b>Wealth</b>\n'
    html += '\t\t\t\t\t</br>%s</br>\n' % total_wealth_f
    html += '\t\t\t\t\t<b>Expenses</b>\n'
    html += '\t\t\t\t\t</br>%s</br>\n' % total_expenses_f
    html += '\t\t\t\t</h2>\n'
    html += '\t\t\t\t<img src="lib/data/images/%s" class="img-responsive %s data-memberid=%s" style="width:100' % (photo, party.lower(), member_id) + r'%' + '; border-radius:50' + r'%' + '" alt="Image">\n'
    html += '\t\t\t</a>\n'
    html += '\t\t\t<p class="thumbnail_label">%s</p>\n' % name.title()
    html += '\t\t</div>\n'


    # write it out
    with open(html_file, "a") as myfile:
        myfile.write(html.encode("utf8"))
