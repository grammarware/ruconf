#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os, glob, datetime
from conflib import implode, namelist, listnames

if __name__ == '__main__':
	date = str(datetime.datetime.now()).split()[0]
	found = []
	sts = {'ws':[],'wc':[],'ss':[],'sy':[],'ic':[],'mc':[],'se':[],'co':[]}
	names = {}
	refd = []
	for f in glob.glob('*.wiki'):
		found.append(f.replace('.wiki',''))
	for n in found:
		if n in ('Home','TODO') or n in listnames.values():
			continue
		f = open('%s.wiki' % n,'r')
		content = f.read()
		for st in content.split('* Статус: [[')[1].split('\n')[0].split('[['):
			sts[implode(st.split('|')[0])].append(n)
		names[n] = content.split("* Перевод: '''")[1].split("'''")[0]
		for link in content.split('[[')[1:]:
			link = link.split(']]')[0].split('|')[0]
			if link.replace(' ','-') not in refd:
				refd.append(link.replace(' ','-'))
		f.close()
	refd.sort()
	f = open('TODO.wiki','w')
	f.write('Статьи, требующие создания:\n\n')
	cx = 0
	for n in refd:
		if n not in found:
			f.write('* [[%s]]\n' % n)
			cx += 1
	f.write("\n--''Список обновлён %s''\n" % date)
	f.close()
	for status in sts.keys():
		try:
			f = open('%s.wiki' % namelist(status),'r')
			b = filter(lambda x:not x.startswith('* ') and not x.startswith('--'), f.readlines())
			f.close()
		except IOError,e:
			b = []
		f = open('%s.wiki' % namelist(status),'w')
		if b:
			f.writelines(b)
		b = []
		for n in sts[status]:
			b.append("* '''[[%s]]''': [[%s|%s]]\n" % (n,n,names[n]))
		# for n in found:
		# 	if sts[n] == status:
		# 		b.append("* '''[[%s]]''': [[%s|%s]]\n" % (n,n,names[n]))
		if b:
			b.sort()
			f.writelines(b)
		f.write("--''Список обновлён %s''" % date)
		f.close()
	print 'Done, %i conferences to write.' % cx
