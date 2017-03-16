# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests, urllib2, re
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from utilities import *
from config import *

class lyricExtractor(object):
	def main(self, base_url, index_url, alphabets):
		for letter in alphabets:
			leaf1_url = index_url+"/"+letter
			element_tag_links = getLinks(leaf1_url)
			max_number_of_pages = self.getPages(element_tag_links)
			for pageNumber in range(1,max_number_of_pages+1):
				page_url_modified = leaf1_url+"/"+letter+str(pageNumber)+".htm"
				refined_links = self.refineLinks(getLinks(page_url_modified), "/lyrics", "title", False)
				for each_link in refined_links:
					song_links = list(set(self.getAllSongs(base_url+"/"+each_link, each_link, "title")))
					for each_song in song_links:
						song_url = base_url+"/"+each_song
						(lyrics, song_name) = self.getSongLyrics(song_url)
						try:
							self.makeDocumentAndPush(each_link.split('/')[-1], song_name, song_url, lyrics)
						except DuplicateKeyError as e:
							pass

	def makeDocumentAndPush(self, artist, song_name, lyric_url, lyrics):
		doc = {
				'_id' : artist+"_"+song_name,
				'artist_name': artist,
				'song' : song_name,
				'lyrics' : lyrics,
				'lyric link' :lyric_url
			}
		mongoclientObj.insert(doc)

	def getSongLyrics(self, song_url):
		soup = BeautifulSoup(getHtmlResponse(song_url),'html.parser')
		return soup.find_all('div',{"class":"content-text-inner"})[0].text.replace("\n"," "), soup.find_all('h1',{"class":"page-title"})[0].text.lower().replace(" lyrics","")

	def refineLinks(self, list_of_links, baseword_href, baseword_title, node_branch):
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

	def getNoOfPages(self, element_tag_links, baseword_title):
		out_links = []
		for link in element_tag_links:
			try:
				if link['title'] and baseword_title.lower() in link['title'].lower():
					out_links.append(link['href'])
			except KeyError:
				pass
		return out_links

	def maxPageForaAlphabet(self, list_of_links):
		return max(list([int(re.findall(r'\d+.htm',link,re.IGNORECASE)[0].replace('.htm','')) for link in list_of_links]))

	def getPages(self, element_tag_links):
		pages = self.getNoOfPages(element_tag_links,"Go to page")
		return self.maxPageForaAlphabet(pages)
		
	def getAllSongs(self, page_url, baseword_href, baseword_title):
		return self.refineLinks(getLinks(page_url), baseword_href, baseword_title, node_branch = True)