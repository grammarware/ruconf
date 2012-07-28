#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os, datetime
from conflib import implode, namelist

if __name__ == '__main__':
	found = []
	sts = {}
	refd = []
	for f in os.listdir('wiki'):
		if f not in ('.git','.gitignore'):
			found.append(f)
	for n in found:
		if n in ('Home.wiki','TODO.wiki','International-Conference.wiki','Working-Conference.wiki','Workshop.wiki','Summer-School.wiki','Symposium.wiki'):
			sts[n] = ''
			continue
		f = open('wiki/'+n,'r')
		content = f.read()
		sts[n] = implode(content.split('* Статус: [[')[1].split('|')[0])
		for link in content.split('[[')[1:]:
			link = link.split(']]')[0].split('|')[0]
			if link not in refd:
				refd.append(link.replace(' ','-'))
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
	for status in ('ws','wc','ss','sy','ic'):
		f = open('wiki/%s.wiki' % namelist(status),'r')
		b = filter(lambda x:not x.startswith('* '), f.readlines())
		f.close()
		f = open('wiki/%s.wiki' % namelist(status),'w')
		if b:
			f.writelines(b)
		for n in found:
			if sts[n] == status:
				f.write('* [[%s]]\n' % n)
		f.close()
	print 'Done, %i conferences to write.' % cx
