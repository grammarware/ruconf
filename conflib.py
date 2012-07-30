#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, datetime
import urllib, urllib2, httplib, socket

listnames = {
				'ic':'International-Conference',
				'wc':'Working-Conference',
				'ws':'Workshop',
				'sy':'Symposium',
				'ss':'Summer-School',
				'mc':'Miniconference',
				'se':'Seminar',
				'co':'Colloquium'
			}

rusnames = {
				'ic':'международная конференция',
				'wc':'рабочая конференция',
				'ws':'рабочая встреча',
				'sy':'симпозиум',
				'ss':'летняя школа',
				'mc':'миниконференция',
				'se':'семинар',
				'co':'коллоквиум'
			}

def exists(url):
	try:
		s = urllib.urlopen(url).read()
	except IOError,e:
 		return False
	except socket.error,e:
		return False
	if s.find('was not found on this server') < 0:
		return True
	return False

def implode(z):
	s = z.lower()
	if s.find('workshop') > -1:
		return 'ws'
	elif s.find('working conference') > -1:
		return 'wc'
	elif s.find('international conference') > -1:
		return 'ic'
	elif s.find('summer school') > -1:
		return 'ss'
	elif s.find('miniconference') > -1:
		return 'mc'
	elif s.find('mini-conference') > -1:
		return 'mc'
	elif s.find('symposium') > -1:
		return 'sy'
	elif s.find('seminar') > -1:
		return 'se'
	elif s.find('colloquium') > -1:
		return 'co'
	else:
		return 'ic'

def explode(s):
	return '[[%s|%s]]' % (namelist(s),namerus(s))

def namelist(s):
	if listnames.has_key(s):
		return listnames[s]
	else:
		return 'ERROR'

def namerus(s):
	if rusnames.has_key(s):
		return rusnames[s]
	else:
		return 'ERROR'

def sign(f):
	f.write("\n--''Список обновлён %s''\n" % str(datetime.datetime.now()).split()[0])
	f.close()
