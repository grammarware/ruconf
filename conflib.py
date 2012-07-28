#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import urllib, urllib2, httplib, socket

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
	elif s == 'ss':
		return '[[Summer School|Летняя школа]]'
	elif s == 'mc':
		return '[[Miniconference|Миниконференция]]'
	else:
		return 'ERROR'

def namelist(s):
	if s == 'ic':
		return 'International-Conference'
	elif s == 'wc':
		return 'Working-Conference'
	elif s == 'ws':
		return 'Workshop'
	elif s == 'sy':
		return 'Symposium'
	elif s == 'ss':
		return 'Summer-School'
	elif s == 'mc':
		return 'Miniconference'
	else:
		return 'ERROR'
