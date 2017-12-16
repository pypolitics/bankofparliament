#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, os, sys, time
from optparse import OptionParser
sys.path.append('../lib/python')
lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lib')

from utils import read_json_file, read_expenses, match_expenses

from register_plot import write_register_plot
from shareholdings_plot import write_shareholder_plot

expenses_data_paths = {
            # '2017-2018' : '../lib/data/export_17_18.csv',
            '2016-2017' : '../lib/data/export_16_17.csv'
            }

expenses_data = read_expenses(expenses_data_paths)

if __name__ == "__main__":
    """Commandline run"""
    parser = OptionParser()
    parser.add_option("--sortby", help="Sort By", action="store", default='income')
    parser.add_option("--from_index", help="Carry on from index", action="store", default=0)

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

    if options.from_index:
        # index the list from a given int
        mps = mps[int(options.from_index):]

    for mp in mps:
        start_time = time.time()
        print '\nProcessing Plot : %s' % mp['name']
        plot_file = os.path.join(lib_path, 'data', 'plots', '%s.json' % mp['member_id'])
        shareholdings_file = os.path.join(lib_path, 'data', 'plots', 'shareholdings', '%s.json' % mp['member_id'])

        # add expenses
        for year in expenses_data.keys():
            mp['expenses'] = match_expenses(mp, year, expenses_data)

        write_register_plot(mp, plot_file)
        write_shareholder_plot(mp, shareholdings_file)

        end_time = time.time()
        elapsed = end_time - start_time

        index = mps.index(mp)
        index = str(index+1).zfill(3)
        print '%s - %s (%s) %s - %s seconds' % (index, mp['name'], mp['party'], mp['constituency'], int(elapsed))
