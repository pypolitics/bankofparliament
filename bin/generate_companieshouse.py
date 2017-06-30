#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, locale, pprint

locale.setlocale(locale.LC_ALL, '')

companies_house_base_url = 'https://beta.companieshouse.gov.uk'

def format_integer(number):

    loc = locale.currency(number, grouping=True).split('.')[0]
    return loc.replace("£", "&#163;")

def write_companieshouse(html_file, name, party, party_dict, constituency, member_id, active_appointments, previous_appointments):
    # -------------------------------------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------------------------------

    # mp_html_file = os.path.join(os.path.dirname(__file__), '../pages/%s.html' % member_id)
    html = u"\n"

    ###########################################################################################################
    # EXPANDED

    # BUILD THE HTML
    html += '\t\t<div class="photo col2 bigWidget panel2 %s %s %s %s %s">\n' % (name.lower(), party.lower(), party_dict[party.lower()], constituency.lower(), str(member_id))
    html += '\t\t\t<div class="panelHeader photo data-member=%s">\n' % (str(member_id))
    # html += '\t\t\t<img class="xxx data-member=%s" src="../lib/data/wordclouds/%s.png" height="200" width="1040\n' % (str(member_id), str(member_id)) 
    # add the thumbnail
    s = os.path.join(os.path.dirname(__file__), '..', 'lib', 'images', '%s.jpg' % str(member_id))
    if os.path.exists(s):
        html += '\t\t\t\t<img class="picture" src="../../lib/images/%s.jpg" height="128" width="128" align="right=middle"></img>\n' % (str(member_id))
        # html += '\t\t\t\t<img class="picture" src="../lib/data/wordclouds/%s.png" height="200" width="800" align="right=middle"></img>\n' % (str(member_id))

    else:
        html += '\t\t\t\t<img src="../../lib/images/photo.png" height="128" width="128" align="right=middle"></img>\n'

    html += '\t\t\t\t%s, %s, %s\n' % (name, party, constituency)
    html += '\t\t\t</div>\n'
    html += '\t\t\t<div class="panelBody">\n'
    html += '\t\t\t\t<table class="myTable3 " style="width: 92%;">\n'

    ############################################################################################################
    # ACTIVE

    html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    html += '\t\t\t\t\t\t<td class="toggle2 income bigger"><b>Active Appointments</b></td>\n'
    # html += '\t\t\t\t\t\t<td class="toggle2 income" align="right"><b>%s</b></td>\n' % (a)
    html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    for item in active_appointments:
        # pprint.pprint(item)
        link = '%s%s' % (companies_house_base_url, item['appointment']['company']['links']['self'])

        html += '\t\t\t\t\t<tr class="toggle2 income">\n'
        html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['appointment']['company']['company_name'][:125].title()

        html += '\t\t\t\t\t\t<td>\n'
        html += '\t\t\t\t\t\t\t<a target="_blank" href="%s">\n' % (link)
        html += '\t\t\t\t\t\t\t\t<div style="height:100%;width:100%">'
        html += '\t\t\t\t\t\t\t\t\tLink\n'
        html += '\t\t\t\t\t\t\t\t</div>'
        html += '\t\t\t\t\t\t\t</a>\n'
        html += '\t\t\t\t\t\t</td>\n'

        # html += '\t\t\t\t\t\t<td href="%s%s" target="_blank" class="toggle2 income" align="right">Link</td>\n' % (companies_house_base_url, item['appointment']['company']['links']['self'])
        html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    ############################################################################################################
    # HISTORIC

    html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'
    html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'

    html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    html += '\t\t\t\t\t\t<td class="toggle2 income bigger"><b>Historic Appointments</b></td>\n'
    # html += '\t\t\t\t\t\t<td class="toggle2 income" align="right"><b>%s</b></td>\n' % (a)
    html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    for item in previous_appointments:

        try:
            self = item['appointment']['company']['links']['self']
        except:
            self = '/'

        try:
            name = item['appointment']['company']['company_name']
        except:
            name = ''

        link = '%s%s' % (companies_house_base_url, self)

        html += '\t\t\t\t\t<tr class="toggle2 income">\n'
        html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % name[:125].title()

        html += '\t\t\t\t\t\t<td>\n'
        html += '\t\t\t\t\t\t\t<a target="_blank" href="%s">\n' % (link)
        html += '\t\t\t\t\t\t\t\t<div style="height:100%;width:100%">'
        html += '\t\t\t\t\t\t\t\t\tLink\n'
        html += '\t\t\t\t\t\t\t\t</div>'
        html += '\t\t\t\t\t\t\t</a>\n'
        html += '\t\t\t\t\t\t</td>\n'

        # html += '\t\t\t\t\t\t<td href="%s%s" target="_blank" class="toggle2 income" align="right">Link</td>\n' % (companies_house_base_url, item['appointment']['company']['links']['self'])
        html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    # ############################################################################################################
    # # RENTAL INCOME

    # html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'
    # html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'
    
    # html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    # html += '\t\t\t\t\t\t<td class="toggle2 income bigger"><b>Rental Income</b></td>\n'
    # html += '\t\t\t\t\t\t<td class="toggle2 income" align="right"><b>%s</b></td>\n' % (rental_income_f)
    # html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    # for item in rental_items:

    #     html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    #     html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:125]
    #     html += '\t\t\t\t\t\t<td class="toggle2 income" align="right">%s</td>\n' % format_integer(item['amount'])
    #     html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    # ############################################################################################################
    # # TOTAL INCOME

    # html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'
    # html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'

    # html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    # html += '\t\t\t\t\t\t<td class="toggle2total toggle2 income bigger"><b>Total Income (Min)</br></td>\n'
    # html += '\t\t\t\t\t\t<td class="toggle2total toggle2 income" align="right"><b>%s</b></td>\n' % (total_income_f)
    # html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    # ############################################################################################################
    # # GIFTS

    # html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'
    # html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'

    # html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    # html += '\t\t\t\t\t\t<td class="toggle2 income bigger"><b>Gifts</b></td>\n'
    # html += '\t\t\t\t\t\t<td class="toggle2 income" align="right"><b>%s</b></td>\n' % (gifts_f)
    # html += '\t\t\t\t\t</tr>\n'

    # for item in gifts_items:

    #     html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    #     html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:125]
    #     html += '\t\t\t\t\t\t<td class="toggle2 income" align="right">%s</td>\n' % format_integer(item['amount'])
    #     html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    # ############################################################################################################
    # # GIFTS OUTSIDE UK

    # html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'
    # html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'

    # html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    # html += '\t\t\t\t\t\t<td class="toggle2 income bigger"><b>Gifts Outside UK</b></td>\n'
    # html += '\t\t\t\t\t\t<td class="toggle2 income" align="right"><b>%s</b></td>\n' % (gifts_outside_uk_f)    
    # html += '\t\t\t\t\t</tr>\n'

    # for item in gifts_outside_uk_items:

    #     html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    #     html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:125]
    #     html += '\t\t\t\t\t\t<td class="toggle2 income" align="right">%s</td>\n' % format_integer(item['amount'])
    #     html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    # ############################################################################################################
    # # DIRECT DONATIONS

    # html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'
    # html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'

    # html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    # html += '\t\t\t\t\t\t<td class="toggle2 income bigger"><b>Direct Donations</b></td>\n'
    # html += '\t\t\t\t\t\t<td class="toggle2 income" align="right"><b>%s</b></td>\n' % (direct_donations_f)    
    # html += '\t\t\t\t\t</tr>\n'

    # for item in direct_donations_items:

    #     html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    #     html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:125]
    #     html += '\t\t\t\t\t\t<td class="toggle2 income" align="right">%s</td>\n' % format_integer(item['amount'])
    #     html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    # ############################################################################################################
    # # DIRECT DONATIONS

    # html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'
    # html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'

    # html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    # html += '\t\t\t\t\t\t<td class="toggle2 income bigger"><b>Indirect Donations</b></td>\n'
    # html += '\t\t\t\t\t\t<td class="toggle2 income" align="right"><b>%s</b></td>\n' % (indirect_donations_f)    
    # html += '\t\t\t\t\t</tr>\n'

    # for item in indirect_donations_items:

    #     html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    #     html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:125]
    #     html += '\t\t\t\t\t\t<td class="toggle2 income" align="right">%s</td>\n' % format_integer(item['amount'])
    #     html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    # ############################################################################################################
    # # VISITS OUTSIDE UK

    # html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'
    # html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'

    # html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    # html += '\t\t\t\t\t\t<td class="toggle2 income bigger"><b>Overseas Visits</b></td>\n'
    # html += '\t\t\t\t\t\t<td class="toggle2 income" align="right"><b>%s</b></td>\n' % (visits_outside_uk_f)    
    # html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    # for item in visits_outside_uk_items:

    #     html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    #     html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:125]
    #     html += '\t\t\t\t\t\t<td class="toggle2 income" align="right">%s</td>\n' % format_integer(item['amount'])
    #     html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    # ############################################################################################################
    # # TOTAL FREEBIES

    # html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'
    # html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'

    # html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    # html += '\t\t\t\t\t\t<td class="toggle2total income bigger"><b>Total Freebies</br></td>\n'
    # html += '\t\t\t\t\t\t<td class="toggle2total income" align="right"><b>%s</b></td>\n' % (total_freebies_f)
    # html += '\t\t\t\t\t</tr>\n'

    # ############################################################################################################
    # # SHAREHOLDINGS PERCENT

    # html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'
    # html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'

    # html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    # html += '\t\t\t\t\t\t<td class="toggle2 income bigger"><b>Shareholdings 15% +</b></td>\n'
    # html += '\t\t\t\t\t\t<td class="toggle2 income" align="right"><b>%s</b></td>\n' % (str(len(shareholdings_percent_items)))
    # html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    # for item in shareholdings_percent_items:

    #     html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    #     html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['raw_string'][:125]
    #     html += '\t\t\t\t\t\t<td class="toggle2 income" align="right">%s</td>\n' % (str(item['amount']) + '%')
    #     html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    # ############################################################################################################
    # # SHAREHOLDINGS

    # html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'
    # html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'

    # html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    # html += '\t\t\t\t\t\t<td class="toggle2 income bigger"><b>Shareholdings &#163;70,000 + (Min)</b></td>\n'
    # html += '\t\t\t\t\t\t<td class="toggle2 income" align="right"><b>%s</b></td>\n' % (shareholding_wealth_f)
    # html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    # for item in shareholdings_items:

    #     html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    #     html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['raw_string'][:125]
    #     html += '\t\t\t\t\t\t<td class="toggle2 income" align="right">%s</td>\n' % format_integer(item['amount'])
    #     html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    # ############################################################################################################
    # # PROPERTY

    # html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'
    # html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'

    # html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    # html += '\t\t\t\t\t\t<td class="toggle2 income bigger"><b>Property (Min)</b></td>\n'
    # html += '\t\t\t\t\t\t<td class="toggle2 income" align="right"><b>%s</b></td>\n' % (property_wealth_f)
    # html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    # for item in property_items:

    #     html += '\t\t\t\t\t<tr class="toggle2 income">\n'
    #     html += '\t\t\t\t\t\t<td class="toggle2 income">&nbsp&nbsp&nbsp&nbsp - %s</td>\n' % item['pretty'][:125]
    #     html += '\t\t\t\t\t\t<td class="toggle2 income" align="right">%s</td>\n' % format_integer(item['amount'])
    #     html += '\t\t\t\t\t</tr class="toggle2 income">\n'

    # ############################################################################################################
    # # TOTAL WEALTH

    # html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'
    # html += '\t\t\t\t\t<td class="toggle2 income"></br></td>\n'

    # html += '\t\t\t\t\t<tr class="toggle2">\n'
    # html += '\t\t\t\t\t\t<td class="toggle2total income bigger"><b>Total Wealth (Min)</br></td>\n'
    # html += '\t\t\t\t\t\t<td class="toggle2total income" align="right"><b>%s</b></td>\n' % (total_wealth_f)
    # html += '\t\t\t\t\t</tr>\n'


    # # END TABLE
    # html += '\t\t\t\t</table>\n'
    # html += '\t\t\t</div>\n'
    # html += '\t\t</div>'


    # write it out
    with open(html_file, "a") as myfile2:
        myfile2.write(html.encode("utf8"))