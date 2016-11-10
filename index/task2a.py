import re
import json
import math
import sys

# vsmq1 indexTC.out queries.txt 100 > resultsVSM1.eval

#pIn = "/Users/Aleph/Desktop/IR/indexTC.txt"
#pQueries = "/Users/Aleph/Desktop/IR/queries.txt"

def readInput(pIn):
	# [[token,[[doc,count]~]]~]
	with open(pIn, "r") as f:
		content = json.loads(f.read())
	return content["indexes"], content["tokens"], content["nums"]
	pass

def readQuery(pQueries):
	with open(pQueries, "r") as f:
		queries = {lines.replace("\r\n", "").split("\t")[0]:lines.replace("\r\n", "").split("\t")[1].split() for lines in f.readlines()}
	return queries
	pass

def calculate(indexes, tokens, nums, queries):
	D = float(len(nums))
	avg = float(sum(nums.values()))/D

	tfs = {}
	for index in indexes:
		token = index[0]
		pairs = index[1]
		tfs[token] = {}
		for pair in pairs:
			doc = pair[0]
			tf = pair[1]
			tfs[token][doc] = tf
		pass

	dfs = {}
	for token in tfs:
		dfs[token] = len(tfs[token])
		pass

	# {$okapis$ doc:{token:okapi~}~}
	okapis = {}
	for doc in nums:
		okapis[doc] = {}
		pass

	for token in tfs:
		for doc in tfs[token]:
			# tf ~ 
			tf = float(tfs[token][doc])
			length = float(nums[doc])
			# calculation
			okapi = tf/(tf+0.5+1.5*(length/avg))
			okapis[doc][token] = okapi
			pass
		pass

	# $rs$[$tfidfs${doc:tfidf~}~]
	tfidfs = {}
	for q in queries:
		tfidfs[q] = {}
		for token in queries[q]:
			for doc in tfs[token]:
				okapi = okapis[doc][token]
				df = dfs[token]
				tfidf = okapi*math.log(D/df)
				if doc in tfidfs[q]:
					tfidfs[q][doc] += tfidf
				else:
					tfidfs[q][doc] = tfidf
				pass
			pass
		pass
	return tfidfs

def output(tfidfs, string):
	num = int(string)
	ls = []
	for q in tfidfs:
		tuples = sorted(tfidfs[q].items(), key = lambda x:x[1], reverse = True)[:num]
		ls += [(q, tuples)]
		pass
	ls.sort(key = lambda x:x[0])
	return ls

if __name__ == "__main__":
	indexes, tokens, nums = readInput(sys.argv[1])
	queries = readQuery(sys.argv[2])
	tfidfs = calculate(indexes, tokens, nums, queries)
	ls = output(tfidfs, sys.argv[3])
	print json.dumps(ls, sort_keys = True, indent = 4, separators = (",",":"))