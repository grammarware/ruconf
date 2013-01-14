#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os, glob
from conflib import implode, namelist, listnames, sign

if __name__ == '__main__':
	found = []
	sts = {'ws':[],'wc':[],'ss':[],'sy':[],'ic':[],'mc':[],'se':[],'co':[]}
	names = {}
	refd = []
	refby = {}
	byyear = {}
	for f in glob.glob('*.wiki'):
		found.append(f.replace('.wiki',''))
	for n in found:
		if n in ('All','Years','TODO') or n in listnames.values() or n.isdigit():
			continue
		# print 'Processing',n
		f = open('%s.wiki' % n,'r')
		content = f.read()
		if n != 'Home':
			for st in content.split('* Статус: [[')[1].split('\n')[0].split('[['):
				sts[implode(st.split('|')[0])].append(n)
			names[n] = content.split("* Перевод: '''")[1].split("'''")[0]
		for link in content.split('[[')[1:]:
			link = link.split(']]')[0].split('|')[0]
			if link.replace(' ','-') not in refd:
				refd.append(link.replace(' ','-'))
			# print n,'to',link.replace(' ','-')
			if link.replace(' ','-') not in refby.keys():
				refby[link.replace(' ','-')] = []
			if n not in refby[link.replace(' ','-')]:
				refby[link.replace(' ','-')].append(n)
		if n != 'Home':
			for link in content.split('== Архив ==')[1].split('== Ссылки ==')[0].split('\n'):
				# print 'Link is "%s"' %link
				if link.startswith('* '):
					# print link
					year = link.split('(')[0].split()[-1]
					if year.startswith('[[') and year.endswith(']]'):
						year = year[2:-2]
					# print 'Year is "%s"' %year
					if not year.isdigit():
						continue
					rname = link.split(year)[0][2:].strip()
					if rname.endswith('[['):
						rname = rname[:-2].strip()
					# print '-->',n,'as',rname,'in',year
					if year not in byyear.keys():
						byyear[year] = []
					byyear[year].append((n,rname))
		f.close()
	refd.sort()
	f = open('TODO.wiki','w')
	g = open('All.wiki','w')
	f.write('Статьи, требующие создания (%i):\n\n' % len(filter(lambda x:x not in found,refd)))
	g.write('Вики уже содержит следующие статьи (%i):\n\n' % len(filter(lambda n:n not in ('All','Home','Years','TODO') and n not in listnames.values() and not n.isdigit(),found)))
	cx1 = cx2 = 0
	for n in refd:
		if n not in found:
			# print n,'is needed by',refby[n]
			f.write("* '''[[%s]]''' (⇐ %s)\n" % (n,', '.join(map(lambda x:'[[%s]]' % x,refby[n]))))
			cx2 += 1
	for n in found:
		if n not in ('All','Home','Years','TODO') and n not in listnames.values() and not n.isdigit():
			g.write("* '''[[%s]]''': [[%s|%s]]\n" % (n,n,names[n]))
			cx1 += 1
	sign(f,[])
	sign(g,[])
	for status in sts.keys():
		try:
			f = open('%s.wiki' % namelist(status),'r')
			b = filter(lambda x:not x.startswith('* ') and not x.startswith('--') and not x.startswith('—') and x.strip(), f.readlines())
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
		sign(f,[])
	f = open('Years.wiki','w')
	f.write('Конференции по годам:')
	# print sorted(byyear.keys())
	for year in sorted(byyear.keys()):
		y = []
		f.write('\n; [[%s]]\n: ' % year)
		g = open(year+'.wiki','r')
		csold = []
		for c in filter(lambda x:x.startswith('* '),map(lambda x:x.strip(),g.readlines())):
			a = c.split('[[')[1].split(']]')[0].split('|')
			if len(a)==1:
				csold.append((a[0],a[0]))
			else:
				csold.append((a[0],a[1]))
		g.close()
		csnew = sorted(byyear[year],key=lambda x:x[1].lower())
		if csnew == csold:
			print 'Year %s is unchanged.' % year
		else:
			# print 'OLD:',csold,'\nNEW:',csnew
			csupd = []
			g = open(year+'.wiki','w')
			g.write('Конференции, проведённые в %s году:\n' % year)
			for c in csnew:
				if c not in csold:
					csupd.append(c[0])
				if c[0]==c[1]:
					g.write('* [[%s]]\n' % c[0])
					y.append('[[%s]]' % c[0])
				else:
					g.write('* [[%s|%s]]\n' % c)
					y.append('[[%s|%s]]' % c)
			sign(g,[('Years','Годы')])
			print 'Year %s is updated with %s.' % (year,', '.join(csupd))
		f.write(' • '.join(y))
	sign(f,[])
	print 'Done, %i venues done, %i yet to go.' % (cx1, cx2)
