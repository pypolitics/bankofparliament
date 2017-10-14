#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, os, sys
from optparse import OptionParser
sys.path.append('../lib/python')

from utils import write_scatter_plot, read_json_file

if __name__ == "__main__":
    """Commandline run"""
    parser = OptionParser()

    # parser.add_option("--summary", help="Summary print", action="store_true", default=True)
    # parser.add_option("--detailed", help="Detailed print", action="store_true", default=False)
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
        write_scatter_plot(mp)
