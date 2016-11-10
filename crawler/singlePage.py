import urllib2
import time
import re
import json

path1 = '/Users/Aleph/Desktop/IR/1-1.txt'
path2 = '/Users/Aleph/Desktop/IR/1-1f.txt'

def visit_link(link, timeDelay):
	text = urllib2.urlopen(link).read()
	time.sleep(timeDelay)
	return text

def get_adj_links(text):
	pattern = 'a href="\/wiki\/([\w_\-.]+?)"'
	linkAffixes = re.findall(pattern, text)
	links = ['https://en.wikipedia.org/wiki/'+linkAffix for linkAffix in linkAffixes]
	return links

def search(link, depthLimit, timeDelay):
	text = visit_link(link, timeDelay)
	depth = 0
	count = 0
	linkSet = set([link])
	linksVisiting = [link]
	textDict = {link: text}
	depthDict = {link: depth}

	while linksVisiting:
		link = linksVisiting.pop(0)

		for link2 in set(get_adj_links(textDict[link])):
			if count > 1000 or depthDict[link] >= 5:
				linksVisiting = []
				break
			if link2 not in linkSet and link2 not in linksVisiting:
				linksVisiting.append(link2)

				text = visit_link(link2, timeDelay)
				count += 1
				linkSet.add(link2)
				textDict[link2] = text
				depthDict[link2] = depthDict[link] + 1
				print '( depth: ' + str(depthDict[link2]) + ', sequence: ' + str(count) + ') ' + link2
	return linkSet, textDict

def fwrite(content, path):
	with open(path, 'wb') as f:
		f.write(json.dumps(content, sort_keys=True, indent=4, separators=(',',':')))

if __name__ == '__main__':
	linkSeed = 'https://en.wikipedia.org/wiki/Sustainable_Energy'
	depthLimit = 5
	timeDelay = 1
	linkSet, textDict = search(linkSeed, depthLimit, timeDelay)
	fwrite(list(linkSet), path1)
	fwrite(textDict, path2)
	print json.dumps(sorted(list(linkSet)), sort_keys=True, indent=4, separators=(',',':'))