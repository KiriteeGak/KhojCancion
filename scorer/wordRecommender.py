import enchant
from pyxdameraulevenshtein import damerau_levenshtein_distance_ndarray
import numpy as np

def checkAndCorrect(sentence):
	dic = enchant.Dict("en_US")
	return " ".join([word if dic.check(word.strip().lower()) else bestSuggestedWord(dic, word) for word in sentence.split(' ')])

def bestSuggestedWord(dic, word):
	words = np.array(dic.suggest(word))
	scores = list(damerau_levenshtein_distance_ndarray(word,words))
	return words[list(scores).index(min(scores))]