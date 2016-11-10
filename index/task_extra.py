import re
import nltk
import json
from bs4 import BeautifulSoup

inPath = "dic_html.txt"
outPath = "wiki_index2.txt"
reStr = "(\w+\.?\w+)*"

def load():
	with open(inPath, "r") as f:
		pages = json.loads(f.read())
	return pages

def extract(pages):
	texts = {}
	for p in pages:
		soup = BeautifulSoup(pages[p])
		texts[p] = soup.get_text()
		pass
	return texts

def tokenize(texts):
	tokens = {}
	for p in texts:
		tokens[p] = re.findall(reStr, texts[p].lower())
		pass
	return tokens

def stop(tokens):
	stop = set(nltk.corpus.stopwords.words("English"))
	for p in tokens:
		i = 0
		while i < len(tokens[p]):
			if tokens[p][i] in stop:
				tokens[p].pop(i)
			else:
				i += 1
			pass
		pass
	return tokens

def stem(stoppeds):
	stemmeds = {}
	for p in stoppeds:
		stemmer = nltk.stem.porter.PorterStemmer()
		stemmeds[p] = [stemmer.stem(stopped) for stopped in stoppeds[p]]
		pass
	return stemmeds

def index(stemmeds):
	se = set()
	for p in stemmeds:
		se |= set(stemmeds[p])
		pass
	indexes = {}
	for token in se:
		indexes[token] = {}
		pass
	for p in stemmeds:
		for token in stemmeds[p]:
			if p in indexes[token]:
				indexes[token][p] += 1
			else:
				indexes[token][p] = 1
			pass
		pass
	return indexes

def dump(indexes):
	with open(inPath, "w") as f:
		f.write(json.dumps(indexes, sort_keys=True, indent=4, separators=(",",":")))

if __name__ == "__main__":
	pages = load()
	tokens = tokenize(pages)
	print "tokens done"
	stoppeds = stop(tokens)
	print "stop done"
	stemmeds = stem(stoppeds)
	print "stem done"
	print stemmeds
	indexes = index(stemmeds)
	print "index done"
	print json.dumps(indexes, sort_keys=True, indent=4, separators=(",",":"))
	dump(indexes)