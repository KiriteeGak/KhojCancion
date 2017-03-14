# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2

def getHtmlResponse(url):
	return urllib2.urlopen(url).read()

def getLinks(url):
	soup = BeautifulSoup(getHtmlResponse(url),'html.parser')
	return soup.find_all(href=True)