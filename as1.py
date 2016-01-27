# 1. get_text
# 2. get_links
# 3. del_repeats
# 4. crawl_again
# 5. text_file
import urllib2
import time
import re
import json

def get_adj_links(link, timeDelay):
	text = urllib2.urlopen(link).read()
	time.sleep(timeDelay)
	pattern = 'a href="(\/wiki\/[\w_\-.#]+)"'
	linkAffixes = re.findall(pattern, text)
	links = ['https://en.wikipedia.org'+linkAffix for linkAffix in linkAffixes]
	return links

def search(link, depth, depthLimit, timeDelay):
	linkSet = set()
	linkSet.add(link)
	count = len(linkSet)
	linkSetComp = linkSet
	setList = list()
	setList.append(linkSetComp)
	for depth in range(depth, depthLimit):
		depth = depth + 1
		linkSetComp2 = set()
		for link in linkSetComp:
			if count > 1000:
				break
			linksAdj = get_adj_links(link, timeDelay)
			linkSet2 = linkSet | set(linksAdj)
			linkSetComp2 |= (linkSet2 - linkSet)
			linkSet = linkSet2
			count = len(linkSet)
		linkSetComp = linkSetComp2
		setList.append(linkSetComp)
		print json.dumps(list(linkSetComp), sort_keys=True, indent=4, separators=(',', ': ')) + '\nTotal ' + str(count) + ' links crawled \'til here depth ' + str(depth)
	return setList, linkSet

def fwrite(list, path):
	with open(path, 'wb') as f:
		f.write(json.dumps(list, sort_keys=True, indent=4, separators=(',',':')))


if __name__ == '__main__':
	linkStart = 'https://en.wikipedia.org/wiki/Sustainable_Energy'
	depth = 0
	depthLimit = 2
	timeDelay = 1
	path = '/Users/Aleph/Desktop/IR/as1-1.txt'
	setList, linkSet = search(linkStart, depth, depthLimit, timeDelay)
	fwrite(list(linkSet), path)