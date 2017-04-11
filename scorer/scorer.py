from pymongo import MongoClient
from wordRecommender import *
import re

# mongo config
add = "localhost"
port = 27017
db = "khojcancion"
collection = "lyrics"
mongoclientObj = MongoClient(add,port)[db][collection]

# cassandra config
from cassandra.cluster import Cluster
cluster = Cluster()
session = cluster.connect("get_cancion")

class matchScorer(object):
	def getScore(self, sample, lyric):
		points_list, score = self.getShortestDistances(sample, lyric, [])
		match_score = (len(points_list) - points_list.count([]))/float(len(points_list))
		distance_score = len(points_list)/(float(score)*(points_list.count([])+1)) if score != 0 else 0
		return match_score+distance_score

	def getIndices(self, sample, lyric, ret):
		if len(sample.split(" ")) == 1:
			raise ValueError("Check the length of the sample string")
		(sample, lyric) = (self.getProperText(sample), self.getProperText(lyric))
		return [[i for i,lyric_word in enumerate(lyric) if sample_word == lyric_word] for sample_word in sample]

	def getProperText(self, text):
		return [x.strip() for x in self.punctuationRemover(text).strip().lower().split(" ")]

	def getShortestDistances(self, sample, lyric, ret, score = 0, penalty = 50):
		points_list = self.getIndices(sample, lyric, ret)
		points_list_modified = filter(lambda ele: ele != [], points_list)
		score = points_list.count([])*penalty
		for i in range(0,len(points_list_modified)-1):
			globalMin = float("Inf")
			for pt1 in points_list_modified[i]:
				for pt2 in points_list_modified[i+1]:
					if abs(pt1-pt2) <= globalMin:
						globalMin = abs(pt1-pt2)
			if globalMin != float("Inf"):
				score += globalMin
		return points_list, score

	def scoreFromSetupDb(self,sample, db='Mongo'):
		if db.lower() == 'mongo':
			return {each['song']: "%.3f" %self.getScore(sample,each['lyrics']) for each in mongoclientObj.find()}
		elif db.lower() == 'cassandra':
			cassandraObj = session.execute('select * from primary_db')
			return {each.song_name: "%.3f" %self.getScore(sample,each.lyrics) for each in cassandraObj}
		else:
			raise ValueError('Valid db names are cassandra and mongo, default is mongo')
			return {}

	def getTopnMatches(self, sample, n_top_matches):
		sample = checkAndCorrect(sample)
		return sorted(self.scoreFromSetupDb(sample,"cassandra").items(), key=lambda (k, v): v, reverse=True)[:int(n_top_matches)]

	def punctuationRemover(self, text):
		return re.sub(r'(\.|,|"|\'|\?|\!)',"",text)

class htmlTableGenerator(object):
	def generateTable(self, list_of_tuples):
		st = '''$def with (sometxt)
	$if sometxt:
		<table id="t01">
		<tr>
		<th>Song</th>
		<th>Match score</th>
		</tr>
'''
		for tup in list_of_tuples:
			st += '''
		<tr>
		<td>'''+tup[0]+'''</td>
		<td>'''+tup[1]+'''</td>
		<tr>
		'''
		st += '''</table>
	$else:
		<h3>Something went wrong<\h3>
		'''
		return st