from pymongo import MongoClient
add = "localhost"
port = 27017
db = "khojcancion"
collection = "lyrics"
mongoclientObj = MongoClient(add,port)[db][collection]

class matchScorer(object):
	def getScore(self, sample, lyric):
		points_list, score = self.getShortestDistances(sample, lyric, [])
		match_score = (len(points_list) - points_list.count([]))/float(len(points_list))
		if score != 0:
			distance_score = len(points_list)/(float(score)+(points_list.count([])+1))
		else:
			distance_score = 0
		return match_score+distance_score

	def getIndices(self, sample, lyric, ret):
		if len(sample.split(" ")) == 1:
			raise ValueError("Check the length of the sample string")
		(sample, lyric) = (self.getProperText(sample), self.getProperText(lyric))
		return [[i for i,lyric_word in enumerate(lyric) if sample_word == lyric_word] for sample_word in sample]

	def getProperText(self, text):
		return [x.strip() for x in text.strip().lower().split(" ")]

	def getShortestDistances(self, sample, lyric, ret, score = 0):
		points_list = self.getIndices(sample, lyric, ret)
		for i in range(0,len(points_list)-1):
			globalMin = float("Inf")
			for pt1 in points_list[i]:
				for pt2 in points_list[i+1]:
					if abs(pt1-pt2) <= globalMin:
						globalMin = abs(pt1-pt2)
			if globalMin != float("Inf"):
				score += globalMin
		return points_list, score

	def getMatchScores(self, sample):
		return {each['_id']: "%.3f" %self.getScore(sample,each['lyrics']) for each in mongoclientObj.find()}

	def getTopnMatches(self, n_top_matches, sample):
		return sorted(self.getMatchScores(sample).items(), key=lambda (k, v): v, reverse=True)[:n_top_matches]

if __name__ == '__main__':
	sample = "at you gettin by aint the same without you"
	print matchScorer().getTopnMatches(10,sample)