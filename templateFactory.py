#-*- coding: UTF-8 -*-


filters=[]

def registerFilter(filter):
	filters.append(filter)

def getTemplate(soup):
	if soup is None:
		None

	for f in filters:
		if f.isSupport(soup):
			return f.getTemplate(soup)

	return None