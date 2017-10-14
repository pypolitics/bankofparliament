#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, os, sys
sys.path.append('../lib/python')

from utils import write_word_cloud, read_json_file

wordcloud_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib', 'data', 'wordclouds'))

if __name__ == "__main__":
    """Commandline run"""
    # return a list (of dicts) of mps
    mps = read_json_file()
    for mp in mps:
        print '\nProcessing Wordcloud : %s' % mp['name']
        write_word_cloud(words=mp['keywords'], member_id=mp['member_id'], filepath=os.path.join(wordcloud_directory, '%s.png' % mp['member_id']))
