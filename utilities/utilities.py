# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2, time
from nltk.corpus import stopwords

def removeStopwords(text):
	return " ".join([word for word in text.split() if word.strip() not in stopwords.words('english')])

def getHtmlResponse(url):
	try:
		return urllib2.urlopen(url).read()
	except Exception:
		return None

def getLinks(url):
	time.sleep(1)
	resp = getHtmlResponse(url)
	if resp != None:
		soup = BeautifulSoup(resp,'html.parser')
		return soup.find_all(href=True)
	return None