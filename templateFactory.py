#-*- coding: UTF-8 -*-


filters=[]

def registerFilter(filter):
	filters.append(filter)

def getTemplate(soup):
	for f in filters:
		if f.isSupport(soup):
			return f.getTemplate(soup)

	return None