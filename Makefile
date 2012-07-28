all:

build: wiki
	cd wiki && git pull

wiki:
	git clone git@github.com:grammarware/ruconf.wiki.git wiki
