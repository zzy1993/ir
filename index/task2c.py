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

def calculate(indexes, lengths, nums, queries):
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

	# $rs$[$tfidfs${doc:tfidf~}~]
	k1, k2, b = 1.2, 100, 0.75
	bm25s = {}
	for q in queries:
		bm25s[q] = {}
		for token in queries[q]:
			for doc in tfs[token]:
				tf = tfs[token][doc]
				df = dfs[token]
				length = nums[doc]
				bm25 = math.log((D+0.5)/(df+0.5))\
					*((tf+k1*tf)/(tf+k1*((1-b)+b*(length/avg))))\
					*((tf+k2*tf)/(tf+k2))
				if doc in bm25s[q]:
					bm25s[q][doc] += bm25
				else:
					bm25s[q][doc] = bm25
				pass
			pass
		pass
	return bm25s

def output(bm25s, string):
	num = int(string)
	ls = []
	for q in bm25s:
		tuples = sorted(bm25s[q].items(), key = lambda x:x[1], reverse = True)[:num]
		ls += [(q, tuples)]
		pass
	ls.sort(key = lambda x:x[0])
	return ls

if __name__ == "__main__":
	indexes, lengths, vocas = readInput(sys.argv[1])
	queries = readQuery(sys.argv[2])
	bm25s = calculate(indexes, lengths, vocas, queries)
	ls = output(bm25s, sys.argv[3])
	print json.dumps(ls, sort_keys = True, indent = 4, separators = (",",":"))