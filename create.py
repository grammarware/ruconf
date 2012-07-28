#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
from conflib import exists, implode, explode

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print 'Create what?'
		sys.exit(-1)
	name = sys.argv[1]
	fname = '%s.wiki' % name
	print 'Creating %s...' % name
	if os.path.exists(fname):
		print 'Already exists.'
		sys.exit(1)
	f = open(fname,'w')
	fullname = raw_input("Full name? ")
	f.write("* Название: '''%s'''\n" % fullname)
	f.write("* Перевод: '''%s'''\n" % raw_input("Translation? "))
	status = implode(fullname)
	s = raw_input("Status[%s]? " % status)
	if s:
		status = s
	f.write('* Статус: %s\n' % explode(status))
	f.write('\n== Тематика ==\n* …\n\n== Ссылки ==\n')
	dblp = name.lower()
	while dblp != '' and not exists('http://dblp.uni-trier.de/db/conf/%s/index.html' % dblp):
		dblp = raw_input("DBLP[%s]? " % dblp)
	f.write('* [http://dblp.uni-trier.de/db/conf/%s/ %s] на [[DBLP]]\n' % (dblp, name))
	acad = raw_input("Academic? ")
	if acad:
		f.write('* [http://academic.research.microsoft.com/Conference/%s/ %s] на [[Academic]]\n' % (acad, name))
	f.close()
	print 'Yes.'
