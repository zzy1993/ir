import urllib2
import time
import re
import json


def get_adj_links(keyWord, link, timeDelay):
	text = urllib2.urlopen(link).read()
	time.sleep(timeDelay)
	pattern = 'a href="\/wiki\/([\w_\-.]+?)".*? title="([\w\-. ]+?)"'
	tuples = re.findall(pattern, text)
	r = re.compile(keyWord)
	linksAdj = ['https://en.wikipedia.org/wiki/'+tuple[0] for tuple in tuples if r.search(tuple[0]) or r.search(tuple[1])]
	return linksAdj

# Here is the demon for the difference between depth and count
def crawl_depth(keyWord, link, depth, depthLimit, timeDelay, linkSet, count):
	if depth > depthLimit or count > 1000:
		return linkSet, count
	linkSetAdj = set(get_adj_links(keyWord, link, timeDelay))
	linkSet.add(link)
	print '(' + str(depth) + ', ' + str(count) + ')' + link
	count += 1
	depth += 1
	linkSetNew = linkSetAdj - linkSet
	for link in linkSetNew:
		linkSet, count = crawl_depth(keyWord, link, depth, depthLimit, timeDelay, linkSet, count)
	return linkSet, count

def search(keyWord, link, depth, depthLimit, timeDelay):
	linkSet = set([link])
	count = 0
	linkSet, count = crawl_depth(keyWord, link, depth, depthLimit, timeDelay, linkSet, count)
	return linkSet

def fwrite(listSet, path):
	with open(path, 'wb') as f:
		f.write(json.dumps(list(linkSet), sort_keys=True, indent=4, separators=(',',':')))

if __name__ == '__main__':
	linkStart = 'https://en.wikipedia.org/wiki/Sustainable_Energy'
	depth = 0
	depthLimit = 5
	timeDelay = 1
	keyWord = 'solar'
	path = '/Users/Aleph/Desktop/IR/as1-2-2.txt'
	linkSet = search(keyWord, linkStart, depth, depthLimit, timeDelay)
	fwrite(linkSet, path)
	print json.dumps(sorted(list(linkSet)), sort_keys=True, indent=4, separators=(',',':'))
