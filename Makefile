# Declarations for the current installation/version
DESTDIR=/var/www/html
VERSION=0.1
WHOAMI=foodlog-$(VERSION)
CONFDIR=/etc/$(WHOAMI)

# Source manifest, kinda
MAKETABLES = foodlog.sql
LIBRARY = 
CONFIG = foodlog.js

help:
	@echo Makefile for food log installation.
	@echo Targets: sql - (to create SQL tables)
	@echo www - to populate Web directory

sql:
