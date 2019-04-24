#!/usr/bin/env python

# sys libs
import os
import sys
from optparse import OptionParser
sys.path.append('../lib')

# 3rd party libs
from py2neo import Graph, Node, Relationship
from bs4 import BeautifulSoup

# local libs
from utils import get_all_mps, get_member_info

# api keys
sys.path.append(os.path.abspath(os.path.expanduser('~/.apikeys')))
from apikeys import companies_house_user, theyworkyou_apikey

# NEO4J_URI=bolt://54.226.6.209:39188
# NEO4J_USER=neo4j
# NEO4J_PASSWORD=divers-ore-servos

def get_graph():
	graph = Graph(host='54.226.6.209', bolt_port=39188, http_port=39189, password='divers-ore-servos')
	return graph

def encode_utf8(name):
	return name.decode('latin-1').encode("utf-8")

def main(mps):

	for mp in mps:
		info = get_member_info(theyworkyou_apikey, mp['person_id'])
		if info.has_key('register_member_interests_html'):
			interests = info['register_member_interests_html']
			soup = BeautifulSoup(interests, 'html.parser')
			text = soup.text

			# split into lines for iteration
			splits = text.splitlines()

			print 'TEXT'
			print text
	return

	organisations = []
	graph = get_graph()

	tx = graph.begin()
	for mp in mps:
		party = encode_utf8(mp['party'])
		if not party in organisations:
			organisation_node = Node('Organisation', name=party)
			print 'Creating: %s' % party
			tx.create(organisation_node)
			organisations.append(party)
	
	tx.commit()
	tx = graph.begin()
	for mp in mps:
		name = encode_utf8(mp['name'])
		party = encode_utf8(mp['party'])

		person_node = Node('Person', name=name, occupation='Member of Parliament', member_id=mp['member_id'], person_id=mp['person_id'])
		print 'Creating: %s' % name
		tx.create(person_node)

		organisation_node = graph.find_one('Organisation', property_key='name', property_value=party)
		member_of = Relationship(person_node, "MEMBER_OF", organisation_node)
		print 'Creating: %s' % member_of
		tx.create(member_of)

	tx.commit()

if __name__ == "__main__":
	parser = OptionParser()
	parser.add_option("--csv", help="Dump to Json file", action="store_true", default=True)
	
	# parse the comand line
	(options, args) = parser.parse_args()
	
	# return a list (of dicts) of mps
	mps = get_all_mps(theyworkyou_apikey)
	searched = []
	
	# TODO: fix this crude arg porser
	if args:
		for member in args:
			for i in mps:
				if member.lower() in i['name'].lower():
					searched.append(i)
		mps = searched

	main(mps[:50])
