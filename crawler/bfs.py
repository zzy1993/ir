import urllib2
import time
import re
import json

linkSeed = 'https://en.wikipedia.org/wiki/Sustainable_Energy'
keyWord = 'solar'
depthLimit = 5
timeDelay = 1
path = '/Users/Aleph/Desktop/IR/as1-2-1.txt'

def get_adj_links(link):
	text = urllib2.urlopen(link).read()
	time.sleep(timeDelay)
	pattern = 'a href="\/wiki\/([\w_\-.]+?)[#"].*? title="([\w\-. ]+?)"'
	tuples = re.findall(pattern, text)
	r = re.compile(keyWord)
	linksAdj = ['https://en.wikipedia.org/wiki/'+tuple[0] for tuple in tuples if r.search(tuple[0]) or r.search(tuple[1])]
	return linksAdj

def search(link):
	depth = 0
	count = 0
	linkSet = set([link])
	linksVisiting = [link]
	depthDict = {link: depth}

	while linksVisiting :
		link = linksVisiting.pop(0)
		linkSetAdj = set(get_adj_links(link))
		for link2 in linkSetAdj:
			if count > 1000 or depthDict[link] >= depthLimit:
				linksVisiting = []
				break
			if link2 not in linkSet and link2 not in linksVisiting:
				linksVisiting.append(link2)
				count += 1
				linkSet.add(link2)
				depthDict[link2] = depthDict[link] + 1
				print '( depth: ' + str(depthDict[link2]) + ', sequence: ' + str(count) + ') ' + link2
	return linkSet

def fwrite(content, path):
	with open(path, 'wb') as f:
		f.write(json.dumps(content, sort_keys=True, indent=4, separators=(',',':')))


if __name__ == '__main__':
	linkSet = search(linkSeed)
	fwrite(list(linkSet), path)

	print json.dumps(sorted(list(linkSet)), sort_keys=True, indent=4, separators=(',',':'))
	