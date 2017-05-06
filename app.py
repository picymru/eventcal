#!/usr/bin/env python

import os, sys, requests, logging
from bottle import route, request, response, redirect, hook, error, default_app, view, static_file, template, HTTPError
from icalendar import Calendar
from tinydb import TinyDB, Query
from tinydb.operations import increment

def fetchData(db, uri):
	table = db.table('events')
	cal = Calendar.from_ical(requests.get(uri).text)

	for event in cal.walk('vevent'):
		table.insert({
			'id': "{}".format(event.get('uid')).replace('@zoho.com', ''),
			'date': '{}'.format(event.get('dtstart').dt),
			'title': '{}'.format(event.get('summary')),
			'location': '{}'.format(event.get('location')),
			'desc': '{}'.format(event.get('description')),
			'url': '{}'.format(event.get('url'))
		})
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
		print fetchData(app_db, app_ical)
	except AssertionError:
		log.error('APP_ICAL is unset. Set APP_ICAL to iCal URL and restart.')