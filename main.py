# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests, urllib2, re

'''
	For each alphabet
	For each page of the alphabet
	For each artist in that alphabet
	For each song of that artist
	-- Get lyrics
'''

def main(base_url, index_url, alphabets):
	for letter in alphabets:
		leaf1_url = index_url+"/"+letter
		element_tag_links = getLinks(leaf1_url)
		max_number_of_pages = getPages(element_tag_links)
		for pageNumber in range(1,max_number_of_pages+1):
			page_url_modified = leaf1_url+"/"+letter+str(pageNumber)+".htm"
			refined_links = refineLinks(getLinks(page_url_modified), "/lyrics", "title", False)
			for each_link in refined_links:
				getAllSongs(base_url+"/"+each_link, each_link, "title")
			exit()

def getHtmlResponse(url):
	return urllib2.urlopen(url).read()

def getLinks(url):
	soup = BeautifulSoup(getHtmlResponse(url),'html.parser')
	return soup.find_all(href=True)

def refineLinks(list_of_links, baseword_href, baseword_title, node_branch):
	out_links = []
	lyric_links = [link for link in list_of_links if baseword_href in link['href']]
	if node_branch:
		lyric_links = list(filter(lambda x: ".html" in x['href'], lyric_links))
	for link in lyric_links:
		try:
			link[baseword_title]
		except KeyError:
			out_links.append(link['href'])
	return out_links

def getNoOfPages(element_tag_links, baseword_title):
	out_links = []
	for link in element_tag_links:
		try:
			if link['title'] and baseword_title.lower() in link['title'].lower():
				out_links.append(link['href'])
		except KeyError:
			pass
	return out_links

def maxPageForaAlphabet(list_of_links):
	return max(list([int(re.findall(r'/index/a/a(.*?).htm',link,re.IGNORECASE)[0]) for link in list_of_links]))

def getPages(element_tag_links):
	allPagesForLetter = getNoOfPages(element_tag_links,"Go to page")
	return maxPageForaAlphabet(allPagesForLetter)

def getAllSongs(page_url, baseword_href, baseword_title):
	print refineLinks(getLinks(page_url), baseword_href, baseword_title, node_branch = True)
	exit()

if __name__ == '__main__':
	base_url = "http://www.allthelyrics.com"
	index_url = "http://www.allthelyrics.com/index"
	alphabets = list("abcdefghiklmnopqrstuvwxyz0123456789")
	main(base_url, index_url, alphabets)