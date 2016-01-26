# 1. get_text
# 2. get_links
# 3. del_repeats
# 4. crawl_again
# 5. text_file
import urllib2
import time
import re

def get_text(link, timeDelay):
    text = urllib2.urlopen(link).read()
    time.sleep(timeDelay)
    return text

def get_links(text):
	pattern = 'a href="(\/wiki\/[\w_\-.#]+)"'
	linkAffixes = re.findall(pattern, text)
	links = ['https://en.wikipedia.org'+linkAffix for linkAffix in linkAffixes]
	return links

def del_repeats(linksGet, linkSet):
	links = list(set(linksGet))
	linkSet = list(set(linkSet+links))
	return linkSet

def crawl(linkSet, level, levelLimit, timeDelay):
	links = linkSet
	for level in range(level, levelLimit+1):
		for link in links:
			text = get_text(link, timeDelay)
			linksGet = get_links(text)
			linkSet2 = del_repeats(linksGet, linkSet)
			count = len(linkSet2)
			print 'Count: ' + str(count)
			if count > 1000:
				break
			links = [link for link in linkSet2 if link not in linkSet]
			linkSet = linkSet2
		print str(linkSet) + '\nTotal ' + str(count) + ' links crawled by level ' + str(level)
	return linkSet

if __name__ == '__main__':
	linkSet = ['https://en.wikipedia.org/wiki/Sustainable_Energy']
	level = 0
	levelLimit = 2
	timeDelay = 1
	links = crawl(linkSet, level, levelLimit, timeDelay)
	print links