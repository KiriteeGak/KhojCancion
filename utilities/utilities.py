# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2, time, cPickle
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

def dumpAsPickle(filename, toDump):
	with open(filename+".pkl", 'wb') as fid:
		cPickle.dump(toDump, fid, protocol = 2)

def loadFromPickle(filename):
	with open(filename+".pkl", 'rb') as fid:
		return cPickle.load(fid)