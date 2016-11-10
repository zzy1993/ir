import re
import json
import sys

def read(pIn):
	with open(pIn, "r") as f:
		texts = f.read().split("#")[1:]
	documents = {}
	for text in texts:
		doc = text.replace("\n"," ").split()[0]
		words = [word for word in text.replace("\n"," ").split()[1:] if not word.isdigit()]
		documents[doc] = words
		pass
	return documents

def reverse(documents):
	# generate tokens
	se = set()
	for doc in documents:
		words = documents[doc]
		for word in words:
			se.add(word)
			pass
		pass
	tokens = list(se)

	# generate indexes
	tfs = {}
	for token in tokens:
		tfs[token] = {}
		pass
	for doc in documents:
		words = documents[doc]
		for word in words:
			if doc in tfs[word]:
				tfs[word][doc] += 1
			else:
				tfs[word][doc] = 1
			pass
		pass

	indexes = []
	for token in tokens:
		tuples = sorted(tfs[token].items(), key = lambda x:int(x[0]))
		indexes += [(token, tuples)]
	indexes.sort(key = lambda x:x[0])

	# generate nums
	nums = {}
	for doc in documents:
		words = documents[doc]
		nums[doc] = len(words)
		pass

	return indexes, tokens, nums

def write(indexes, tokens, nums, pOut):
	content = {"indexes": indexes, "tokens": tokens, "nums": nums}
	with open(pOut, "w") as f:
		f.write(json.dumps(content, sort_keys = True, indent = 4, separators = (",",":")))

if __name__ == "__main__":
	docs = read(sys.argv[1])
	indexes, tokens, nums = reverse(docs)
	write(indexes, tokens, nums, sys.argv[2])