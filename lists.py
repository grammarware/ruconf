#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os, glob
from conflib import implode, namelist, listnames, sign

if __name__ == '__main__':
	found = []
	sts = {'ws':[],'wc':[],'ss':[],'sy':[],'ic':[],'mc':[],'se':[],'co':[]}
	names = {}
	refd = []
	byyear = {}
	for f in glob.glob('*.wiki'):
		found.append(f.replace('.wiki',''))
	for n in found:
		if n in ('Home','All','Years','TODO') or n in listnames.values() or n.isdigit():
			continue
		# print 'Processing',n
		f = open('%s.wiki' % n,'r')
		content = f.read()
		for st in content.split('* Статус: [[')[1].split('\n')[0].split('[['):
			sts[implode(st.split('|')[0])].append(n)
		names[n] = content.split("* Перевод: '''")[1].split("'''")[0]
		for link in content.split('[[')[1:]:
			link = link.split(']]')[0].split('|')[0]
			if link.replace(' ','-') not in refd:
				refd.append(link.replace(' ','-'))
		for link in content.split('== Архив ==')[1].split('== Ссылки ==')[0].split('\n'):
			if link.startswith('* '):
				# print link
				year = link.split('(')[0].split()[-1]
				if not year.isdigit():
					continue
				rname = link.split(year)[0][2:].strip()
				# print '-->',n,'as',rname,'in',year
				if year not in byyear.keys():
					byyear[year] = []
				byyear[year].append((n,rname))
		f.close()
	refd.sort()
	f = open('TODO.wiki','w')
	g = open('All.wiki','w')
	f.write('Статьи, требующие создания:\n\n')
	g.write('Вики уже содержит следующие статьи:\n\n')
	cx1 = cx2 = 0
	for n in refd:
		if n not in found:
			f.write('* [[%s]]\n' % n)
			cx2 += 1
	for n in found:
		if n not in ('All','Home','Years','TODO') and n not in listnames.values() and not n.isdigit():
			g.write("* '''[[%s]]''': [[%s|%s]]\n" % (n,n,names[n]))
			cx1 += 1
	sign(f)
	sign(g)
	for status in sts.keys():
		try:
			f = open('%s.wiki' % namelist(status),'r')
			b = filter(lambda x:not x.startswith('* ') and not x.startswith('--') and x.strip(), f.readlines())
			f.close()
		except IOError,e:
			b = []
		f = open('%s.wiki' % namelist(status),'w')
		if b:
			f.writelines(b)
		b = []
		for n in sts[status]:
			b.append("* '''[[%s]]''': [[%s|%s]]\n" % (n,n,names[n]))
		if b:
			b.sort()
			f.writelines(b)
		sign(f)
	f = open('Years.wiki','w')
	f.write('Конференции по годам:')
	for year in sorted(byyear.keys()):
		y = []
		f.write('\n; [[%s]]\n: ' % year)
		g = open(year+'.wiki','w')
		g.write('Конференции, проведённые в %s году:\n' % year)
		for c in sorted(byyear[year],key=lambda x:x[1].lower()):
			if c[0]==c[1]:
				g.write('* [[%s]]\n' % c[0])
				y.append('[[%s]]' % c[0])
			else:
				g.write('* [[%s|%s]]\n' % c)
				y.append('[[%s|%s]]' % c)
		f.write(' • '.join(y))
		sign(g)
	sign(f)
	print 'Done, %i venues done, %i yet to go.' % (cx1, cx2)
