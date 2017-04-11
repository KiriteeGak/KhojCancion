import enchant
from pyxdameraulevenshtein import damerau_levenshtein_distance_ndarray
import numpy as np
import os, sys
from bs4 import BeautifulSoup

def checkAndCorrect(sentence):
	dic = enchant.Dict("en_US")
	return " ".join([word if dic.check(word.strip().lower()) else bestSuggestedWords(dic, word) for word in sentence.split(' ')])

def bestSuggestedWords(dic, word):
	words = np.array(dic.suggest(word))
	scores = list(damerau_levenshtein_distance_ndarray(word,words))
	return [words[i] for i,e in enumerate(scores) if e == min(scores)]