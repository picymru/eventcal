#!/usr/bin/env python

import os, sys, requests, logging, calendar, datetime, ujson, hashlib, CommonMark
from bottle import route, request, response, redirect, hook, error, default_app, view, static_file, template, HTTPError
from icalendar import Calendar
from tinydb import TinyDB, Query, where
from tinydb.operations import increment

def fetchData(db, uri, cachetime=3600):
	ptr = Query()
	table = db.table('events')
	settings = db.table('settings')
	cal = Calendar.from_ical(requests.get(uri).text)

	lastUpdated = settings.search(ptr.name == 'fetchTime')
	if len(lastUpdated) == 0:
		# We haven't fetched data at all!
		log.info("Data fetching has not been completed yet. Fetching...")
		settings.insert({
			'name': 'fetchTime',
			'value': calendar.timegm(datetime.datetime.utcnow().timetuple())
		})
		pass
	else:
		past = datetime.datetime.utcnow() - datetime.timedelta(seconds=cachetime)
		if lastUpdated[0]['value'] < calendar.timegm(past.timetuple()):
			# The data is older than an hour, so we refresh it
			log.info('Data is considered stale. Fetching...')
			pass
		else:
			# The data is less than an hour old, so we consider it current
			log.info('Returning cached data...')
			return table.all()

	for event in cal.walk('vevent'):
		uid = hashlib.sha224(event.decoded('uid')).hexdigest()[:15]
		if len(table.search(ptr.id == uid)) == 0:
			log.info("Inserting new event: {}".format(uid))
			table.insert({
				'id': uid,
				'date': '{}'.format(event.decoded('dtstart')),
				'title': event.decoded('summary'),
				'location': event.decoded('location', 'Online'),
				'desc': CommonMark.commonmark(event.decoded('description', 'This event doesn\'t have a description')),
				'url': event.decoded('url', ''),
				'updated': '{}'.format(event.decoded('last-modified'))
			})
		else:
			# Event already exists, probably, so we'll check last updated time
			lookup = table.search(ptr.id == uid)
			if lookup[0]['updated'] != '{}'.format(event.decoded('last-modified')):
				log.info('Found an updated event: {}'.format(uid))
				table.update({
					'date': '{}'.format(event.decoded('dtstart')),
					'title': event.decoded('summary'),
					'location': event.decoded('location', 'Online'),
					'desc': CommonMark.commonmark(event.decoded('description', 'This event doesn\'t have a description')),
					'url': event.decoded('url', ''),
					'updated': '{}'.format(event.decoded('last-modified'))
				}, ptr.id == uid)
			else:
				log.info('Event {} has not been updated since insertion'.format(uid))

	settings.update({
		'value': calendar.timegm(datetime.datetime.utcnow().timetuple())
	}, ptr.name == 'fetchTime')
	return table.all()

@route('/assets/<filepath:path>')
def server_static(filepath):
	return static_file(filepath, root='views/static')

@route('/event/<id>')
def event(id):
	ptr = Query()
	table = app_db.table('events')
	event = table.search(ptr.id==id)[0]
	return template('event', event=event)

@route('/events.json')
def indexJSON():
	calendar = fetchData(app_db, app_ical, app_cachetime)
	response.content_type = 'application/json'
	return ujson.dumps(calendar)

@route('/')
@route('/events')
def index():
	calendar = fetchData(app_db, app_ical, app_cachetime)
	return template('index', events=calendar)

if __name__ == '__main__':

	# Instantiate the logger
	log = logging.getLogger('log')
	console = logging.StreamHandler()
	log.setLevel(logging.INFO)
	log.addHandler(console)

	# Configuration setting
	serverHost = os.getenv('IP', 'localhost')
	serverPort = os.getenv('PORT', '5000')
	app_cachetime = int(os.getenv('APP_CACHETIME', 3600))
	app_dbpath = os.getenv('APP_DATABASE', 'db/app.json')
	app_db = TinyDB(app_dbpath)
	app_deleteOnLoad = os.getenv('APP_DELETE', '0')
	app_ical = os.getenv('APP_ICAL', '')

	try:
		assert app_ical is not ''
		if app_deleteOnLoad is not '0':
			try:
				os.unlink(app_dbpath)
			except OSError:
				log.error('Unable to remove active database at {}'.format(app_dbpath))
				exit()
		app = default_app()
		app.run(host=serverHost, port=serverPort, server='tornado')
	except AssertionError:
		log.error('APP_ICAL is unset. Set APP_ICAL to iCal URL and restart.')