#!/usr/bin/env python
#!encoding:utf-8

import sys, os, re
import pickle

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
		relative_new_position = 0
		for n in news:
			dictionary_news[newID] = (docID , relative_new_position) # Add entry 
			new = n[n.index('<TEXT>') + 6 : n.index('</TEXT>')].lower()
			new = clean_re.sub(' ', new) # Clean text
			terms = new.split() # Tokenize
			relative_term_position = 0
			for t in terms:
				if(t in dictionary_terms):
					if(newID == dictionary_terms[t][-1][0]): # Ultima posicio de la llista de tuple (ultima tupla)
						dictionary_terms[t][-1][1].append(relative_term_position)
					else:
						dictionary_terms[t].append((newID, [relative_term_position])) 
				else:
					dictionary_terms[t] = [(newID ,[relative_term_position])]
				relative_term_position += 1
			newID += 1
			relative_new_position += 1
		docID += 1

	
	# ---- Printing stats -----
	print(len(dictionary_docs))
	print(len(dictionary_news))
	print(len(dictionary_terms))

	file = open(index_file,'wb')
	pickle.dump((dictionary_terms, dictionary_docs, dictionary_news), file)


if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 3:
    	print("Usage: python sar_indexer.py <dir_news> <index_file>")
    else: 
    	dir_news = sys.argv[1]
    	index_file = sys.argv[2]
    	if not os.path.exists(dir_news):
    		print("Error: The directory " + dir_news + " doesn't exist")
    		sys.exit(1)

    	documents_processing(dir_news, index_file)

        