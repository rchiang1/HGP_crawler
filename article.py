from collections import namedtuple
import json
from dbco import * # this imports the db connexion

Article = namedtuple('Article', ['guid', 'title', 'url', 'timestamp', 'source', 'feed', 'content', 'img', 'keywords'])
class Article(namedtuple('Article', ['guid', 'title', 'url', 'timestamp', 'source', 'feed', 'content', 'img', 'keywords'])):
    def __new__(cls, guid='', title='', url='', timestamp=0, source='', feed='', content='No Content', img='', keywords=[]):
        return super(Article, cls).__new__(cls, guid, title, url, timestamp, source, feed, content, img, keywords)

def saveNewArticles(newArticles):
	As = []
	for a in newArticles:
		if isValid(a):
			As.append(a._asdict())
		else:
			print "Article from source: ", a.source, "feed: ", a.feed, " was invalid"
	if len(As) > 0:
		insertArticles(db, As)

def insertArticles(db, As):
	for a in As:
		db.qdoc.update({'guid': a['guid']}, {'$set': a}, upsert=True) # if the GUID is already in the set
	# db.qdoc.insert(As)

def saveNewArticlesFile(newArticles):
	with open("DB_ex.txt", "a") as f:
		for a in newArticles:
			if isValid(a):
				f.write(json.dumps(a._asdict())+'\n')
			else:
				print "Article from source: ", a.source, "feed: ", a.feed, " was invalid"

def isValid(a):
	if a.guid == '':
		return False
	if a.title == '':
		return False
	if a.url == '':
		return False
	if a.timestamp < 500:
		return False
	if a.source == '':
		return False
	if a.feed == '':
		return False
	if a.content == '':
		return False
	return True