# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2, time

def getHtmlResponse(url):
	return urllib2.urlopen(url).read()

def getLinks(url):
	time.sleep(2)
	soup = BeautifulSoup(getHtmlResponse(url),'html.parser')
	return soup.find_all(href=True)