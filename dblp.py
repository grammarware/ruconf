#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, urllib, urllib2, httplib, socket

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print 'Crawl what?'
		sys.exit(-1)
	name = sys.argv[1]
	f = open('wiki/%s.wiki' % name, 'r')
	content = f.read()
	dblp = content.split(' %s] на [[DBLP]]' % name)[0].split('[')[-1]
	s = urllib.urlopen(dblp).read()
	lst = []
	c = {}
	for h2 in s.split('<h2>')[1:]:
		lst.append(h2.split('</h2>')[0])
		c[lst[-1]] = []
		for cnt in h2.split('">Contents</a>')[:-1]:
			c[lst[-1]].append(cnt.split('"')[-1])
	print 'Crawling...'
	f.close()
	c1,c2 = content.split('== Ссылки ==')
	f = open('wiki/%s.wiki' % name, 'w')
	f.write(c1)
	f.write('== Архив ==\n')
	for s in lst:
		f.write('* %s\n' % s)
		for cnt in c[s]:
			f.write('** [%s DBLP]\n' % (dblp+cnt))
	f.write('\n== Ссылки ==')
	f.write(c2)
	f.close()
	print 'Done.'
