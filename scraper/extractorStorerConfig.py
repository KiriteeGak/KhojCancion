ip = "localhost"
port = 27017
db = "test_get_cancion"
collection = "lyrics"
keyspace = "get_cancion"

base_url = "http://www.allthelyrics.com"
index_url = "http://www.allthelyrics.com/index"
alphabets = list("abcdefghiklmnopqrstuvwxyz")
alphabets.append("numbers")

from pymongo import MongoClient
mongoCliObj = MongoClient(ip,port)[db][collection]

from cassandra.cluster import Cluster
cluster = Cluster()
cassClusObj = cluster.connect(keyspace)

def createTable():
	session.execute('create table primary_db (id text, lyrics text, lyrics_link text, artist_name text, song_name text, PRIMARY KEY(id)')