#!/usr/bin/env python
#! -*- encoding: utf8 -*-

import sys, os, re

clean_re = re.compile('\W+')


def documents_processing(directory, index_file):
	dictionary_docs = {} 
	dictionary_terms = {}
	dictionary_news = {}

	docID = 0
	newID = 0
	list_files_dir = os.listdir(directory)
	for i in list_files_dir:
		path = os.path.join(directory, i)
		dictionary_docs[docID] = path
		file = open(path)
		content = file.read()
		news = content.split('<DOC>')
		news.pop(0) # Delete the first item, it is empty
		relative_position = 0
		for n in news:
			dictionary_news[newID] = (docID, relative_position) # Add entry 
			relative_position += len(n) # Current + length new
			new = n[n.index('<TEXT>') + 6 : n.index('</TEXT>')].lower()
			new = clean_re.sub(' ', new)
			terms = re.split('\s|\n|\t', new)
			for t in terms:
				if(t in dictionary_terms):
					dictionary_terms[t].append(newID)
				else:
					dictionary_terms[t] = [newID]
			newID += 1
		docID += 1


	del dictionary_terms[""] # TODO: Resolve this problem
	# ---- Printing stats -----
	print(len(dictionary_docs))
	print(len(dictionary_news))
	print(len(dictionary_terms))



if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 3:
    	print("Usage: python sar_indexer.py <dir_news> <index_file>")
    else: 
    	dir_news = sys.argv[1]
    	index_file = sys.argv[2]
    	documents_processing(dir_news, index_file)

        