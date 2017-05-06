#!/usr/bin/env python

import os, sys, requests, logging
from bottle import route, request, response, redirect, hook, error, default_app, view, static_file, template, HTTPError
from icalendar import Calendar
from tinydb import TinyDB, Query, where
from tinydb.operations import increment

def fetchData(db, uri):
	table = db.table('events')
	ptr = Query()
	cal = Calendar.from_ical(requests.get(uri).text)

	for event in cal.walk('vevent'):
		uid = event.decoded('uid').replace('@zoho.com', '')
		if len(table.search(ptr.id == uid)) == 0:
			log.info("Inserting new event: {}".format(uid))
			table.insert({
				'id': uid,
				'date': event.decoded('dtstart'),
				'title': event.decoded('summary'),
				'location': event.decoded('location'),
				'desc': event.decoded('description'),
				'url': event.decoded('url'),
				'updated': '{}'.format(event.decoded('last-modified'))
			})
		else:
			# Event already exists, probably, so we'll check last updated time
			lookup = table.search(ptr.id == uid)
			if lookup[0]['updated'] != '{}'.format(event.decoded('last-modified')):
				log.info('Found an updated event: {}'.format(uid))
				table.update({
					'date': event.decoded('dtstart'),
					'title': event.decoded('summary'),
					'location': event.decoded('location'),
					'desc': event.decoded('description'),
					'url': event.decoded('url'),
					'updated': '{}'.format(event.decoded('last-modified'))
				}, ptr.id == uid)
			else:
				log.info('Event {} has not been updated since insertion'.format(uid))
	return table.all()

if __name__ == '__main__':

	# Instantiate the logger
	log = logging.getLogger('log')
	console = logging.StreamHandler()
	log.setLevel(logging.INFO)
	log.addHandler(console)

	# Configuration setting
	serverHost = os.getenv('IP', 'localhost')
	serverPort = os.getenv('PORT', '5000')
	app_db = TinyDB(os.getenv('APP_DATABASE', 'db/app.json'))
	app_ical = os.getenv('APP_ICAL', '')

	try:
		assert app_ical is not ''
		app = default_app()
	except AssertionError:
		log.error('APP_ICAL is unset. Set APP_ICAL to iCal URL and restart.')