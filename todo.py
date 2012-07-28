#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os, datetime

if __name__ == '__main__':
	found = []
	refd = []
	for f in os.listdir('wiki'):
		if f not in ('Home.wiki','TODO.wiki','.git','.gitignore'):
			found.append(f)
	for n in found:
		f = open('wiki/'+n,'r')
		for link in f.read().split('[[')[1:]:
			link = link.split(']]')[0].split('|')[0]
			if link not in refd:
				refd.append(link)
		f.close()
	refd.sort()
	f = open('wiki/TODO.wiki','w')
	f.write('Статьи, требующие создания:\n\n')
	cx = 0
	for n in refd:
		if n+'.wiki' not in found:
			f.write('* [[%s]]\n' % n)
			cx += 1
	f.write("\n--''Список обновлён %s''\n" % datetime.datetime.now())
	f.close()
	print 'Done, %i conferences to write.' % cx
