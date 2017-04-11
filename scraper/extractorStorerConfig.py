def pushToMongo(ip, port, db, collection):
	from pymongo import MongoClient
	return MongoClient(ip,port)[db][collection]

def pushToCassandra(keyspace):
	from cassandra.cluster import Cluster
	cluster = Cluster()
	return cluster.connect(keyspace)
	# Create the table with following columns
	# session.execute('create table primary_db (id text, lyrics text, lyrics_link text, artist_name text, song_name text, PRIMARY KEY(id)')

base_url = "http://www.allthelyrics.com"
index_url = "http://www.allthelyrics.com/index"
alphabets = list("abcdefghiklmnopqrstuvwxyz")
alphabets.append("numbers")