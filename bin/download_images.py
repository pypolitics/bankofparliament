#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, os, sys

sys.path.append('../lib/python')

from utils import get_mp_image

images_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib', 'data', 'images'))

def read_json_file():
    """
    Read file from json_dump_location
    """
    json_dump_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lib', 'data', 'members')
    data = []
    for mp in os.listdir(json_dump_location):
        f = os.path.join(json_dump_location, mp)
        with open(f) as json_data:
            data.append(json.load(json_data))

    return data

if __name__ == "__main__":
	"""
	Commandline run
	"""


	# return a list (of dicts) of mps
	mps = read_json_file()

	for mp in mps:
		print 'Downloading : %s' % mp['name']
		get_mp_image(mp['name'], mp['forname'], mp['surname'], mp['member_id'], images_directory)
