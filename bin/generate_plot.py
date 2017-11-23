#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, os, sys
from optparse import OptionParser
sys.path.append('../lib/python')
lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lib')

from utils import write_scatter_plot, read_json_file, read_expenses, match_expenses

expenses_data_paths = {
            # '2017-2018' : '../lib/data/export_17_18.csv',
            '2016-2017' : '../lib/data/export_16_17.csv'
            }

expenses_data = read_expenses(expenses_data_paths)

if __name__ == "__main__":
    """Commandline run"""
    parser = OptionParser()
    parser.add_option("--sortby", help="Sort By",
                      action="store", default='income')

    # parse the comand line
    (options, args) = parser.parse_args()    
    # return a list (of dicts) of mps
    mps = read_json_file()

    # TODO: fix this crude arg porser
    if args:
        searched = []
        for member in args:
            for i in mps:
                if member.lower() in i['name'].lower():
                    searched.append(i)
                if member.lower() in i['party'].lower():
                    searched.append(i)
                if member.lower() in i['constituency'].lower():
                    searched.append(i)

        mps = searched

    for mp in mps:
        print '\nProcessing Plot : %s' % mp['name']
        plot_file = os.path.join(lib_path, 'data', 'plots', '%s.json' % mp['member_id'])

        # add expenses
        for year in expenses_data.keys():
            mp['expenses'] = match_expenses(mp, year, expenses_data)

        write_scatter_plot(mp, plot_file)
