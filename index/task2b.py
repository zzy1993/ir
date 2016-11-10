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
	ds= {}
	for doc in nums:
		ds[doc] = {}
	for token in tokens:
		df = float(dfs[token])
		for doc in tfs[token]:
			tf = float(tfs[token][doc])
			length = float(nums[doc])
			okapi = tf/(tf+0.5+1.5*(length/avg))
			ds[doc][token] = okapi*math.log(D/df)
			pass
		pass

	# $rs$[$tfidfs${doc:tfidf~}~]

	seQ = set()
	for q in queries:
		words = queries[q]
		for word in words:
			seQ.add(word)
			pass
		pass
	tokensQ = list(seQ)

	numsQ = {}
	for q in queries:
		numsQ[q] = len(queries[q])
		pass

	tfsQ = {}
	for token in tokensQ:
		tfsQ[token] = {}
		for q in queries:
			if token in queries[q]:
				if q in tfsQ[token]:
					tfsQ[token][q] += 1
				else:
					tfsQ[token][q] = 1
				pass
			pass
		pass

	dfsQ = {}
	for token in tokensQ:
		dfsQ[token] = len(tfsQ[token])
		pass

	DQ = float(len(numsQ))

	qs = {}
	for q in queries:
		qs[q] = {}
		pass
	for token in tokensQ:
		dfQ = float(dfsQ[token])
		for q in tfsQ[token]:
			tfQ = float(tfsQ[token][q])
			qs[q][token] = tfQ*math.log(DQ/dfQ)
			pass
		pass
	return qs, ds

def similarity(qs, ds):
	qSum = {}
	for q in qs:
		qSum[q] = 0.0
		for token in qs[q]:
			qSum[q] += qs[q][token]**2
			pass
		pass
	dSum = {}
	for d in ds:
		dSum[d] = 0.0
		for token in ds[d]:
			dSum[d] += ds[d][token]**2
			pass
		pass
	ss = {}
	for q in qs:
		ss[q] = {}
		for d in ds:
			ss[q][d] = 0.0
			product = 0.0
			for token in qs[q]:
				if token in ds[d]:
					tfidfQ = qs[q][token]
					tfidfD = ds[d][token]
					product += tfidfQ*tfidfD
					pass
				pass
			ss[q][d] = product/(qSum[q]*dSum[d])**0.5
			pass
		pass
	return ss

def output(ss, string):
	num = int(string)
	ls = []
	for q in ss:
		tuples = sorted(ss[q].items(), key = lambda x:x[1], reverse = True)[:num]
		ls += [(q, tuples)]
		pass
	ls.sort(key = lambda x:x[0])
	return ls

if __name__ == "__main__":
	indexes, tokens, nums = readInput(sys.argv[1])
	queries = readQuery(sys.argv[2])
	qs, ds = calculate(indexes, tokens, nums, queries)
	ss = similarity(qs, ds)
	ls = output(ss, sys.argv[3])
	print json.dumps(ls, sort_keys = True, indent = 4, separators = (",",":"))