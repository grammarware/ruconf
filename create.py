#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import urllib, urllib2, httplib, socket
rel = {}

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

def determine(s):
	if s.find('Workshop') > -1:
		return 'ws'
	elif s.find('Working conference') > -1:
		return 'wc'
	elif s.find('Working Conference') > -1:
		return 'wc'
	elif s.find('International conference') > -1:
		return 'ic'
	elif s.find('International Conference') > -1:
		return 'ic'
	elif s.find('Symposium') > -1:
		return 'sy'
	else:
		return 'ic'

def explode(s):
	if s == 'ic':
		return '[[International Conference|международная конференция]]'
	elif s == 'wc':
		return '[[Working Conference|рабочая конференция]]'
	elif s == 'ws':
		return '[[Workshop|рабочая встреча]]'
	elif s == 'sy':
		return '[[Symposium|Симпозиум]]'
	else:
		return 'ERROR'

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print 'Create what?'
		sys.exit(-1)
	name = sys.argv[1]
	fname = 'wiki/%s.wiki' % name
	print 'Creating %s...' % name
	if os.path.exists(fname):
		print 'Already exists.'
		sys.exit(1)
	f = open(fname,'w')
	fullname = raw_input("Full name? ")
	f.write("* Название: '''%s'''\n" % fullname)
	f.write("* Перевод: '''%s'''\n" % raw_input("Translation? "))
	status = determine(fullname)
	s = raw_input("Status[%s]? " % status)
	if s:
		status = s
	f.write('* Статус: %s\n' % explode(status))
	f.write('\n== Тематика ==\n* …\n\n== Ссылки ==\n')
	dblp = name.lower()
	while not exists('http://dblp.uni-trier.de/db/conf/%s/index.html' % dblp):
		dblp = raw_input("DBLP[%s]? " % dblp)
	# s = urllib.urlopen('http://dblp.uni-trier.de/db/conf/%s/index.html' %s dblp).read()
	f.write('* [http://dblp.uni-trier.de/db/conf/%s/ %s] на [[DBLP]]\n' % (dblp, name))
	acad = raw_input("Academic? ")
	if acad:
		f.write('* [http://academic.research.microsoft.com/Conference/%s/ %s] на [[Academic]]\n' % (acad, name))
	f.close()
	print 'Yes.'
