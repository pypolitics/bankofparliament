#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, os

from utils import get_mp_image

images_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'images'))
json_dump_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'json', 'members_dump.json')

def read_json_file():
	"""
	Read file from json_dump_location
	"""
	with open(json_dump_location) as json_data:
		return json.load(json_data)

if __name__ == "__main__":
	"""
	Commandline run
	"""


	# return a list (of dicts) of mps
	mps = read_json_file()

	for mp in mps:
		print 'Downloading : %s' % mp['name']
		get_mp_image(mp['name'], mp['forname'], mp['surname'], mp['member_id'], images_directory)
