from scraper.extractorStorer import lyricExtractor as le
from scraper.extractorStorerConfig import *
from utilities.utilities import *
dumpAsPickle("DumpedUrls", le().main(base_url, index_url, alphabets))