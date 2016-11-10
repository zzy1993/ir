import json
import re
import sys

pathVSM1 = "/users/aleph/desktop/ir/resultsVSM1.txt"
pathVSM2 = "/users/aleph/desktop/ir/resultsVSM2.txt"
pathBM25 = "/users/aleph/desktop/ir/resultsBM25.txt"

def read():
	with open(pathVSM1) as f1:
		dataVSM1 = json.loads(f1.read().replace("(", "[").replace(")", "]"))
		dicVSM1 = {}
		for query in dataVSM1:
			dicVSM1[query[0]] = query[1]
			pass
	with open(pathVSM2) as f2:
		dataVSM2 = json.loads(f2.read())
		dicVSM2 = {}
		for query in dataVSM2:
			dicVSM2[query[0]] = query[1]
			pass
	with open(pathBM25) as f3:
		dataBM25 = json.loads(f3.read())
		dicBM25 = {}
		for query in dataBM25:
			dicBM25[query[0]] = query[1]
			pass
	return dicVSM1, dicVSM2, dicBM25

def compare(dicA, dicB):
	taus = {}

	for q in dicA:
		pairsA = dicA[q]
		pairsB = dicB[q]
		rankA = {pair[0]:i for i, pair in enumerate(pairsA)}
		rankB = {pair[0]:i for i, pair in enumerate(pairsB)}
		commons = set(rankA.keys())&set(rankB.keys())
		commonList = list(commons)
		var = 0
		count = 0
		for i in xrange(1, len(commonList)):
			d1 = commonList[i]
			for j in xrange(i):
				d2 = commonList[j]
				var += (rankA[d1]-rankA[d2])/abs(rankA[d1]-rankA[d2])*(rankB[d1]-rankB[d2])/abs(rankB[d1]-rankB[d2])
				count += 1
				pass
			pass
		taus[q] = float(var)/float(count)
	return taus

def output(tausVSM1_VSM2, tausVSM1_BM25, tausVSM2_BM25):
	print {"tausVSM1_VSM2":tausVSM1_VSM2, "tausVSM1_BM25":tausVSM1_BM25, "tausVSM2_BM25":tausVSM2_BM25}

if __name__ == "__main__":
	dicVSM1, dicVSM2, dicBM25 = read()
	tausVSM1_VSM2 = compare(dicVSM1, dicVSM2)
	tausVSM1_BM25 = compare(dicVSM1, dicBM25)
	tausVSM2_BM25 = compare(dicVSM2, dicBM25)
	output(tausVSM1_VSM2, tausVSM1_BM25, tausVSM2_BM25)
