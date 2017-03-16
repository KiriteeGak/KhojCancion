from pymongo import MongoClient
add = "localhost"
port = 27017
db = "khojcancion"
collection = "lyrics"
mongoclientObj = MongoClient(add,port)[db][collection]

sample = "We like Van Halen And Iron Maiden"

class matchScorer(object):
	def getScore(self, sample, lyric):
		points_list, score = self.getShortestDistances(sample, lyric, [])
		print points_list, score
		match_score = (len(points_list) - points_list.count([]))/float(len(points_list))
		distance_score = float(len(points_list))/score
		print match_score, distance_score

	def getIndices(self, sample, lyric, ret):
		if len(sample.split(" ")) == 1:
			raise ValueError("Check the length of the sample string")
		(sample, lyric) = (self.getProperText(sample), self.getProperText(lyric))
		return [[i for i,lyric_word in enumerate(lyric) if sample_word == lyric_word] for sample_word in sample]

	def getProperText(self, text):
		return [x.strip() for x in text.strip().lower().split(" ")]

	def getShortestDistances(self, sample, lyric, ret, score = 0):
		points_list = self.getIndices(sample, lyric, [])
		for i in range(0,len(points_list)-1):
			globalMin = float("Inf")
			for pt1 in points_list[i]:
				for pt2 in points_list[i+1]:
					if abs(pt1-pt2) <= globalMin:
						globalMin = abs(pt1-pt2)
			if globalMin != float("Inf"):
				score += globalMin
		return points_list, score
