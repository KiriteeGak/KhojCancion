import enchant
from pyxdameraulevenshtein import damerau_levenshtein_distance_ndarray
import numpy as np
import os, sys
from bs4 import BeautifulSoup

def checkAndCorrect(sentence):
	dic = enchant.Dict("en_US")
	return sentenceGenerator([word if dic.check(word.strip().lower()) else bestSuggestedWords(dic, word) for word in sentence.split(' ')])

def bestSuggestedWords(dic, word):
	words = np.array(dic.suggest(word))
	scores = list(damerau_levenshtein_distance_ndarray(word,words))
	return [words[i] for i,e in enumerate(scores) if e == min(scores) and " " not in words[i] and len(words[i])>=len(word)]

def sentenceGenerator(listOfElements,appendedTree = []):
	for i,s in enumerate(listOfElements):
		if appendedTree != []:
			if type(s) == list: appendedTree = [e1+" "+e2 for e2 in s for e1 in appendedTree]
			else: appendedTree = map(lambda x: x+" "+s,appendedTree)
		else:
			if type(s) == list: appendedTree += s
			else: appendedTree.append(s)
	return appendedTree